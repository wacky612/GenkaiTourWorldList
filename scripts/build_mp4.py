#!/usr/bin/python

import asyncio
import httpx
import json
import shutil
import tempfile
import subprocess
from pathlib import Path

CACHE_SERVER_URL = 'http://localhost:8010'

async def fetch_world_thumbnail(client, tmpdir, world, index):
    world_id = world['ID']
    
    if world_id is not None:
        response = await client.get(CACHE_SERVER_URL + f'/world/{world_id}/thumbnail')
        Path(f'{tmpdir}/{index:05}.png').write_bytes(response.content)
    else:
        shutil.copy(Path('image/black.png'), Path(f'{tmpdir}/{index:05}.png'))
    return

async def fetch_thumbnails_in_category(tmpdir, category, index):
    async with httpx.AsyncClient(timeout=120.0) as client:
        tasks = [fetch_world_thumbnail(client, tmpdir, world, index + i)
                 for i, world in enumerate(category['Worlds'])]
        await asyncio.gather(*tasks)

    return len(category['Worlds'])

async def fetch_thumbnails(tmpdir, lists, index):
    for category in lists:
        count = await fetch_thumbnails_in_category(tmpdir, category, index)
        index = index + count
    return index

async def main():
    lists = json.loads(Path('data/world_list.json').read_text())

    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copy(Path('image/black.png'), Path(f'{tmpdir}/00000.png'))
        index = await fetch_thumbnails(tmpdir, lists, 1)
        shutil.copy(Path('image/black.png'), Path(f'{tmpdir}/{index:05}.png'))

        subprocess.run(' '.join([f'ffmpeg -y -r 1',
                                 f'-i {tmpdir}/%05d.png',
                                 f'-vcodec libx264 -profile:v baseline -pix_fmt yuv420p -movflags +faststart',
                                 f'build/thumbnail.mp4']),
                   shell=True)

asyncio.run(main())
