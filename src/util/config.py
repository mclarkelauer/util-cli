from util.logging import logger
import toml

from pathlib import Path
from collections import namedtuple

home = Path.home()
config_file = f"{home}/.utilrc"


class Config:
    global_config = None

    @staticmethod
    def init(config_file):
        Config.global_config = Config(config_file)

    @staticmethod
    def get_global_config():
        return Config.global_config

    @staticmethod
    def get_config_from_file(config_file):
        Config.init(config_file)
        return Config.get_global_config()

    @staticmethod
    def click_callback(ctx, param, filename):
        logger.debug(f"Config file loaded from{filename}")
        ctx.obj = Config.get_config_from_file(filename)

    def __init__(self, config_file):
        self.filename = config_file
        try:
            with open(self.filename, "r") as f:
                self.config = toml.load(f)
        except FileNotFoundError:
            self.config = {}

        print(self.config)
        self.default_section = "GLOBAL"
        if self.default_section not in self.config:
            self.config[self.default_section] = {}

    def __str__(self):
        return toml.dumps(self.config)

    def get_config(self, section=None, config=None):
        if section is None:
            section = self.default_section
        if section not in self.config:
            raise Exception(f"Section {section} not in config")
        if config not in self.config[section]:
            raise Exception(f"Section {section} doesn't contain {config}")
        return self.config[section][config]

    def set_config(self, section=None, config=None, value=None):
        if section is None:
            section = self.default_section
        elif section not in self.config:
            self.config[section] = dict()

        logger.debug(f"setting config: {section}:{config} to {value}")
        self.config[section][config] = value

    def set_section(self, section, config={}, overwrite=False):
        if section not in config:
            self.config[section] = {}
        for key in config.keys:
            if not overwrite and key in self.config[section]:
                logging.debug(
                    f"Key {key} exists in section {section} and overwrite is false, skipping"
                )
                continue
            else:
                self.config[section][key] = config[key]
