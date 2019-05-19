class ScanConfig:
    def __init__(self, config):
        keys = config.keys()
        self.image_path = config['image_path'] if 'image_path' in keys else ''
        self.scan_paths = config['scan_paths'] if 'scan_paths' in keys else [
            '/']
        self.ignore_paths = config['ignore_paths'] if 'ignore_paths' in keys else [
        ]
        self.validate_mode = config['validate_mode'] if 'validate_mode' in keys else False

    def __repr__(self):
        return ("FidsConfig("
                f"image_path={self.image_path},"
                f"scan_paths={self.scan_paths},"
                f"ignore_paths={self.ignore_paths},"
                f"validate_mode={self.validate_mode},)")
