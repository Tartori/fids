import hashlib


class SqLiteDbConfig:
    def __init__(self, config):
        keys = config.keys()
        self.type = 'SqLite'
        self.filename = config['filename'] if 'filename' in keys else 'fids_db.db'

    def __repr__(self):
        return ("SqLiteDbConfig("
                f"filename={self.filename},)")


class RemoteDbConfig:
    def __init__(self, config):
        keys = config.keys()
        self.type = 'Remote'
        self.host = config['host'] if 'host' in keys else ""
        self.port = config['port'] if 'port' in keys else ""
        self.dbname = config['dbname'] if 'dbname' in keys else ""
        self.user = config['user'] if 'user' in keys else ""
        self.password = config['password'] if 'password' in keys else ""

    def __repr__(self):
        return ("RemoteDbConfig("
                f"host={self.host},"
                f"port={self.port},"
                f"dbname={self.dbname},"
                f"user={self.user},"
                f"password={hashlib.sha256(self.password.encode('utf-8')).hexdigest()})")
