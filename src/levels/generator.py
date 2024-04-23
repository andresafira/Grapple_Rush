import json


map_ = [[0 if i < 18 else 1 for j in range(40)] for i in range(20)]

for i in range(6):
        map_[18 - i][5 + 3*i] = 1
map_[17][24] = 1
map_[16][24] = 1
map_[15][24] = 1
with open('l1.json', 'w') as file:
    json.dump(map_, file, indent=2)
