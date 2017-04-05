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
        from azure.cli.core.azlogging import CustomStreamHandler
        import logging
        class PrintLogger(logging.Logger):
            def _log(self, level, msg, args, exc_info=None, extra=None,
                     stack_info=False):
                print('{}: {}'.format(level, msg).format(args))

        logging.setLoggerClass(PrintLogger)
        profile_logger = logging.getLogger('az.azure.cli.core._profile')
        profile_logger.addHandler(CustomStreamHandler(logging.DEBUG, {
            True: '%(message)s',
            False: '%(levelname)s: %(message)s',
        }))
        profile = Profile()
        try:
            profile.get_subscription()
        except CLIError as exc:
            profile.find_subscriptions_on_login(True, None, None, None, None)
        subs = profile.load_cached_subscriptions()
        if not subs:
            print('No subscriptions available.')
            print('Please run `az login` from the console then try again')
            return
        print("Available subscriptions:\n  {}".format('\n  '.join(
            [sub['name'] for sub in subs])))

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
