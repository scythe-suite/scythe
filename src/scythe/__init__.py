from logging import basicConfig, getLogger, DEBUG, INFO

from redis import StrictRedis

LOG_LEVEL = INFO
basicConfig(format = '%(asctime)s %(levelname)s: [%(funcName)s] %(message)s', datefmt = '%Y-%m-%d %H:%M:%S', level = LOG_LEVEL)
LOGGER = getLogger(__name__)

redis = StrictRedis(host = 'localhost', port = 6379, db = 0)
