from   configparser import ConfigParser, UNNAMED_SECTION
import json

config_file="~/.utilrc"

# init logging
logger = logging.getLogger(__name__)

def read_config(ctx, filename=config_file, ):
    cfg = ConfigParser()
    cfg.read(filename)
    try:
        options = dict(cfg['options'])
    except KeyError:
        options = {}
    ctx.default_map = options

class Config():
    def __init__(self, config_file):
        self.filename = config_file
        self.config = ConfigParser()
        self.config.read(config_file)
        self.default_section = UNNANED_SECTION

    def get_section(self, section=None):
        if section not in self.config:
            logger.DEBUG(f"Section {section} doesn't exist")            
            return None
        return self.config[section]

    def get_config(self, section=None, config):
        config_section = self.get_section(section)
        pass

    def set_section(self, section):
        pass

    def set_config(self, section, config):
        pass
