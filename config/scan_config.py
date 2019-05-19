class ScanConfig:
    def __init__(self, config):
        self.image_path = config['image_path']
        self.scan_paths = config['scan_paths']
        self.ignore_paths = config['ignore_paths']
        self.validate_mode = config['validate_mode']

    def __repr__(self):
        return ("FidsConfig("
                f"image_path={self.image_path},"
                f"scan_paths={self.scan_paths},"
                f"ignore_paths={self.ignore_paths},"
                f"validate_mode={self.validate_mode},)")
