import os
import sys
import json
import base64
import argparse

from IPython.utils.tempdir import TemporaryDirectory
from jupyter_client.kernelspec import KernelSpecManager

kernel_logo = b'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'
kernel_json = {"argv":[sys.executable, "-m", "mysql_kernel", "-f", "{connection_file}"],
               "display_name":"Mysql",
               "language":"sql"}

def install_my_kernel_spec(user=True, prefix=None):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
        with open(os.path.join(td, 'logo-64x64.png'), 'wb') as f:
            f.write(base64.b64decode(kernel_logo))
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
