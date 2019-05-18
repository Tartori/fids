from scaner import Scanner
from hids_file import HidsFile
from config.config import Config
from db_connector.db import Database
from fids_run import FidsRun


class FIDS:
    def scan_system(self):
        config = Config()
        db = Database(config.db_config)
        run = FidsRun(config)

        db.start_run(run)
        scanner = Scanner(fids_config=config.fids_config)
        files = scanner.scan()
        print(files)
        for file in files:
            db.safe_file(file, run)
        run.finish_run()
        db.finish_run(run)
        db.commit()


if __name__ == "__main__":
    FIDS().scan_system()
