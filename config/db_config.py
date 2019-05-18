import hashlib


class DbConfig:
    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.dbname = config['dbname']
        self.user = config['user']
        self.password = config['password']

    def __repr__(self):
        return ("DbConfig("
                f"host={self.host},"
                f"port={self.port},"
                f"dbname={self.dbname},"
                f"user={self.user},"
                f"password={hashlib.sha256(self.password.encode('utf-8')).hexdigest()})")
