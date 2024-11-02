.PHONY: all wget merge update deploy clean

gh-pages:
	git clone -b gh-pages git@github.com:wacky612/GenkaiTourWorldList.git gh-pages

all: wget merge update deploy

wget:
	wget -i private/url -O cache/themes.json

merge:
	/usr/bin/python merge.py > cache/merged_list.json

update:
	cp cache/merged_list.json json/world_list.json

deploy:
	/bin/sh deploy.sh

clean:
	rm cache/*
