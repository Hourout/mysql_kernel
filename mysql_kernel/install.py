import os
import sys
import json
import argparse

from IPython.utils.tempdir import TemporaryDirectory
from jupyter_client.kernelspec import KernelSpecManager


kernel_json = {"argv":[sys.executable, "-m", "mysql_kernel", "-f", "{connection_file}"],
               "display_name":"Mysql",
               "language":"mysql"}

def install_my_kernel_spec(user=True, prefix=None):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
        print('Installing Jupyter Mysql kernel spec.')
        KernelSpecManager().install_kernel_spec(td, 'Mysql', user=user, replace=True, prefix=prefix)

def _is_root():
    try:
        return os.geteuid()==0
    except AttributeError:
        return False

def main(argv=None):
    parser = argparse.ArgumentParser(description='Install Jupyter KernelSpec for Mysql Kernel.')
    prefix_locations = parser.add_mutually_exclusive_group()
    prefix_locations.add_argument('--user',
                                  help='Install Jupyter Mysql KernelSpec in user homedirectory.',
                                  action='store_true')
    prefix_locations.add_argument('--sys-prefix',
                                  help='Install Jupyter Mysql KernelSpec in sys.prefix. Useful in conda / virtualenv',
                                  action='store_true',
                                  dest='sys_prefix')
    prefix_locations.add_argument('--prefix',
                                  help='Install Jupyter Mysql KernelSpec in this prefix',
                                  default=None)
    args = parser.parse_args(argv)

    user = False
    prefix = None
    if args.sys_prefix:
        prefix = sys.prefix
    elif args.prefix:
        prefix = args.prefix
    elif args.user or not _is_root():
        user = True

    install_my_kernel_spec(user=user, prefix=prefix)

if __name__ == '__main__':
    main()
