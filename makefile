SRC = $(wildcard src/*.tex)
OUT = $(wildcard dist/*)
PYPROG=python3

all: clean
	latexmk -outdir=../dist/draft -pdf -cd -quiet src/main.tex

watch: all
	./vimnotify
	make view

view: all
	okular ./dist/draft/main.pdf &!

publish:
	latexmk -outdir=../dist/draft -pdf -cd -quiet src/main.tex

clean:
	rm -rf dist/draft/*

archive:
	git archive --format=zip HEAD > archive.zip

size:
	git count-objects -vH

images:
	$(PYPROG) src/main.py src/imgs/ src/imgs.tex src/shapeFile.csv

error:
	bat ./dist/draft/main.log
