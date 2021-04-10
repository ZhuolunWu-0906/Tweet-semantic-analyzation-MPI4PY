import json
from geoLookUp import grid_search
from wordmark import text_to_score

# Read latitudes and longitudes of grids from melbGrid.json
with open("melbGrid.json", "r") as f:
    grids_data = json.load(f)
grids = grids_data["features"]

# Initialize the scoreboard
scoreboard = {}
for grid in grids:
    scoreboard[grid["properties"]["id"]] = [0,0]

# Test grid search
# print(grid_search([145.15000, -37.950000],grids))

# Read tweets
text = open("tinyTwitter.json",'rb')
text_dict = json.load(text)

# Read word mark board
wordmark = open("AFINN.txt")
wordmark_d = {}
for line in wordmark:
    key, value = line.rsplit("	", 1)
    wordmark_d[key] = value.replace("\n", "")

# Calculating scores

for i in text_dict['rows']:
    geo = grid_search(i['value']['geometry']['coordinates'],grids)
    text = (i['value']['properties']['text']).lower()
    # print(text)
    mark = text_to_score(text,wordmark_d)
    # print(str(mark)+'\n')
    scoreboard[geo][0] += 1
    scoreboard[geo][1] += mark
print(scoreboard)