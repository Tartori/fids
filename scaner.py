import pytsk3
from hids_file import HidsFile
from fids_error import FidsError


class Scanner:

    def __init__(self, scan_config):
        self.img_path = scan_config.image_path
        self.offset = scan_config.offset
        self.paths = scan_config.scan_paths
        self.ignore_paths = scan_config.ignore_paths
        self.scan_config = scan_config

    def scan(self):
        self.files = []
        self.errors = []
        img_info = pytsk3.Img_Info(self.img_path)
        self.fs_info = pytsk3.FS_Info(img_info, offset=self.offset)
        self.stack = []
        for path in self.paths:
            print(f'start scan for path \'{path}\'')
            try:
                self.open_directory_rec(path, self.fs_info.open_dir(path))
            except:
                self.errors.append(FidsError(
                    description=f'could not open path \'{path}\'', location="Scanner.open_directory_rec"))
        print("Scan Done")

    def open_directory_rec(self, path, curDir):
        self.stack.append(curDir.info.fs_file.meta.addr)
        try:
            if path in self.ignore_paths:
                return

            for directory_entry in curDir:
                if(not hasattr(directory_entry, "info") or
                   not hasattr(directory_entry.info, "name") or
                   not hasattr(directory_entry.info.name, "name") or
                   directory_entry.info.name.name in [b".", b".."]):
                    continue
                if directory_entry.info.name.type == pytsk3.TSK_FS_NAME_TYPE_DIR:
                    sub_directory = directory_entry.as_directory()
                    inode = directory_entry.info.meta.addr
                    # This ensures that we don't recurse into a directory
                    # above the current level and thus avoid circular loops.
                    dirname = directory_entry.info.name.name.decode('utf8')
                    if inode not in self.stack:
                        self.open_directory_rec(
                            (f'{path}'
                             f'{dirname}/'),
                            sub_directory)
                elif directory_entry.info.name.type == pytsk3.TSK_FS_NAME_TYPE_REG:
                    hids_file = HidsFile(path=path)
                    hids_file.parse_tsk_file(directory_entry)
                    self.files.append(hids_file)
                    if hids_file.name_name == 'FileToBeDeletedWithVeryAppropropriateNameToFindIt.txt':
                        print(hids_file)
        except Exception as e:
            self.errors.append(
                FidsError(
                    description=f'Unknown Error Occured \'{e}\'', location=f'Scanner.open_directory_rec(path=\'{path}\')'))


if __name__ == "__main__":
    from pprint import pprint


# 17:57 - 17:59
