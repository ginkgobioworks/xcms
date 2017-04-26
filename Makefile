.PHONY: help clean clean-build \
	test \
	bump/major bump/minor bump/patch bump/mod \
	release sdist bdist_wheel

PROJECT_NAME = xcms
BUILD_IMAGE ?= ${PROJECT_NAME}
CI_PROJECT_PATH ?= testpipe/${PROJECT_NAME}
XCMS_HOME ?= /usr/src/${PROJECT_NAME}

SETUP = python ${XCMS_HOME}/setup.py

help:
	@echo "test - run R tests"
	@echo "sdist, bdist_wheel - package"
	@echo "bump/major bump/minor bump/patch bump/mod - bump the version; only bump mod"
	@echo "release - package and upload a release"

clean: clean-build

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info


test:
	$(MAKE) -C inst/unitTests


bump/major bump/minor bump/patch bump/mod:
	bumpversion --verbose $(@F)


release: clean sdist bdist_wheel
	twine upload dist/*

sdist:
	${SETUP} sdist
	ls -l dist

bdist_wheel:
	${SETUP} bdist_wheel
	ls -l dist


## Image manipulation and running from outside

MAKE_EXT = docker-compose run --rm ${PROJECT_NAME} make -C ${XCMS_HOME}

# Generically execute make targets from outside the Docker container
%-ext: image
	${MAKE_EXT} $*

# Build the image
image:
	docker-compose build --pull

# Add the image to the docker registry
push: image
	docker push ${BUILD_IMAGE}

#  vim: set noet
