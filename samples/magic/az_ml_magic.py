from __future__ import print_function
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic)
from IPython.utils.ipstruct import Struct


@magics_class
class AMLHelpers(Magics):
    @cell_magic
    def save_file(self, parameter_s='', cell=None):
        opts, arg_str = self.parse_options(parameter_s, 'f:', list_all=True, posix=False)
        if cell is not None:
            arg_str += '\n' + cell

        return self._save_file(arg_str, opts, self.shell.user_ns)

    @cell_magic
    def list_subs(self, line, cell):
        from azure.cli.core._profile import Profile
        from azure.cli.core._util import CLIError
        self._redirect_logging('az.azure.cli.core._profile')
        profile = Profile()
        try:
            profile.get_subscription()
        except CLIError:
            profile.find_subscriptions_on_login(True, None, None, None, None)
        subs = profile.load_cached_subscriptions()
        if not subs:
            print('No subscriptions available.')
            print('Please run `az login` from the console then try again')
            return
        print("Available subscriptions:\n  {}".format('\n  '.join(
            [sub['name'] for sub in subs])))

    @cell_magic
    def select_sub(self, line, cell):
        from azure.cli.core._profile import Profile
        from azure.cli.core._util import CLIError
        self._redirect_logging('az.azure.cli.core._profile')
        sub_name = cell
        profile = Profile()
        subs = profile.load_cached_subscriptions()
        if not subs:
            profile.find_subscriptions_on_login(True, None, None, None, None)

        try:
            profile.set_active_subscription(sub_name)
            print('Active subscription set to {}'.format(profile.get_subscription()['name']))
        except CLIError as exc:
            print(exc)
            print('Active subscription remains {}'.format(profile.get_subscription()['name']))


    @cell_magic
    def env_setup(self, line, cell):
        pass

    @cell_magic
    def publish_batch_local(self, parameter_s='', cell=None):
        print('param: {}'.format(parameter_s))
        print('cell: {}'.format(cell))
        import sys
        print('sys.executable: {}'.format(sys.executable))
        import azure.cli.command_modules.ml.service.batch as b
        import azure.cli.command_modules.ml._util as u
        import os
        print(os.path.abspath(u.__file__))
        context = u.JupyterContext()
        context.local_mode = True

        b.batch_service_list(context)
        #  return line, cell

    @staticmethod
    def _redirect_logging(module_name):
        import logging
        from azure.cli.core.azlogging import CustomStreamHandler
        profile_logger = logging.getLogger(module_name)
        if not profile_logger.handlers:
            profile_logger.addHandler(CustomStreamHandler(logging.DEBUG, {
                True: '%(message)s',
                False: '%(levelname)s: %(message)s',
            }))

    @staticmethod
    def _save_file(code, opts, namespace):
        # read arguments
        opts.merge(Struct(f=None))
        file_name = opts.f

        if not file_name:
            return "Usage: %%save_file -f file_name"

        file_name = file_name[0]

        with open(file_name, 'w') as fileName:
            fileName.write(code)

        print("Saved cell to {}".format(file_name))
        return


from IPython import get_ipython

get_ipython().register_magics(AMLHelpers)
