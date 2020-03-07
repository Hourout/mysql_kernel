from ipykernel.kernelapp import IPKernelApp
from .kernel import MysqlKernel


IPKernelApp.launch_instance(kernel_class=MysqlKernel)
