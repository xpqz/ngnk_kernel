# A Jupyter kernel for bash

This requires IPython 3.

To use the kernel, build and run the docker image:

    docker build -t ngnkern .

Run container as `ktest`

    docker run --name ktest --rm -p 8888:8888 -v ./notebooks ngnkern

To open a shell:

    docker exec -it ktest /bin/bash

For details of how this works, see the Jupyter docs on [wrapper kernels](http://jupyter-client.readthedocs.org//en/latest/wrapperkernels.html), and
Pexpect's docs on the [replwrap module](http://pexpect.readthedocs.org/en/latest/api/replwrap.html).

