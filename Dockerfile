ARG BASE_CONTAINER=jupyter/minimal-notebook
FROM $BASE_CONTAINER

USER root

# Install some stuff required to build ngn/k
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -yq dist-upgrade && \
    apt-get install -yq --no-install-recommends \
    build-essential rlwrap && \
    rm -rf /var/lib/apt/lists/*

USER $NB_UID

# RUN pip install jupyter_contrib_nbextensions
# RUN jupyter contrib nbextension install --user
# RUN jupyter nbextension enable spellchecker/main

# Fetch and build ngn/k
RUN git clone https://codeberg.org/ngn/k.git && \
    cd k && \
    make k-dflt

ENV NGNKDIR=/home/jovyan/k

# Install the flit tool; a simplified python package manager
RUN pip install flit

# Fetch the ngnk_kernel source and install
RUN git clone https://github.com/xpqz/ngnk_kernel.git && \
    cd ngnk_kernel && \
    flit install && \
    python install.py --sys-prefix && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

USER $NB_UID
