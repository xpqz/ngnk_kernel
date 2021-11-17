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

# Fetch and build ngn/k
RUN git clone https://codeberg.org/ngn/k.git && \
    cd k && \
    git rev-parse --short HEAD > VER && \
    sed 's/repl.prompt:," "/repl.prompt:"ngnk> "/' repl.k>repl.k.new && \
    mv repl.k.new repl.k && \
    make k-libc

# Fetch the ngnk_kernel source and install
RUN git clone https://github.com/xpqz/ngnk_kernel.git && \
    cd ngnk_kernel && \
    python install.py --sys-prefix && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

USER $NB_UID
