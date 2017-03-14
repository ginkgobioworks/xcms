.PHONY: help clean clean-pyc clean-build \
	lint \
	test test-tox \
	bump/major bump/minor bump/patch \
	release

help:
	@echo "test - run R tests"
	@echo "sdist, bdist_wheel - package"
	@echo "bump/major bump/minor bump/patch - bump the version"
	@echo "release - package and upload a release"


test:
	$(MAKE) -C inst/unitTests


bump/major bump/minor bump/patch bump/mod:
	bumpversion --verbose $(@F)


release: sdist bdist_wheel
	twine upload dist/*

sdist:
	python setup.py sdist
	ls -l dist

bdist_wheel:
	python setup.py bdist_wheel
	ls -l dist
