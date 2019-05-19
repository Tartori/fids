class DetectionConfig:
    def __init__(self, config):
        keys = config.keys()
        self._parse_fixed_values(
            config['fixed_values'] if 'fixed_values' in keys else None)
        self._parse_compared_values(
            config['compared'] if 'compared' in keys else None)

    def _parse_fixed_values(self, fixed_values):
        if fixed_values is None:
            return

    def _parse_compared_values(self, compared):
        if compared is None:
            return
