#!/usr/bin/env python

from http.cookiejar import Cookie

import vrchatapi
from vrchatapi.api import authentication_api
from vrchatapi.api.worlds_api import WorldsApi

import time
import json
from pathlib import Path

auth   = json.loads(Path('private/auth.json').read_text())
cookie = json.loads(Path('private/cookie.json').read_text())
data   = json.loads(Path('json/data.json').read_text())

def make_cookie(name, value):
    return Cookie(0, name, value,
                  None, False,
                  "api.vrchat.cloud", True, False,
                  "/", False,
                  False,
                  173106866300,
                  False,
                  None,
                  None, {})

configuration = vrchatapi.Configuration(
    username = auth['Username'],
    password = auth['Password'],
)

with vrchatapi.ApiClient(configuration) as api_client:
    api_client.user_agent = 'WorldInformationFetcher'
    api_client.rest_client.cookie_jar.set_cookie(
        make_cookie('auth', cookie['AuthCookie']))
    api_client.rest_client.cookie_jar.set_cookie(
        make_cookie('twoFactorAuth', cookie['TwoFactorAuthCookie']))

    auth_api = authentication_api.AuthenticationApi(api_client)
    current_user = auth_api.get_current_user()
    print("Logged in as:", current_user.display_name)

    worlds_api = WorldsApi(api_client)

    for c in range(0, len(data)):
        for w in range(0, len(data[c]['Worlds'])):
            if (data[c]['Worlds'][w]['ID'] is not None) and (not ('Platform' in data[c]['Worlds'][w])):
                try:
                    world = worlds_api.get_world(data[c]['Worlds'][w]['ID'])
                    data[c]['Worlds'][w]['Name']                = world.name
                    data[c]['Worlds'][w]['RecommendedCapacity'] = world.recommended_capacity
                    data[c]['Worlds'][w]['Capacity']            = world.capacity
                    data[c]['Worlds'][w]['Description']         = world.description

                    pc      = True in [p.platform == 'standalonewindows' for p in world.unity_packages]
                    android = True in [p.platform == 'android'           for p in world.unity_packages]
                    data[c]['Worlds'][w]['Platform']            = {}
                    data[c]['Worlds'][w]['Platform']['PC']      = pc
                    data[c]['Worlds'][w]['Platform']['Android'] = android
                    
                    print(f'第{c+1:03}回-{w+1:02}     Found ワールド名: {world.name}')

                except vrchatapi.exceptions.NotFoundException:
                    data[c]['Worlds'][w]['ID'] = None
                    print(f'第{c+1:03}回-{w+1:02} Not Found ワールド名: {data[c]['Worlds'][w]['Name']}')

                except Exception as e:
                    print(f'第{c+1:03}回-{w+1:02} Crashed!! ワールド名: {data[c]['Worlds'][w]['Name']}')
                    Path('json/data.json').write_text(json.dumps(data, indent=2, ensure_ascii=False))
                    raise e

                time.sleep(3)
            else:
                print(f'第{c+1:03}回-{w+1:02} Skipped   ワールド名: {data[c]['Worlds'][w]['Name']}')

    Path('json/data.json').write_text(json.dumps(data, indent=2, ensure_ascii=False))
