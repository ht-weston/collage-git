SRC = $(wildcard src/*.tex)
OUT = $(wildcard dist/*)
PYPROG=python3
pubName=projectName_collage


all: images publish

watch: all
	./vimnotify
	make view

view: all
	okular ./dist/draft/main.pdf &!

publish:
	TEXINPUTS=src/: latexmk -outdir=dist/publish -pdf -quiet src/main.tex
	mv ./dist/publish/main.pdf ./dist/publish/$(shell date +%Y%m%d)_$(pubName).pdf

clean:
	rm -rf dist/draft/*

archive:
	git archive --format=zip HEAD > archive.zip

size:
	git count-objects -vH

images:
	$(PYPROG) src/main.py src/imgs/ src/imgs.tex src/shapeFile.csv

test:
	pytest

error:
	bat ./dist/draft/main.log
