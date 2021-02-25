SRC = $(wildcard src/*.tex)
OUT = $(wildcard dist/*)
PYPROG=python3
pubName=20-21UCLA-Monitoring_CoGen

all: images draft

watch: all
	./vimnotify
	make view

view: all
	okular ./dist/draft/main.pdf &!

publish:
	TEXINPUTS=src/: latexmk -outdir=dist/publish -pdf -quiet src/main.tex
	mv ./dist/publish/main.pdf ./dist/publish/$(shell date +%Y%m%d)_$(pubName).pdf

draft:
	TEXINPUTS=src/: latexmk -outdir=dist/draft -pdf -quiet src/main.tex

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
