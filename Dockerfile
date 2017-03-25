FROM docker.ginkgobioworks.com/docker/python-base
MAINTAINER Ginkgo Bioworks <test-dev@ginkgobioworks.com>

ENV HOME=/root
# Save $HOME for container environments
RUN echo $HOME > /etc/container_environment/HOME

ENV XCMS_HOME=/usr/src/xcms
RUN mkdir -p $XCMS_HOME

ARG DEBIAN_FRONTEND=noninteractive

# catools, runit, and xml are needed for running unit tests
RUN apt-get --assume-yes update && apt-get --assume-yes upgrade && apt-get --assume-yes install \
  libnetcdf-dev \
  r-base-dev \
  r-cran-catools \
  r-cran-rcpp \
  r-cran-runit \
  r-cran-xml

WORKDIR $XCMS_HOME

COPY install_bioconductor_deps .
RUN ./install_bioconductor_deps

COPY setup.py .
COPY requirements.txt .
RUN pip install --requirement requirements.txt

COPY . .

RUN pip install --editable .

CMD ["make", "test"]
