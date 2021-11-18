# A Jupyter kernel for ngn/k

NOTE: This is alpha quality at best.

This is a jupyter kernel for [ngn/k](https://codeberg.org/ngn/k), derived from the [bash_kernel](https://github.com/takluyver/bash_kernel).

This kernel is designed to run in a docker container, which fetches the most bleeding edge of ngn/k and builds it from source. Note that ngn/k is a moving target.

If you want to run this kernel 'natively' instead of in Docker, you need to do two things:

1. Change the line

    cmd = '/home/jovyan/k/k-libc /home/jovyan/k/repl.k'

in `NgnkKernel` to reflect your ngn/k installation location.

2. Change the prompt in `repl.k` and rebuild:

    repl.prompt:"ngnk> "

This is so that `pexpect` has something to look for. See the `Dockerfile`.

To use the kernel, build and run the docker image:

    docker build -t ngnkern .

Run container as `ngnk`

    docker run --name ngnk --rm -p 8888:8888 -v ./notebooks ngnkern

If everything worked as intended, you should be given a URL to open.

To open a shell on the running container, you can do

    docker exec -it ngnk /bin/bash

For details of how this works, see the Jupyter docs on [wrapper kernels](http://jupyter-client.readthedocs.org//en/latest/wrapperkernels.html), and
`pexpect`'s docs on the [replwrap module](http://pexpect.readthedocs.org/en/latest/api/replwrap.html).
