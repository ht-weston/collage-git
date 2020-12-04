SRC = $(wildcard src/*.tex)
OUT = $(wildcard dist/*)

all:
	latexmk -outdir=../dist/draft -pdf -cd -quiet src/*.tex

clean:

watch:
