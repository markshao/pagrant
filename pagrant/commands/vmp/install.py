__author__ = 'root'

from pip import main
from pkg_resources import load_entry_point
from pagrant.basecommand import Command
from pagrant.vendors.myoptparser.optparse import Option
from pagrant.exceptions import CommandError, VmProviderError


class InstallCommand(Command):
    name = "install"
    usage = """%prog """
    summary = "install the vmprovider from the repository"

    def __init__(self):
        super(InstallCommand, self).__init__()

        self.parser.add_option(Option(
            '--index-url',
            dest='index_url',
            action='store',
            default=None,
            help="change the source for the vmproviders repository"
        ))

    def run(self, args):
        options, arg_else = self.parse_args(args)

        if not arg_else or len(arg_else) != 1:
            raise CommandError("the vmprovider name is empty , could install it \n")

        from pagrant.commands.vmp import check_vmprovider_existed, add_into_vmprovider_dict

        vmprovider_name = arg_else[0]

        if not check_vmprovider_existed(vmprovider_name):
            # if vmprovider_name in providers_class_map:
            #     raise VmProviderError("The vmprovider has already support by the pagrant itself")

            install_commands = ["install", vmprovider_name]
            if options.index_url:
                install_commands.extend(["--index-url", options.index_url])

            # install_commands.extend(["-q"])  # make it quiet for output

            self.logger.warn("start install the vmprovider [{}]".format(arg_else[0]))
            exit_code = main(install_commands)

            if exit_code != 0:
                raise VmProviderError("Fail to install the vmprovier %s" % vmprovider_name)

            self.logger.warn("finish install the new provider")

            # persistant the info into the .vmprovider_dict
            # get the provider_summary from pkg_resource
            project_info = load_entry_point(vmprovider_name, "PAGRANT", "VMPROVIDER_INFO")()
            dist = {'summary': project_info['provider_summary']}

            add_into_vmprovider_dict(vmprovider_name, **dist)
        else:
            self.logger.warn("The vmprovider %s has already been installed " % vmprovider_name)