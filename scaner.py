import pytsk3
from hids_file import HidsFile
from config.fids_config import FidsConfig


class Scanner:

    def __init__(self, fids_config):
        self.img_path = fids_config.image_path
        self.paths = fids_config.scan_paths
        self.fids_config = fids_config

    def scan(self):
        self.files = []
        img_info = pytsk3.Img_Info(self.img_path)
        self.fs_info = pytsk3.FS_Info(img_info, offset=0)
        self.fs_info.info
        for path in self.paths:
            self.open_directory_rec(path)
        return self.files

    def open_directory_rec(self, path):
        try:
            curDir = self.fs_info.open_dir(path)
        except:
            print("exception!")
            return
        for element in curDir:
            if element.info.name.type == pytsk3.TSK_FS_NAME_TYPE_DIR:
                print("directory!")
                if(not element.info.name.name == b'.' and not element.info.name.name == b'..'):
                    print("valid directory")
                    self.open_directory_rec(
                        path + element.info.name.name.decode("ascii") + "/")
            elif element.info.name.type == pytsk3.TSK_FS_NAME_TYPE_REG:
                print("I'm a file")
                hids_file = HidsFile(path=path)
                hids_file.parse_tsk_file(element)
                self.files.append(hids_file)


if __name__ == "__main__":
    from pprint import pprint
