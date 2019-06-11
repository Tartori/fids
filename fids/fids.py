from fids import Scanner
from fids import HidsFile
from fids import FidsError
from fids.config import Config
from fids.db_connector import Database
from fids import FidsRun
from fids import DetectionError
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
        investigator_config = self.config.investigator_config
        investigator_config.prepare_investigations()
        runs = self.db.read_runs()
        sorted_runs = sorted(runs, key=attrgetter('finish_time'), reverse=True)
        if len(sorted_runs) < 2:
            return
        cur_run = sorted_runs[0]
        prev_run = sorted_runs[1]

        errors = []

        if investigator_config.same_config:
            if not cur_run.config_hash == prev_run.config_hash:
                errors.append(DetectionError(
                    "Config Hashes not equal even as they should be!!!", "high"))
        files = self.db.read_files_for_two_runs(cur_run.id, prev_run.id)
        for prev_file, cur_file in files:
            for investigation in investigator_config.investigations:
                if prev_file.path is None or prev_file.path == '' and not 'new_files_ok' in investigation.rules:
                    errors.append(DetectionError(
                        ('Found a new file!!!'
                         f'Path:\'{cur_file.path}\', filename: \'{cur_file.name_name}\', inode: \'{cur_file.meta_addr}\')'), "high"))
                    continue
                if cur_file.path is None or cur_file.path == '' and not 'deleted_files_ok' in investigation.rules:
                    errors.append(DetectionError(
                        ('Found a deleted file!!!'
                         f'Path:\'{prev_file.path}\', filename: \'{prev_file.name_name}\', inode: \'{prev_file.meta_addr}\')'), "high"))
                    continue
                if len(investigation.paths) >= 1 and (not prev_file.path == cur_file.path or not any(prev_file.path.startswith(path) for path in investigation.paths)):
                    continue
                if not investigation.fileregexwhitelist == '' and investigation.whitelist_negated == re.search(investigation.fileregexwhitelist, cur_file.name_name):
                    continue
                if investigation.fileregexblacklist and investigation.blacklist_negated != re.search(investigation.fileregexblacklist, cur_file.name_name):
                    errors.append(DetectionError(
                        ('FileName from blacklist actually found!!!'
                         f'Regex:\'{investigation.fileregexblacklist}\', filename: \'{cur_file.name_name}\')'), "high"))
                    continue
                for equal_attr in investigation.equal:
                    if not getattr(prev_file, equal_attr) == getattr(cur_file, equal_attr):
                        errors.append(DetectionError((
                            f'Attributes not equal even as they should be. '
                            f'File: \'{cur_file.name_name}\' Attribute \'{equal_attr}\' prev: \'{getattr(prev_file, equal_attr)}\' cur: \'{getattr(cur_file, equal_attr)}\'!!!'), "high"))
                for greater_attr in investigation.greater:
                    if not getattr(prev_file, greater_attr) <= getattr(cur_file, greater_attr):
                        errors.append(DetectionError(
                            f'Attributes not greater or equal even as they should be. '
                            f'\'{cur_file.name_name}\' Attribute \'{greater_attr}\' prev: \'{getattr(prev_file, greater_attr)}\' cur: \'{getattr(cur_file, greater_attr)}\'!!!', "high"))
        for error in errors:
            print(f'Found Error: {error}')
        print(f'Total of {len(errors)} Errors')


if __name__ == "__main__":
    config = Config()
    fids = FIDS(config)
    if config.scan_config is not None:
        fids.scan_system()
    if config.investigator_config is not None:
        fids.evaluate_intrusions()


# 18:41-1849
