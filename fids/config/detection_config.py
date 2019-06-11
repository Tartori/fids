class DetectionConfig:
    def __init__(self, config):
        keys = config.keys()
        self.filename_regex = config['filename_regex'] if 'filename_regex' in keys else ''
        self.same_config = config['same_config'] if 'same_config' in keys else True
        self.greater = config['greater'] if 'greater' in keys else []
        self.equal = config['equal'] if 'equal' in keys else []
