from argparse import ArgumentParser
from multiprocessing import Process

from rq import Worker

from scythe import redis

def main():
    parser = ArgumentParser(prog = 'scythe start')
    parser.add_argument('--num_workers', '-w', help = 'The number of workers.', required = True, type = int)
    args = parser.parse_args()

    processes = []
    for n in range(args.num_workers):
        worker = Worker('default', name = 'Scythe-worker-{}'.format(n), connection = redis)
        p = Process(target = worker.work)
        p.start()
        processes.append(p)
    for p in processes: p.join()
