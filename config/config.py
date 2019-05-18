import yaml
from config.fids_config import FidsConfig
from config.db_config import DbConfig


class Config:
    def __init__(self, config_file='./config.yaml'):
        with open(config_file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        print(cfg)
        self.fids_config = FidsConfig(cfg['fids'])
        self.db_config = DbConfig(cfg['db'])

    def __repr__(self):
        return ("Config("
                f"fids_config={self.fids_config},"
                f"db_config={self.db_config}")
