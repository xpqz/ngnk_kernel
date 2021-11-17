from ipykernel.kernelapp import IPKernelApp
from .kernel import NgnkKernel

IPKernelApp.launch_instance(kernel_class=NgnkKernel)
