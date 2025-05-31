#!/usr/bin/env python

import os
import json
from pathlib import Path

data = json.loads(Path('json/data.json').read_text())

i = 1

for c in range(0, len(data)):
    for w in range(0, len(data[c]['Worlds'])):
        dst = f'{os.getcwd()}/thumbnail/link/{i:05}.png'
        if os.path.lexists(dst): os.remove(dst)
        
        if (data[c]['Worlds'][w]['ID'] is not None):
            src = f'{os.getcwd()}/thumbnail/img/{data[c]['Worlds'][w]['ID']}.png'
            os.symlink(src, dst)
        else:
            src = f'{os.getcwd()}/thumbnail/black.png'
            os.symlink(src, dst)
        
        i = i + 1
