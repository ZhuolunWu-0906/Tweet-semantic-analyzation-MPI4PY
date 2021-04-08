import json
from geoLookUp import grid_search

# Read latitudes and longitudes of grids from melbGrid.json
with open("melbGrid2.json", "r") as f:
    grids_data = json.load(f)
grids = grids_data["features"]

# Initialize the scoreboard
scoreboard = {}
for grid in grids:
    scoreboard[grid["properties"]["id"]] = [0,0]
print(scoreboard)

# Test grid search
print(grid_search([145.15000, -37.950000],grids))

# Read tweets


# Calculating scores