import json
from geoLookUp import grid_search

# Read latitudes and longitudes of grids from melbGrid.json
with open("melbGrid2.json", "r") as f:
    grids_data = json.load(f)
grids = grids_data["features"]

# Test grid search
print(grid_search([145.15000, -37.950000],grids))