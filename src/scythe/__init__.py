from base64 import decodestring
import io
from logging import basicConfig, getLogger, DEBUG, INFO
from os import chmod, unlink
from shutil import rmtree
from tarfile import TarFile
from tempfile import mkdtemp

from redis import StrictRedis

LOG_LEVEL = INFO
basicConfig(format = '%(asctime)s %(levelname)s: %(message)s', datefmt = '%Y-%m-%d %H:%M:%S', level = LOG_LEVEL)
LOGGER = getLogger(__name__)

VERSION = '0.1.0'

redis = StrictRedis(host = 'localhost', port = 6379, db = 0)

def rmrotree(path):
    def _oe(f, p, e):
        if p == path: return
        pp = dirname(p)
        chmod(pp, 0700)
        chmod(p, 0700)
        unlink(p)
    rmtree(path, onerror = _oe)

def tar2tmpdir(source, decode = False):
    if decode:
        fo = io.BytesIO(decodestring(source))
    else:
        fo = io.open(source, 'rb')
    temp_dir = mkdtemp(prefix = 'scythe-', dir = '/tmp' )
    with TarFile.open(mode = 'r', fileobj = fo) as tf:
        try:
            tf.extractall(temp_dir)
        except IOError:
            rmrotree(temp_dir)
            return None
    return temp_dir

"""
 SET	uids:<SESSION_ID> -> JSON({uid : <UID>, info : <INFO>, status: <STATUS>})
HASH	texts:<SESSION_ID> -> <EXERCISE_NAME>: JSON({name: <TEXT_NAME>, content: <MARKDOWN_TEXT>})
HASH	cases:<SESSION_ID> -> <EXERCISE_NAME>: JSON([{name: <CASE_NAME>, args: <ARGS>, input: <INPUT>, expected: <EXPECTED>}+])

ZSET	timestamps:<SESSION_ID>:<UID> -> TIMESTAMP

HASH	solutions:<UID>:<TIMESTAMP> -> <EXERCISE_NAME>: JSON([{content: <SOURCE_CODE>, name: <FILE_NAME>}+])
HASH	results:<UID>:<TIMESTAMP> -> <EXERCISE_NAME>: JSON([{name: <CASE_NAME>, diffs: <ARGS>, errors: <INPUT>}+])
HASH	compilations:<UID>:<TIMESTAMP> -> <EXERCISE_NAME>: <COMPILER_OUTPUT>

HASH	summary:<SESSION_ID> -> <UID>: JSON([{name: <EXERCISE_NAME>, compile: <BOOLEAN>: diffs: <NUM_DIFFS>, errors: <NUM_ERRORS>, …}+])
"""
