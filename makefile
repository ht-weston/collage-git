SRC = $(wildcard src/*.tex)
OUT = $(wildcard dist/*)

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
	cd src/
	python main.py ./imgs/ > ./imgs.tex
