import redis
import json
from datetime import datetime

from os import environ as env, getppid


class ErrorQueue:
    def __init__(self, options):
        self.__redis = None
        self.__options = options
        self.__ppid = env["WATSON_REDIS_KEY_FAMILY"]

    def push(self, parametrized_path, error_content):
        key = self.key_name("errors_out")
        payload = {
            'timestamp': datetime.now().isoformat(),
            'path': parametrized_path,
            'error': error_content
        }

        self.redis().lpush(key, json.dumps(payload))

    def key_name(self, name):
        result_name = "%s__%s" % (self.__ppid, name)
        return result_name

    def redis(self):
        if self.__redis is None:
            if self.__options.get("url", None):
                self.__redis = redis.from_url(self.__options["url"])
            else:
                self.__redis = redis.Redis(**self.__options)

        return self.__redis
