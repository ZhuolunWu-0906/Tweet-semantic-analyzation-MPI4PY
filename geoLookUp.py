def grid_search(geo, grids):
    grid_dict = {}
    letter_dict = {"A": 0, "B": 10, "C": 20, "D": 30}
    for grid in grids:
        prop = grid["properties"]

        # if the coordinate is within any grid, mark the grid in with a value
        if (
            geo[0] <= prop["xmax"]
            and geo[0] >= prop["xmin"]
            and geo[1] <= prop["ymax"]
            and geo[1] >= prop["ymin"]
        ):
            grid_dict[prop["id"]] = letter_dict[prop["id"][0]] - int(prop["id"][1])*100

    return max([(value, key) for key, value in grid_dict.items()])[0]
