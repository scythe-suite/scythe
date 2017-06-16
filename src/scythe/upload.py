from base64 import decodestring
from datetime import datetime
from fnmatch import fnmatch
from glob import glob
import io
from json import dumps
from os import chmod, unlink, symlink, makedirs
from os.path import join, dirname, basename, isdir, islink
import re
from shutil import copytree, rmtree
from tarfile import TarFile
from tempfile import mkdtemp

from sf import DEFAULT_ENCODING
from sf.solution import autodetect_solution, ExecutionException
from sf.testcases import TestCase, TestCases

from . import redis, LOGGER
import config

UID_TIMESTAMP_RE = re.compile( r'.*/(?P<uid>.+)/(?P<timestamp>[0-9]+)\.tar' )

def ts2iso(timestamp):
    return datetime.fromtimestamp(int(timestamp)/1000).isoformat()
#
# def json_dump(data, path):
#     with io.open(path, 'w', encoding = DEFAULT_ENCODING) as f: f.write(dumps(data, ensure_ascii = False, sort_keys = True, indent = 4))
#
def rmrotree(path):
    def _oe(f, p, e):
        if p == path: return
        pp = dirname(p)
        chmod(pp, 0700)
        chmod(p, 0700)
        unlink(p)
    rmtree(path, onerror = _oe)

class Uploads(object):

    def __init__(self, path, session_id):
        if not isdir(path): raise IOError('{} is not a directory'.format(path))
        LOGGER.info('Processing session {} uploads'.format(session_id))

        self.path = path
        self.session_id = session_id
        self.timestamps_key = 'timestamps:{}:{{}}'.format(session_id)

        for tf in glob(join(path, '*', '[0-9]*.tar')):
            m = UID_TIMESTAMP_RE.match(tf)
            if m:
                gd = m.groupdict()
                self.add(gd['uid'], gd['timestamp'])

    def _test(self, temp_dir, uid, timestamp, exercise):
        exercise_path = join(temp_dir, exercise)
        cases = config.cases(self.session_id, exercise)
        if cases is None:
            LOGGER.warn('Missing cases for {}'.format(exercise))
            return
        compile_case = TestCase('<COMPILE>')
        solution = autodetect_solution(exercise_path)
        if solution is None:
            compile_case.errors = u'Missing (or ambiguous) solution'
            LOGGER.warn('Missing (or ambiguous) solution for {}'.format(exercise))
        else:
            compilation_result = solution.compile()
            if compilation_result.returncode:
                compile_case.errors = compilation_result.stderr.decode(DEFAULT_ENCODING)
                LOGGER.warn( 'Failed to compile exercise {}'.format(exercise))
        result = [compile_case.to_dict()]
        if not compile_case.errors:
            LOGGER.info( 'Compiled solution for exercise {}'.format(exercise))
            num_cases = cases.fill_actual(solution)
            LOGGER.info( 'Run {} test cases for {}'.format(num_cases, exercise))
            redis.hset('results:{}:{}'.format(uid, timestamp), exercise, dumps(cases.to_list_of_dicts(('input', 'args', 'expected'))))

    def add(self, uid, timestamp):
        redis.zadd(self.timestamps_key.format(uid), timestamp, timestamp)
        temp_dir = mkdtemp(prefix = 'scythe-', dir = '/tmp' )
        LOGGER.info('Processing upload by uid {} at {} (in {})'.format(uid, ts2iso(timestamp), temp_dir))
        solutions = {}
        with TarFile.open(join(self.path, uid, timestamp + '.tar'), mode = 'r') as tf:
            try:
                tf.extractall(temp_dir)
            except IOError:
                LOGGER.error( 'Failed to untar upload for uid {} at timestamp {} ({})'.format(uid, timestamp, ts2iso(timestamp)))
                exercises = []
            for m in tf.getmembers():
                if m.isfile():
                    exercise_name = dirname(m.name)
                    file_name = basename(m.name)
                    exercise_solutions =  solutions.get(exercise_name, {})
                    solution = tf.extractfile(m).read().decode(DEFAULT_ENCODING)
                    exercise_solutions[file_name] = solution
                    solutions[exercise_name] = exercise_solutions
        solutions_key = 'solutions:{}:{}'.format(uid, timestamp)
        for exercise_name, exercise_solutions in solutions.items():
            redis.hset(solutions_key, exercise_name, exercise_solutions)
            LOGGER.info('Imported solutions for {}'.format(exercise_name))
            self._test(temp_dir, uid, timestamp, exercise_name)
        #rmrotree(temp_dir)


if __name__ == '__main__':
    Uploads('harvests/170613/uploads', '170613')
