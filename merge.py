#!/usr/bin/env python

import json

data = []

with open("json/world_list.json", "r") as f:
    data = json.load(f)

with open("cache/themes.json", "r") as f:
    themes = json.load(f)['themes']


for i in range(len(data), len(themes)):
    dic = {}
    dic['Times'] = str(i + 1)
    dic['Theme'] = themes[i]['theme']
    dic['Worlds'] = []
    for w in themes[i]['worlds']:
        dic2 = {}
        dic2['Name'] = w['worldName']
        dic2['ID'] = w['worldId']
        dic['Worlds'].append(dic2)
    data.append(dic)

print(json.dumps(data, indent=2, ensure_ascii=False))
