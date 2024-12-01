curdir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: all wget merge update deploy clean prepare

all: wget merge update

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

update:
	cp cache/data.json json/data.json

deploy:
	/bin/sh deploy.sh

clean:
	rm cache/*
