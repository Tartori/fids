import yaml
from config import ScanConfig, SqLiteDbConfig, RemoteDbConfig, InvestigatorConfig


class Config:
    def __init__(self, config_file='./config.yaml'):
        with open(config_file, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        print(cfg)
        keys = cfg.keys()
        self.scan_config = ScanConfig(cfg['scan']) if 'scan' in keys else None
        self.investigator_config = InvestigatorConfig(
            cfg['investigator']) if 'investigator' in keys else None
        if 'remote_db' in keys:
            self.db_config = RemoteDbConfig(cfg['remote_db'])
        elif 'sqlite' in keys:
            self.db_config = SqLiteDbConfig(cfg['sqlite'])

    def __repr__(self):
        return ("Config("
                f"scan_config={self.scan_config},"
                f"db_config={self.db_config},"
                f"investigator_config={self.investigator_config},"
                ")")
