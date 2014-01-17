__author__ = 'root'

from pip import main
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

        if check_vmprovider_existed(vmprovider_name):
            install_commands = ["install", vmprovider_name]

            if options.index_url:
                install_commands.extend(["--index-url", options.index_url])

            # install_commands.extend(["-q"])  # make it quiet for output

            self.logger.warn("start install the vmprovider [{}]".format(arg_else[0]))
            exit_code = main(install_commands)

            if exit_code != 0:
                raise VmProviderError("Fail to install the vmprovier %s" % vmprovider_name)

            self.logger.warn("finish install the new provider")

            try:
                module = __import__(vmprovider_name)
            except ImportError:
                raise VmProviderError("Could not load the module %s" % vmprovider_name)

            # persistant the info into the .vmprovider_dict
            dist = {"summary": getattr(module, "provider_summary", "nothing")}

            add_into_vmprovider_dict(vmprovider_name, **dist)
        else:
            self.logger.warn("The vmprovider %s has already been installed " % vmprovider_name)