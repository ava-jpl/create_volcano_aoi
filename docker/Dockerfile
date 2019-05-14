FROM hysds/pge-base:latest
MAINTAINER jlinick "Justin.P.Linick@jpl.nasa.gov"
LABEL description="Create Volcano AOI products"

USER ops

COPY . /home/ops/verdi/ops/create_volcano_aoi

WORKDIR /home/ops
CMD ["/bin/bash", "--login"]
