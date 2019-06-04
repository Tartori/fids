from scaner import Scanner
from hids_file import HidsFile
from fids_error import FidsError
from config import Config
from db_connector.db import Database
from fids_run import FidsRun
from detection_error import DetectionError
import re
from operator import attrgetter


class FIDS:
    def __init__(self, config):
        self.db = Database(config.db_config)
        self.config = config

    def scan_system(self):
        run = FidsRun(config)

        self.db.start_run(run)
        self.db.commit()

        scanner = Scanner(scan_config=config.scan_config)
        scanner.scan()
        print("scanner done, inserting")

        errors = scanner.errors
        for error in errors:
            self.db.safe_error(error, run)
        self.db.commit()
        errors = []
        files = scanner.files
        for file in files:
            try:
                self.db.safe_file(file, run)
            except Exception as e:
                errors.append(FidsError(
                    description=f'Unknown Error Occured \'{e}\'', location=f'FIDS.scan_system.for(file=\'{file}\')'))
        self.db.commit()

        for error in errors:
            self.db.safe_error(error, run)
        self.db.commit()
        run.finish_run()
        self.db.finish_run(run)
        self.db.commit()

    def evaluate_intrusions(self, cur_files=None):
        detection_config = self.config.detection_config
        runs = self.db.read_runs()
        sorted_runs = sorted(runs, key=attrgetter('finish_time'), reverse=True)
        cur_run = sorted_runs[0]
        prev_run = sorted_runs[1]
        if len(sorted_runs) < 2:
            return

        errors = []

        if detection_config.same_config:
            if not cur_run.config_hash == prev_run.config_hash:
                errors.append(DetectionError(
                    "Config Hashes not equal even as they should be!!!", "high"))
        # todo: nice python code, sucks at execution
        files = self.db.read_files_for_two_runs(cur_run.id, prev_run.id)
        for prev_file, cur_file in files:
            if detection_config.filename_regex and not re.search(detection_config.filename_regex, cur_file.name_name):
                errors.append(DetectionError(
                    ('FileName Regex does not match even as it should!!!'
                     'Regex:\'{detection_config.filename_regex}\', filename: \'{cur_file.name_name}\')'), "high"))
            for equal_attr in detection_config.equal:
                if not getattr(prev_file, equal_attr) == getattr(cur_file, equal_attr):
                    errors.append(DetectionError((
                        f'Attributes not equal even as they should be. '
                        f'File: \'{cur_file.name_name}\' Attribute \'{equal_attr}\' prev: \'{getattr(prev_file, equal_attr)}\' cur: \'{getattr(cur_file, equal_attr)}\'!!!'), "high"))
            for greater_attr in detection_config.greater:
                if not getattr(prev_file, greater_attr) <= getattr(cur_file, greater_attr):
                    errors.append(DetectionError(
                        f'Attributes not greater or equal even as they should be. '
                        f'\'{cur_file.name_name}\' Attribute \'{greater_attr}\' prev: \'{getattr(prev_file, greater_attr)}\' cur: \'{getattr(cur_file, greater_attr)}\'!!!', "high"))
        print(errors)


if __name__ == "__main__":
    config = Config()
    fids = FIDS(config)
    if config.scan_config is not None:
        fids.scan_system()
    if config.detection_config is not None:
        fids.evaluate_intrusions()
