#!/bin/sh

cp json/world_list.json gh-pages
cd gh-pages
git add world_list.json
git commit --amend --no-edit
git -c core.sshCommand="ssh -i ../private/ssh/id_ed25519 -F /dev/null" push -f
