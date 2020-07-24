cur_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))

act:
	source .$(cur_dir)

deact:
	deactivate

inst:
	pip install {}
