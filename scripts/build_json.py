#!/usr/bin/python

import asyncio
import httpx

import json
from pathlib import Path

CACHE_SERVER_URL = 'http://localhost:8010'

async def fetch_world_info(client, world):
    world_id   = world['ID']
    world_name = world['Name']

    if world_id is not None:
        response = await client.get(CACHE_SERVER_URL + f'/world/{world_id}/info')
        new_world = json.loads(response.text)
        keys = ['ID', 'Name', 'RecommendedCapacity', 'Capacity',
                'Description', 'ReleaseStatus', 'Platform']
        return { key: new_world[key] for key in keys }
    else:
        new_world = {}
        new_world['ID']   = world_id
        new_world['Name'] = world_name
        return new_world

async def build_category(category):
    new_category = {}
    new_category['Category'] = category['Category']
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        tasks = [fetch_world_info(client, world) for world in category['Worlds']]
        new_category['Worlds'] = await asyncio.gather(*tasks)

    return new_category

async def build_lists(lists):
    new_lists = []

    for category in lists:
        new_lists.append(await build_category(category))

    return new_lists

async def main():
    lists = json.loads(Path('data/world_list.json').read_text())

    data = {}
    data['ReverseCategorys'] = True;
    data['ShowPrivateWorld'] = False;
    data['Categorys']        = await build_lists(lists)

    Path('build/data.json').write_text(json.dumps(data, ensure_ascii=False))

asyncio.run(main())
