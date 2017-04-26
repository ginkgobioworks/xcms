FROM docker.ginkgobioworks.com/docker/python-base:v1.3.3
MAINTAINER Ginkgo Bioworks <test-dev@ginkgobioworks.com>

ENV HOME=/root
# Save $HOME for container environments
RUN echo $HOME > /etc/container_environment/HOME

ENV XCMS_HOME=/usr/src/xcms
RUN mkdir -p $XCMS_HOME

ARG DEBIAN_FRONTEND=noninteractive

# Install as many Bioconductor and CRAN packagages from binary as we can to save build time.
# As long as we use the biocLite function from the BiocInstaller library in the Ubuntu package,
# instead of downloading it fresh, any additional packages that it compiles from source should
# be the right ones for this release of Bioconductor and R version (3.2)
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
