#!/bin/sh

python build.py
cd gh-pages
git add data.json
git commit --amend --no-edit
git -c core.sshCommand="ssh -i ../private/ssh/id_ed25519 -F /dev/null" push -f
