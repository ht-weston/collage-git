SRC = $(wildcard src/*.tex)
OUT = $(wildcard dist/*)
PYPROG=python3
pubName=Anthony-Inc_IGP-Consulting
fname=$(shell date +%Y%m%d)_$(pubName)

all: images draft

watch: all
	./vimnotify
	make view

view:
	okular ./dist/draft/main.pdf &!

publish:
	TEXINPUTS=src/: latexmk -outdir=dist/publish -pdf -quiet src/main.tex
	mv ./dist/publish/main.pdf ./dist/publish/$(fname).pdf

compress: publish
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=./dist/publish/$(fname)_compressed.pdf ./dist/publish/$(fname).pdf

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
