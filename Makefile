develop: update-submodules
	pip install -q "file://`pwd`#egg=aurora[dev]" --use-mirrors


update-submodules:
	git submodule init
	git submodule update
