FROM python:3.8.10-alpine

ADD requirements.txt evoppi-interactomes/

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r evoppi-interactomes/requirements.txt

ARG version

ENV VERSION=${version}

ADD core evoppi-interactomes/core
ADD query_single_species evoppi-interactomes/query_single_species
ADD list_species evoppi-interactomes/list_species
ADD list_interactomes evoppi-interactomes/list_interactomes

RUN chmod u+x evoppi-interactomes/* && \
    sed -i 's#/usr/bin/#/usr/local/bin/#g' evoppi-interactomes/query_single_species && \
    sed -i 's#/usr/bin/#/usr/local/bin/#g' evoppi-interactomes/list_species && \
    sed -i 's#/usr/bin/#/usr/local/bin/#g' evoppi-interactomes/list_interactomes

ENV PATH=/evoppi-interactomes:${PATH}
