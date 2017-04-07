from __future__ import print_function
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic)
from IPython.utils.ipstruct import Struct
import os
import argparse
import shlex


@magics_class
class AMLHelpers(Magics):

    @staticmethod
    def print_and_update_env(k, v):
        os.environ[k] = v
        print(' os.environ["{}"]="{}"'.format(k, v))
        return 'export {}={}'.format(k, v)

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
    def check_deployment(self, line):
        from azure.cli.core._profile import Profile
        from azure.cli.core.commands import client_factory
        from azure.mgmt.resource.resources import ResourceManagementClient
        from azure.cli.command_modules.ml._az_util import az_get_app_insights_account
        self._redirect_logging('az.azure.cli.core._profile')
        p = argparse.ArgumentParser()
        p.add_argument('-d', '--deployment', help='Long running deployment to check', required=True)
        parsed_args = p.parse_args(line.split())
        deployment_name = parsed_args.deployment

        # validate that user has selected a subscription
        profile = Profile()
        subs = profile.load_cached_subscriptions()
        if not subs:
            print('Please run %%select_sub before attempting to query.')
            return

        if 'deployment' not in deployment_name:
            print("Not a valid AML deployment name.")

        resource_group = deployment_name.split('deployment')[0]
        client = client_factory.get_mgmt_service_client(ResourceManagementClient).deployments
        result = client.get(resource_group, deployment_name)
        if result.properties.provisioning_state != 'Succeeded':
            print('Deployment status: {}'.format(result.properties.provisioning_state))
            return

        completed_deployment = result

        if 'appinsights' in completed_deployment.name:
            (app_insights_account_name,
             app_insights_account_key) = az_get_app_insights_account(completed_deployment)
            if app_insights_account_name and app_insights_account_key:

                print("Environment updated with AppInsight information.")
                print("This notebook will keep this environment available, though kernel restarts will clear it.")
                print("To reset the environment, use the following commands:")
                print(' import os')
                result_str = '\n'.join([
                        self.print_and_update_env('AML_APP_INSIGHTS_NAME', app_insights_account_name),
                        self.print_and_update_env('AML_APP_INSIGHTS_KEY', app_insights_account_key)])
                try:
                    with open(os.path.join(os.path.expanduser('~'), '.amlenvrc'), 'a') as env_file:
                        env_file.write(result_str)
                        print('{} has also been updated.'.format(env_file.name))
                except IOError:
                    pass
        else:
            acs_master = completed_deployment.properties.outputs['masterFQDN']['value']
            acs_agent = completed_deployment.properties.outputs['agentpublicFQDN'][
                'value']
            if acs_master and acs_agent:
                print('ACS deployment succeeded.')
                print("Environment updated with ACS information.")
                print("This notebook will keep this environment available, though kernel restarts will clear it.")
                print("To reset the environment, use the following commands:")
                print(' import os')

                result_str = '\n'.join([
                        self.print_and_update_env('AML_ACS_MASTER', acs_master),
                        self.print_and_update_env('AML_ACS_AGENT', acs_agent)])
                try:
                    with open(os.path.join(os.path.expanduser('~'), '.amlenvrc'), 'a') as env_file:
                        env_file.write(result_str)
                        print('{} has also been updated.'.format(env_file.name))
                except IOError:
                    pass


    @line_magic
    def env_setup(self, line):
        from azure.cli.core._profile import Profile
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
        from azure.cli.command_modules.ml._az_util import az_create_app_insights_account
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
        az_create_app_insights_account(parsed_args.name, resource_group)
        az_create_acs(parsed_args.name, resource_group, acr_login_server, c.acr_username,
                      acr_password, ssh_public_key)

        print("Environment configured, pending ACS deployment completion.")
        print("This notebook will keep this environment available, though kernel restarts will clear it.")
        print("To reset the environment, use the following commands:")
        print(' import os')
        result_str = '\n'.join([
            self.print_and_update_env('AML_STORAGE_ACCT_NAME', storage_account_name),
            self.print_and_update_env('AML_STORAGE_ACCT_KEY', storage_account_name),
            self.print_and_update_env('AML_ACR_HOME', acr_login_server),
            self.print_and_update_env('AML_ACR_USER', c.acr_username),
            self.print_and_update_env('AML_ACR_PW', acr_password)])
        try:
            with open(os.path.expanduser('~/.amlenvrc'), 'w+') as env_file:
                env_file.write(result_str)
                print('You can also find these settings saved in {}'.format(env_file.name))
        except IOError:
            pass


    @cell_magic
    def publish_realtime_local(self, parameter_s='', cell=None):
        import tempfile
        import azure.cli.command_modules.ml.service.realtime as r
        import azure.cli.command_modules.ml._util as u

        # reload util to get new environment vars
        self.easy_reload(u)
        p = argparse.ArgumentParser()
        p.add_argument('-s', '--schema', help='local path to schema file', required=True)
        p.add_argument('-m', '--model', help='local path to model', required=True)
        p.add_argument('-n', '--name', help='name of the webservice', required=True)
        p.add_argument('-o', '--overwrite', help='flag to overwrite existing service',
                       action='store_true')
        args = p.parse_args(parameter_s.split())
        context = u.JupyterContext()
        context.local_mode = True
        context.set_input_response('Delete existing service and create new service (y/N)? ',
                          'y' if args.overwrite else 'n')
        _, fp = tempfile.mkstemp()
        with open(fp, 'w') as score_file:
            score_file.write(cell)
        try:
            resp_code = r.realtime_service_create(score_file.name,
                                      dependencies=[], requirements='',
                                      schema_file=args.schema, service_name=args.name,
                                      verb=False, custom_ice_url='', target_runtime='spark-py',
                                      logging_level='', model=args.model, context=context)
            if resp_code == 1:
                print('Use -o flag to magic to overwrite the existing service.')
        finally:
            # cleanup
            os.remove(fp)

    @line_magic
    def list_realtime_local(self, line):
        from azure.cli.command_modules.ml.service.realtime import realtime_service_list
        from azure.cli.command_modules.ml._util import JupyterContext
        c = JupyterContext()
        c.local_mode = True
        realtime_service_list(context=c)

    @line_magic
    def view_realtime_local(self, line):
        import azure.cli.command_modules.ml.service.realtime as r
        import azure.cli.command_modules.ml._util as u

        p = argparse.ArgumentParser()
        p.add_argument('-n', '--name', help='name of the webservice', required=True)
        name = p.parse_args(line.split()).name
        context = u.JupyterContext()
        context.local_mode = True
        r.realtime_service_view(service_name=name, context=context)

    @line_magic
    def run_realtime_local(self, line):
        import azure.cli.command_modules.ml.service.realtime as r

        p = argparse.ArgumentParser()
        p.add_argument('-n', '--name', help='name of the webservice', required=True)
        p.add_argument('-d', '--data', help='data to send', default='')
        parsed_args = p.parse_args(shlex.split(line))
        name = parsed_args.name
        input_data = parsed_args.data
        r.realtime_service_run_local(service_name=name, input_data=input_data, verbose=False)

    @line_magic
    def delete_realtime_local(self, line):
        import azure.cli.command_modules.ml.service.realtime as r

        p = argparse.ArgumentParser()
        p.add_argument('-n', '--name', help='name of the webservice', required=True)
        name = p.parse_args(line.split()).name
        r.realtime_service_delete_local(service_name=name, verbose=False)

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

    @staticmethod
    def easy_reload(module):
        try:
            # python 3.4+ import
            from importlib import reload
        except ImportError:
            try:
                # 3 < 3.4
                from imp import reload
            except ImportError:
                pass
                # builtin for p2

        reload(module)

from IPython import get_ipython

get_ipython().register_magics(AMLHelpers)
