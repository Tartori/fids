from scaner import Scanner
from hids_file import HidsFile
from fids_error import FidsError
from config.config import Config
from db_connector.db import Database
from fids_run import FidsRun


class FIDS:
    def scan_system(self):
        config = Config()
        db = Database(config.db_config)
        run = FidsRun(config)

        db.start_run(run)
        db.commit()

        scanner = Scanner(fids_config=config.fids_config)
        scanner.scan()

        errors = scanner.errors
        for error in errors:
            db.safe_error(error, run)
        db.commit()
        errors = []
        files = scanner.files
        for file in files:
            try:
                db.safe_file(file, run)
            except Exception as e:
                errors.append(FidsError(
                    description=f'Unknown Error Occured \'{e}\'', location=f'FIDS.scan_system.for(file=\'{file}\')'))
        db.commit()

        for error in errors:
            db.safe_error(error, run)
        db.commit()
        run.finish_run()
        db.finish_run(run)
        db.commit()


if __name__ == "__main__":
    FIDS().scan_system()
