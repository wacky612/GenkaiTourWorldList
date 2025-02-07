#!/usr/bin/env python

import json
from pathlib import Path

data = {}
data['ReverseCategorys'] = True;
data['ShowPrivateWorld'] = False;
data['Categorys']        = json.loads(Path('json/data.json').read_text())

Path('gh-pages/data.json').write_text(json.dumps(data, indent=4, ensure_ascii=False))
