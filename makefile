venv: env/bin/activate
env/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

devbuild: venv
	venv/bin/python setup.py install

test: devbuild
	venv/bin/python test/runtests.py
