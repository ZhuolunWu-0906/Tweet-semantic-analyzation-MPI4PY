from mpi4py import MPI
import csv
import sys
import json

MASTER_RANK = 0

# Read latitudes and longitudes of grids from melbGrid.json


def read_grids(grid_file):
    with open(grid_file) as f:
        grids_data = json.load(f)
    return grids_data["features"]

# Read word mark board


def read_markboard(dict_file):
    scores = open(dict_file)
    score_dict = {}
    for line in scores:
        key, value = line.rsplit("	", 1)
        score_dict[key] = value.replace("\n", "")
    return score_dict

# Find geolocation from coordinates


def grid_search(geo, grids):
    grid_dict = {}
    letter_dict = {"A": 0, "B": 10, "C": 20, "D": 30}
    for grid in grids:
        prop = grid["properties"]

        # If the coordinate is within any grid, mark the grid in with a value
        if (
            geo[0] <= prop["xmax"]
            and geo[0] >= prop["xmin"]
            and geo[1] <= prop["ymax"]
            and geo[1] >= prop["ymin"]
        ):
            grid_dict[prop["id"]] = letter_dict[prop["id"][0]] - \
                int(prop["id"][1])*100

    return max([(value, key) for key, value in grid_dict.items()])[1]

# Calculate sentiment score


def text_to_score(text, score_dict):
    mark = 0
    head = text.split()[:-1]
    foot = text.split()[1:]
    for i in range(len(head)):
        head[i] = head[i]+" "+foot[i]
    for i in head:
        if(i.strip("!,?.\'\"") in score_dict.keys()):
            mark += int(score_dict[i.strip("!,?.\'\"")])
            text = text.replace(i, '', 1)
    for i in text.split():
        if(i.strip("!,?.\'\"") in score_dict.keys()):
            mark += int(score_dict[i.strip("!,?.\'\"")])
    return mark


def process_tweets(rank, size, tweets_file, score_dict, grids):

    # Initialize the scoreboard
    scoreboard = {}
    for grid in grids:
        scoreboard[grid["properties"]["id"]] = [0, 0]

    with open(tweets_file) as f:
        for i, line in enumerate(f):
            if i % size == rank:
                if len(line) > 200:
                    try:
                        tweet = json.loads(line[:-2])
                        geo = grid_search(
                            tweet['value']['geometry']['coordinates'], grids)
                        text = (tweet['value']['properties']['text']).lower()
                        scoreboard[geo][0] += 1
                        scoreboard[geo][1] += text_to_score(text, score_dict)
                    except Exception as e:
                        pass

    return scoreboard


def marshall_scores(comm):
    size = comm.Get_size()
    dicts = []
    for i in range(size - 1):
        comm.send('return_data', dest=(i + 1), tag=(i + 1))
    for i in range(size - 1):
        dicts.append(comm.recv(source=(i + 1), tag=MASTER_RANK))
    return dicts


def master(comm, tweets_file, score_dict, grids):

    rank = comm.Get_rank()
    size = comm.Get_size()

    scoreboard = process_tweets(rank, size, tweets_file, score_dict, grids)

    if size > 1:
        dicts = marshall_scores(comm)
        for i in dicts:
            for key, value in i.items():
                scoreboard[key][0] += value[0]
                scoreboard[key][1] += value[1]
        for i in range(size - 1):
            comm.send('exit', dest=(i + 1), tag=(i + 1))

    print(scoreboard)


def slave(comm, tweets_file, score_dict, grids):

    rank = comm.Get_rank()
    size = comm.Get_size()

    scoreboard = process_tweets(rank, size, tweets_file, score_dict, grids)

    while True:
        in_comm = comm.recv(source=MASTER_RANK, tag=rank)
        if isinstance(in_comm, str):
            if in_comm in ("return_data"):
                comm.send(scoreboard, dest=MASTER_RANK, tag=MASTER_RANK)
            elif in_comm in ("exit"):
                exit(0)


def main(argv):
    tweets_file = argv[0]
    score_dict = read_markboard(argv[1])
    grids = read_grids(argv[2])

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        master(comm, tweets_file, score_dict, grids)
    else:
        slave(comm, tweets_file, score_dict, grids)

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
