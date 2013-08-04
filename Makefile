develop: update-submodules
	python setup.py develop


update-submodules:
	git submodule init
	git submodule update
