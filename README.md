# A Jupyter kernel for ngn/k

NOTE: This is alpha quality at best.

This is a jupyter kernel for [ngn/k](https://codeberg.org/ngn/k), derived from the [bash_kernel](https://github.com/takluyver/bash_kernel).

To use the kernel with docker, see the file README-Docker.md

## Install

Ensure that you have a working build of ngn/k. This kernel expects that you have built the `k-libc` version. Set the environment variable `NGNKDIR`

    export NGNKDIR="/your/path/to/k/dir"

so that the executable can be reached as `/your/path/to/k/dir/k-libc`.

Now run

    `python install.py --sys-prefix`

and start the notebook server

    jupyter notebook

For details of how this works, see the Jupyter docs on [wrapper kernels](http://jupyter-client.readthedocs.org//en/latest/wrapperkernels.html), and
`pexpect`'s docs on the [replwrap module](http://pexpect.readthedocs.org/en/latest/api/replwrap.html).
