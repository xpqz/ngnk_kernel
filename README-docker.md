# A Jupyter kernel for ngn/k

NOTE: This is alpha quality at best.

This is a jupyter kernel for [ngn/k](https://codeberg.org/ngn/k), derived from the [bash_kernel](https://github.com/takluyver/bash_kernel).

To use the kernel with docker, build and run the docker image:

    docker build -t ngnkern .

which fetches the most bleeding edge of ngn/k and builds it from source. Note that ngn/k is a moving target.

Run container as `ngnk`

    docker run --name ngnk --rm -p 8888:8888 -v ./notebooks ngnkern

or, better, as

    docker run --name ngnk --rm -p 8888:8888 -v "$(pwd)"/notebooks:/home/jovyan/notebooks ngnkern

sharing a directory `./notebooks` on the host as `/home/jovyan/notebooks` in the container for persistence.

If everything worked as intended, you should be given a URL to open.

To open a shell on the running container, you can do

    docker exec -it ngnk /bin/bash

For details of how this works, see the Jupyter docs on [wrapper kernels](http://jupyter-client.readthedocs.org//en/latest/wrapperkernels.html), and
`pexpect`'s docs on the [replwrap module](http://pexpect.readthedocs.org/en/latest/api/replwrap.html).
