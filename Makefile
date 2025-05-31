curdir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: all prepare wget merge complement symlink update partial-update deploy clean

all: wget merge complement symlink

prepare: .venv gh-pages

.venv:
	/usr/bin/python -m venv .venv
	$(curdir)/.venv/bin/pip install vrchatapi

gh-pages:
	git clone -b gh-pages git@github.com:wacky612/GenkaiTourWorldList.git gh-pages

wget:
	wget -i private/url -O cache/themes.json

merge:
	/usr/bin/python merge.py

complement:
	$(curdir)/.venv/bin/python complement.py

symlink:
	/usr/bin/python symlink.py

update:
	$(curdir)/.venv/bin/python update.py

partial-update:
	$(curdir)/.venv/bin/python partial_update.py

deploy:
	/bin/sh ffmpeg.sh
	/bin/sh deploy.sh

clean:
	rm cache/*
