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
        with open(os.path.join(td, 'logo_64x64.png'), 'wb') as f:
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
