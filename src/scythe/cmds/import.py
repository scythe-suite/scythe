from argparse import ArgumentParser

from scythe.config import add

def main():
    parser = ArgumentParser(prog = 'scythe import')
    parser.add_argument('--config', '-c', help = 'The path of the Tristo Mietitore config file.', required = True)
    parser.add_argument('--session_id', '-s', help = 'The session identifier.', required = True)
    parser.add_argument('--no-clean', '-n', default = False, help = 'Whether to clean same session_id configurations before importing.', action = 'store_true')

    args = parser.parse_args()

    add(args.config, args.session_id, not args.no_clean)
