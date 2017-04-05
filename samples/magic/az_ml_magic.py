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
        sub_name = cell.strip()
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

    @line_magic
    def env_stuff(self, line):
        import os
        os.environ['bob'] = 'hey'


    @line_magic
    def env_setup(self, line):
        from azure.cli.core._profile import Profile
        import argparse
        import os
        self._redirect_logging('az.azure.cli.core._profile')
        p = argparse.ArgumentParser()
        p.add_argument('-n', '--name', help='base name for your environment', required=True)
        parsed_args = p.parse_args(line.split())

        # validate that user has selected a subscription
        profile = Profile()
        subs = profile.load_cached_subscriptions()
        if not subs:
            print('Please run %%select_sub before attempting to set up environment.')
            return
        from azure.cli.command_modules.ml._util import create_ssh_key_if_not_exists
        from azure.cli.command_modules.ml._util import JupyterContext
        from azure.cli.command_modules.ml._az_util import az_create_resource_group
        from azure.cli.command_modules.ml._az_util import az_create_storage_account
        from azure.cli.command_modules.ml._az_util import az_create_acr
        from azure.cli.command_modules.ml._az_util import az_create_acs
        print('Setting up your Azure ML environment with a storage account, App Insights account, ACR registry and ACS cluster.')
        c = JupyterContext()
        try:
            ssh_public_key = create_ssh_key_if_not_exists()
        except:
            return
        resource_group = az_create_resource_group(c, parsed_args.name)
        storage_account_name, storage_account_key = az_create_storage_account(c,
                                                                              parsed_args.name,
                                                                              resource_group)
        (acr_login_server, c.acr_username, acr_password) = \
            az_create_acr(c, parsed_args.name, resource_group, storage_account_name)
        az_create_acs(parsed_args.name, resource_group, acr_login_server, c.acr_username,
                      acr_password, ssh_public_key)

        os.environ['AML_STORAGE_ACCT_NAME'] = storage_account_name
        os.environ['AML_STORAGE_ACCT_KEY'] = storage_account_key
        os.environ['AML_ACR_HOME'] = acr_login_server
        os.environ['AML_ACR_USER'] = c.acr_username
        os.environ['AML_ACR_PW'] = acr_password
        env_verb = 'export'
        env_statements = ["{} AML_STORAGE_ACCT_NAME='{}'".format(env_verb, storage_account_name),
                          "{} AML_STORAGE_ACCT_KEY='{}'".format(env_verb, storage_account_key),
                          "{} AML_ACR_HOME='{}'".format(env_verb, acr_login_server),
                          "{} AML_ACR_USER='{}'".format(env_verb, c.acr_username),
                          "{} AML_ACR_PW='{}'".format(env_verb, acr_password)]
        print('Environment configured, pending ACS deployment completion.')
        print('This notebook will keep this environment available, though kernel restarts may clear it.')
        print('To reset the environment, use the following commands:')
        print('\n'.join([' {}'.format(statement) for statement in env_statements]))

        try:
            with open(os.path.expanduser('~/.amlenvrc'), 'w+') as env_file:
                env_file.write('\n'.join(env_statements) + '\n')
            print('You can also find these settings saved in {}'.format(os.path.join(os.path.expanduser('~'), '.amlenvrc')))
        except IOError:
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
