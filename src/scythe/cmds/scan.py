from argparse import ArgumentParser

from scythe.upload import scan

def main():
    parser = ArgumentParser(prog = 'scythe scan')
    parser.add_argument('--harvests_dir', '-H', help = 'The harvests directory.', required = True)
    parser.add_argument('--session_id', '-s', help = 'The session identifier.', required = True)
    parser.add_argument('--no-clean', '-n', default = False, help = 'Whether to start from a clean result state.', action = 'store_true')
    args = parser.parse_args()

    scan(args.harvests_dir, args.session_id, not args.no_clean)
