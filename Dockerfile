FROM docker.ginkgobioworks.com/docker/python-base:v1.3.3
MAINTAINER Ginkgo Bioworks <test-dev@ginkgobioworks.com>

ENV HOME=/root
# Save $HOME for container environments
RUN echo $HOME > /etc/container_environment/HOME

ENV XCMS_HOME=/usr/src/xcms
RUN mkdir -p $XCMS_HOME

ARG DEBIAN_FRONTEND=noninteractive

# CRAN packages catools, runit, and xml are needed for running unit tests.
# As long as we use BiocInstaller from ubuntu's package, any packages compiled
# by BioConductor from source should work
RUN apt-get --assume-yes update && apt-get --assume-yes install --verbose-versions \
  r-base-core \
  r-base-dev \
  r-bioc-biobase \
  r-bioc-biocgenerics \
  r-bioc-biocinstaller \
  r-bioc-multtest \
  r-cran-catools \
  r-cran-lattice \
  r-cran-plyr \
  r-cran-rcolorbrewer \
  r-cran-rcpp \
  r-cran-rgl \
  r-cran-runit \
  r-cran-xml


WORKDIR $XCMS_HOME

COPY install_bioconductor_deps .
RUN ./install_bioconductor_deps

COPY setup.py ./
COPY . ./
RUN pip install -vvv .

CMD ["make", "test"]
