.PHONY: help clean clean-pyc clean-build \
	lint \
	test \
	bump/major bump/minor bump/patch bump/mod \
	release sdist

help:
	@echo "test - run R tests"
	@echo "sdist, bdist_wheel - package"
	@echo "bump/major bump/minor bump/patch bump/mod - bump the version"
	@echo "release - package and upload a release"


test:
	$(MAKE) -C inst/unitTests


bump/major bump/minor bump/patch bump/mod:
	bumpversion --verbose $(@F)


release: sdist
	twine upload dist/*

sdist:
	python setup.py sdist
	ls -l dist
