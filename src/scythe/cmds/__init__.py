from importlib import import_module
from os import environ
import sys
from traceback import format_exception_only

from scythe import VERSION

COMMANDS = 'import', 'scan', 'watch', 'rqcli', 'start'

def main():
    if 'SCYTHE_DEBUG' not in environ:
        sys.excepthook = lambda t, v, tb: sys.exit('The following error occurred: ' + format_exception_only(t, v)[0].strip())
    try:
        subcommand = sys.argv.pop(1)
    except IndexError:
        sys.stderr.write('Available subcommsands: {}\n'.format(', '.join(COMMANDS)))
        sys.exit(1)
    if subcommand == 'version':
        sys.stderr.write('Version: {}\n'.format(VERSION))
        sys.exit(0)
    if subcommand not in COMMANDS:
        sys.stderr.write('Unknown subcommand {}; available subcommsands: {}\n'.format(subcommand, ', '.join(COMMANDS)))
        sys.exit(1)
    try:
        import_module( 'scythe.cmds.{0}'.format(subcommand)).main()
    except KeyboardInterrupt:
        sys.stderr.write('Premature exit!\n')
        sys.exit(1)
