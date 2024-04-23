import json


map_ = [[-1 if i < 18 else 1 for j in range(40)] for i in range(20)]

for i in range(6):
        map_[18 - i][5 + 3*i] = 0
map_[17][24] = 0
map_[16][24] = 0
map_[15][24] = 0
with open('l1.json', 'w') as file:
    json.dump(map_, file, indent=2)
