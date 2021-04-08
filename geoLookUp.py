import json

with open("melbGrid2.json", "r") as f:
    grids_data = json.load(f)

grids = grids_data["features"]

geo = [145.150000, -37.950000]


def grid_search(geo, grids):
    grid_in = []
    for grid in grids:
        prop = grid["properties"]
        if (
            geo[0] <= prop["xmax"]
            and geo[0] >= prop["xmin"]
            and geo[1] <= prop["ymax"]
            and geo[1] >= prop["ymin"]
        ):
            grid_in.append(prop["id"])

    letter_dict = {"A": 0, "B": 10, "C": 20, "D": 30, "E": 40}
    grid_dict = {}
    for grid in grid_in:
        grid_dict[grid] = letter_dict[grid[0]] - int(grid[1])

    return max([(value, key) for key, value in grid_dict.items()])[1]


print(grid_search(geo, grids))
