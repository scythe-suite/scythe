from base64 import decodestring
from fnmatch import fnmatch
import io
from json import dumps, loads
from os.path import join, basename, dirname
import re
from tarfile import TarFile

from sf import DEFAULT_ENCODING
from sf.testcases import TestCase, TestCases

from . import redis, LOGGER

MARKDOWN_GLOB = '*.md'
MARKDOWN_RE = re.compile(r'(.*)\.md')

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
        LOGGER.info('Imported uid {}'.format(uid))

    tar_data = io.BytesIO(decodestring(config['TAR_DATA']))
    cases = {}
    texts = {}
    with TarFile.open(mode = 'r', fileobj = tar_data) as tf:
        for m in tf.getmembers():
            if m.isfile():
                exercise_name = dirname(m.name)
                file_name = basename(m.name)

                exercise_cases = cases.get(exercise_name, {})
                for kind in TestCase.KINDS:
                    if fnmatch(file_name, TestCase.GLOBS[kind]):
                        case_name = TestCase.TEST_NUM_RE.match(file_name).group(1)
                        data = tf.extractfile(m).read().decode(DEFAULT_ENCODING)
                        tc = exercise_cases.get(case_name, TestCase(case_name))
                        if kind == 'args': data = TestCase.u2args(data)
                        setattr(tc, kind, data)
                        exercise_cases[case_name] = tc
                cases[exercise_name] = exercise_cases

                exercise_texts =  texts.get(exercise_name, {})
                if fnmatch(file_name, MARKDOWN_GLOB):
                    markdown_name = MARKDOWN_RE.match(file_name).group(1)
                    markdown = tf.extractfile(m).read().decode(DEFAULT_ENCODING)
                    exercise_texts[markdown_name] = markdown
                texts[exercise_name] = exercise_texts

    texts_key = 'texts:{}'.format(session_id)
    for exercise_name, exercise_texts in texts.items():
        list_of_texts = []
        for text_name, text in exercise_texts.items():
            list_of_texts.append({'name': text_name, 'content': text})
        redis.hset(texts_key, exercise_name, dumps(list_of_texts))
        LOGGER.info('Imported texts for exercise {}'.format(exercise_name))

    cases_key = 'cases:{}'.format(session_id)
    for exercise_name, exercise_cases in cases.items():
        list_of_cases = []
        for case_name, case in exercise_cases.items():
            dct = case.to_dict()
            for key in 'diffs', 'actual', 'errors': dct.pop(key, None)
            list_of_cases.append(dct)
        redis.hset(cases_key, exercise_name, dumps(list_of_cases))
        LOGGER.info('Imported cases for exercise {}'.format(exercise_name))


if __name__ == '__main__':
    toredis('confs/170613-t.py','170613')
    print cases('170613', '01-parole_graziose')
