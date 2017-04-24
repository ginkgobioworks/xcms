FROM docker.ginkgobioworks.com/docker/python-base:v1.3.1
MAINTAINER Ginkgo Bioworks <test-dev@ginkgobioworks.com>

ENV HOME=/root
# Save $HOME for container environments
RUN echo $HOME > /etc/container_environment/HOME

ENV XCMS_HOME=/usr/src/xcms
RUN mkdir -p $XCMS_HOME

ARG DEBIAN_FRONTEND=noninteractive

# catools, runit, and xml are needed for running unit tests
RUN apt-get --assume-yes update && apt-get --assume-yes install --verbose-versions \
  libnetcdf-dev \
  r-base-core=3.3.1* \
  r-base-dev=3.3.1* \
  r-cran-rcpp=0.12.3* \
  r-cran-catools=1.17.1* \
  r-cran-rcpp=0.12.3* \
  r-cran-runit=0.4.31* \
  r-cran-xml=3.98*


WORKDIR $XCMS_HOME

COPY biocLite.R .
COPY install_bioconductor_deps .
RUN ./install_bioconductor_deps

COPY setup.py ./
COPY . ./
RUN pip install -vvv .

CMD ["make", "test"]
