import json


map_ = [[0 if i < 20 else 1 for j in range(50)] for i in range(30)]

with open('l1.json', 'w') as file:
    json.dump(map_, file, indent=2)
