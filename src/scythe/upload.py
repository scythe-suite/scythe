from datetime import datetime
from glob import glob
import io
from logging import getLogger
from json import dumps, loads
from os.path import join, basename, isdir
import re

from rq.decorators import job

from sf import DEFAULT_ENCODING
from sf.solution import autodetect_solution
from sf.testcases import TestCases

from . import redis, tar2tmpdir, rmrotree

LOGGER = getLogger(__name__)

def ts2iso(timestamp):
    return datetime.fromtimestamp(int(timestamp)/1000).isoformat()

@job('default', connection = redis)
def process(path, session_id, uid, timestamp, clean = False):

    timestamps_key = 'timestamps:{}:{}'.format(session_id, uid)
    solutions_key = 'solutions:{}:{}'.format(uid, timestamp)
    compilations_key = 'compilations:{}:{}'.format(uid, timestamp)
    results_key = 'results:{}:{}'.format(uid, timestamp)

    if not clean and redis.zscore(timestamps_key, timestamp):
        LOGGER.info('Skipping upload by uid {} at {}'.format(uid, ts2iso(timestamp)))
        return

    if clean:
        LOGGER.info('Cleaning upload by uid {} at {}'.format(uid, ts2iso(timestamp)))
        for key in timestamps_key, solutions_key, compilations_key, results_key:
            redis.delete(key)

    temp_dir = tar2tmpdir(join(path, uid, timestamp + '.tar'))
    LOGGER.info('Processing upload by uid {} at {} (in {})'.format(uid, ts2iso(timestamp), temp_dir))

    for exercise_path in glob(join(temp_dir, '*')):
        exercise_name = basename(exercise_path)

        solution = autodetect_solution(exercise_path)
        if solution.sources is None:
            LOGGER.warn('No solutions found for exercise {}'.format(exercise_name))
            continue
        list_of_solutions = []
        for solution_name in solution.sources:
            solution_path = join(exercise_path, solution_name)
            with io.open(solution_path, 'r', encoding = DEFAULT_ENCODING) as tf: solution_content = tf.read()
            list_of_solutions.append({'name': solution_name, 'content': solution_content})
        redis.hset(solutions_key, exercise_name, dumps(list_of_solutions))
        LOGGER.info('Imported solutions for exercise {}'.format(exercise_name))

        compiler_message = ''
        if solution.main_source is None:
            compiler_message = u'Missing (or ambiguous) solution'
            LOGGER.warn('Missing (or ambiguous) solution for {}'.format(exercise_name))
        compilation_result = solution.compile()
        if compilation_result.returncode:
            compiler_message = compilation_result.stderr.decode(DEFAULT_ENCODING)
            LOGGER.warn( 'Failed to compile exercise {}'.format(exercise_name))
        redis.hset(compilations_key, exercise_name, compiler_message)

        if compiler_message: continue
        LOGGER.info( 'Compiled solution for exercise {}'.format(exercise_name))
        cases_key = 'cases:{}'.format(session_id)
        cases = TestCases.from_list_of_dicts(loads(redis.hget(cases_key, exercise_name)))
        num_cases = cases.fill_actual(solution)
        LOGGER.info( 'Run {} test cases for {}'.format(num_cases, exercise_name))
        redis.hset(results_key, exercise_name, dumps(cases.to_list_of_dicts(('input', 'args', 'expected'))))

    rmrotree(temp_dir)
    redis.zadd(timestamps_key, timestamp, timestamp)

def scan(path, session_id, clean = False):
    if not isdir(path): raise IOError('{} is not a directory'.format(path))
    LOGGER.info('Processing session {} uploads'.format(session_id))
    UID_TIMESTAMP_RE = re.compile( r'.*/(?P<uid>.+)/(?P<timestamp>[0-9]+)\.tar' )

    for tf in glob(join(path, '*', '[0-9]*.tar')):
        m = UID_TIMESTAMP_RE.match(tf)
        if m:
            gd = m.groupdict()
            process.delay(path, session_id, gd['uid'], gd['timestamp'], clean)
            LOGGER.info('Enqueued upload by uid {} at {}'.format(gd['uid'], ts2iso(gd['timestamp'])))
