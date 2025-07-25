"""Configuration management module."""
import asyncio
import logging
from pathlib import Path

import aiofiles
import toml

from util.logging import logger

home = Path.home()
CONFIG_FILE = f"{home}/.utilrc"

# Export the config_file for backwards compatibility  
# pylint: disable=invalid-name
config_file = CONFIG_FILE


class Config:
    """Configuration manager for the util package."""
    global_config = None

    @staticmethod
    def init(config_file_path):
        """Initialize global config with the given file path."""
        Config.global_config = Config(config_file_path)

    @staticmethod
    def get_global_config():
        """Get the global configuration instance."""
        return Config.global_config

    @staticmethod
    def get_config_from_file(config_file_path):
        """Get configuration from the specified file."""
        Config.init(config_file_path)
        return Config.get_global_config()
        
    @staticmethod
    async def get_config_from_file_async(config_file_path):
        """Get configuration from the specified file asynchronously."""
        config = Config(config_file_path)
        await config.load_config_async()
        Config.global_config = config
        return config

    @staticmethod
    def click_callback(ctx, _param, filename):
        """Click callback for loading configuration."""
        logger.debug("Config file loaded from %s", filename)
        config = Config(filename)
        # Load config synchronously for Click compatibility
        try:
            with open(filename, "r", encoding="utf-8") as f:
                config.config = toml.load(f)
        except FileNotFoundError:
            config.config = {}
        if config.default_section not in config.config:
            config.config[config.default_section] = {}
        ctx.obj = config

    def __init__(self, config_file_path):
        """Initialize configuration from file."""
        self.filename = config_file_path
        self.config = {}
        self.default_section = "GLOBAL"
        # Initialize synchronously for now, async init will be called separately
        
    async def load_config_async(self):
        """Load configuration from file asynchronously."""
        try:
            async with aiofiles.open(self.filename, "r", encoding="utf-8") as f:
                content = await f.read()
                self.config = toml.loads(content)
        except FileNotFoundError:
            self.config = {}

        print(self.config)
        if self.default_section not in self.config:
            self.config[self.default_section] = {}

    def __str__(self):
        return toml.dumps(self.config)

    def get_config(self, section=None, config=None):
        """Get configuration value from section."""
        if section is None:
            section = self.default_section
        if section not in self.config:
            raise KeyError(f"Section {section} not in config")
        if config not in self.config[section]:
            raise KeyError(f"Section {section} doesn't contain {config}")
        return self.config[section][config]

    def set_config(self, section=None, config=None, value=None):
        """Set configuration value in section."""
        if section is None:
            section = self.default_section
        elif section not in self.config:
            self.config[section] = {}

        logger.debug("setting config: %s:%s to %s", section, config, value)
        self.config[section][config] = value
        
    async def set_config_async(self, section=None, config=None, value=None):
        """Set configuration value in section asynchronously."""
        if section is None:
            section = self.default_section
        elif section not in self.config:
            self.config[section] = {}

        logger.debug("setting config: %s:%s to %s", section, config, value)
        self.config[section][config] = value

    def set_section(self, section, config=None, overwrite=False):
        """Set entire configuration section."""
        if config is None:
            config = {}
        if section not in self.config:
            self.config[section] = {}
        for key in config.keys():
            if not overwrite and key in self.config[section]:
                logging.debug(
                    "Key %s exists in section %s and overwrite is false, skipping",
                    key, section
                )
                continue
            self.config[section][key] = config[key]

    def get_gemini_apikey(self):
        """Get the Gemini API key from the GEMINI section"""
        try:
            return self.get_config(section="GEMINI", config="apikey")
        except KeyError:
            return None

    def set_gemini_apikey(self, apikey):
        """Set the Gemini API key in the GEMINI section"""
        self.set_config(section="GEMINI", config="apikey", value=apikey)

    def save_config(self):
        """Save the current configuration to file"""
        with open(self.filename, "w", encoding="utf-8") as f:
            toml.dump(self.config, f)
            
    async def save_config_async(self):
        """Save the current configuration to file asynchronously."""
        async with aiofiles.open(self.filename, "w", encoding="utf-8") as f:
            await f.write(toml.dumps(self.config))
