from scaner import Scanner
from hids_file import HidsFile
from fids_error import FidsError
from config.config import Config
from db_connector.db import DatabaseWriter
from fids_run import FidsRun


class FIDS:
    def scan_system(self, config):
        db_writer = DatabaseWriter(config.db_config)
        run = FidsRun(config)

        db_writer.start_run(run)
        db_writer.commit()

        scanner = Scanner(scan_config=config.scan_config)
        scanner.scan()

        errors = scanner.errors
        for error in errors:
            db_writer.safe_error(error, run)
        db_writer.commit()
        errors = []
        files = scanner.files
        for file in files:
            try:
                db_writer.safe_file(file, run)
            except Exception as e:
                errors.append(FidsError(
                    description=f'Unknown Error Occured \'{e}\'', location=f'FIDS.scan_system.for(file=\'{file}\')'))
        db_writer.commit()

        for error in errors:
            db_writer.safe_error(error, run)
        db_writer.commit()
        run.finish_run()
        db_writer.finish_run(run)
        db_writer.commit()

    def evaluate_intrusions(self, config):
        pass


if __name__ == "__main__":
    config = Config()
    if config.scan_config is not None:
        FIDS().scan_system(config)
    if config.detection_config is not None:
        FIDS().evaluate_intrusions(config)
