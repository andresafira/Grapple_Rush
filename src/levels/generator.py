import json


map_ = [[0 if i < 20 else 1 for j in range(50)] for i in range(30)]

for i in range(6):
        map_[20 - i][5 + 3*i] = 1
map_[19][24] = 1
map_[18][24] = 1
map_[17][24] = 1
with open('l1.json', 'w') as file:
    json.dump(map_, file, indent=2)
