#!/usr/bin/env python

import vrchatapi
from vrchatapi.api.worlds_api import WorldsApi

import time
import json
from pathlib import Path

data = json.loads(Path('json/data.json').read_text())
skip = json.loads(Path('json/skip.json').read_text())

with vrchatapi.ApiClient() as api_client:
    api_client.user_agent = 'WorldInformationFetcher'

    worlds_api = WorldsApi(api_client)

    for c in range(0, len(data)):
        for w in range(0, len(data[c]['Worlds'])):
            if (data[c]['Worlds'][w]['ID'] is not None) and (not (data[c]['Worlds'][w]['ID'] in skip)):
                try:
                    world = worlds_api.get_world(data[c]['Worlds'][w]['ID'])
                    data[c]['Worlds'][w]['Name']                = world.name
                    data[c]['Worlds'][w]['RecommendedCapacity'] = world.recommended_capacity
                    data[c]['Worlds'][w]['Capacity']            = world.capacity
                    data[c]['Worlds'][w]['Description']         = world.description
                    data[c]['Worlds'][w]['ReleaseStatus']       = world.release_status

                    #pc      = True in [p.platform == 'standalonewindows' for p in world.unity_packages]
                    #android = True in [p.platform == 'android'           for p in world.unity_packages]
                    #data[c]['Worlds'][w]['Platform']            = {}
                    #data[c]['Worlds'][w]['Platform']['PC']      = pc
                    #data[c]['Worlds'][w]['Platform']['Android'] = android
                    
                    print(f'第{c+1:03}回-{w+1:02} Updated   ワールド名: {world.name}')

                except vrchatapi.exceptions.NotFoundException:
                    data[c]['Worlds'][w]['ID'] = None
                    print(f'第{c+1:03}回-{w+1:02} Not Found ワールド名: {data[c]['Worlds'][w]['Name']}')

                except Exception as e:
                    print(f'第{c+1:03}回-{w+1:02} Error!!!! ワールド名: {data[c]['Worlds'][w]['Name']}')
                    Path('json/data.json').write_text(json.dumps(data, indent=4, ensure_ascii=False))
                    raise e

                time.sleep(3)
            else:
                print(f'第{c+1:03}回-{w+1:02} Skipped   ワールド名: {data[c]['Worlds'][w]['Name']}')

    Path('json/data.json').write_text(json.dumps(data, indent=4, ensure_ascii=False))
