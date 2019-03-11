from os import environ as env

import re
import yaml


def env_substitute(value):
    if isinstance(value, dict):
        result = {key: env_substitute(sub_value)
                  for (key, sub_value) in value.items()}
    elif isinstance(value, list):
        result = [env_substitute(sub_value) for sub_value in value]
    elif isinstance(value, str):
        result = value
        variables = re.findall("<%(.*?)%>", value)

        for variable in variables:
            result = result.replace("<%$$%>".replace(
                "$$", variable), env[variable.strip()])
    else:
        result = value

    return result


class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.environment = env.get("FLASK_ENV", "development")

        with open(config_file, "r") as config:
            config_contents = yaml.load(config)

            self.config = {key: env_substitute(value) for (
                key, value) in config_contents[self.environment].items()}

    def get(self, key):
        return self.config[key]
