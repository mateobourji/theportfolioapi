import redis
from backend.app.core.config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_SERVER
import logging

redis_logger = logging.getLogger("REDIS")


def setup_redis_cache():
    try:
        cache = redis.Redis(host=REDIS_HOST, password=REDIS_PASSWORD, port=REDIS_PORT, db=REDIS_SERVER)
        redis_logger.log(level=logging.INFO,
                         msg="Connecting to redis host %s on port %i" % (REDIS_HOST, REDIS_PORT))
    except Exception as e:
        redis_logger.log(level=logging.WARNING,
                         msg="Unable to connect to redis host %s on port %i" % (REDIS_HOST, REDIS_PORT))


def configure_redis_cache():
    return
