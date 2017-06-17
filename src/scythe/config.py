from glob import glob
import io
from json import dumps, loads
from os.path import join, basename, dirname, splitext

from sf import DEFAULT_ENCODING
from sf.testcases import TestCases

from . import redis, tar2tmpdir, rmrotree, LOGGER

TEXTS_GLOB = '*.md'

def cases(session_id, exercise):
    cases_key = 'cases:{}'.format(session_id)
    return TestCases.from_list_of_dicts(loads(redis.hget(cases_key, exercise)))

def toredis(path, session_id):

    config = {}
    with open(path, 'r') as f: exec(f, config)
    LOGGER.info('Read session {} configuration'.format(session_id))

    uids_key = 'uids:{}'.format(session_id)
    for uid, info in config['REGISTERED_UIDS'].items():
        redis.sadd(uids_key, dumps({'uid': uid, 'info': info, 'status': 'registered'}))
    LOGGER.info('Imported uids')

    temp_dir = tar2tmpdir(config['TAR_DATA'], decode = True)

    cases_key = 'cases:{}'.format(session_id)
    texts_key = 'texts:{}'.format(session_id)

    for exercise_path in glob(join(temp_dir, '*')):

        exercise_name = basename(exercise_path)
        list_of_cases = TestCases(exercise_path).to_list_of_dicts(('diffs', 'errors', 'actual'))
        if not list_of_cases:
            LOGGER.warn('Missing cases for {}'.format(exercise_name))
        else:
            redis.hset(cases_key, exercise_name, dumps(list_of_cases))
            LOGGER.info('Imported cases for exercise {}'.format(exercise_name))

        list_of_texts = []
        for text_path in glob(join(exercise_path, TEXTS_GLOB)):
            text_name = splitext(basename(text_path))[0]
            with io.open(text_path, 'r', encoding = DEFAULT_ENCODING) as tf: text = tf.read()
            list_of_texts.append({'name': text_name, 'content': text})
        if not list_of_texts:
            LOGGER.warn('Missing texts for {}'.format(exercise_name))
        else:
            redis.hset(texts_key, exercise_name, dumps(list_of_texts))
            LOGGER.info('Imported texts for exercise {}'.format(exercise_name))

    rmrotree(temp_dir)

if __name__ == '__main__':
    toredis('confs/170613-t.py','170613')
