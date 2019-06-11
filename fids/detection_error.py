class DetectionError:
    def __init__(self, message, level):
        self.message = message
        self.level = level

    def __str__(self):
        return (f'{self.level} Error Occured:'
                f'{self.message}')

    def __repr__(self):
        return ('DetectionError('
                f'message={self.message},'
                f'level={self.level},'
                ')')
