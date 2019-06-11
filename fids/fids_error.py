import uuid


class FidsError:
    def __init__(self, description, location):
        self.id = uuid.uuid1().hex
        self.description = description
        self.location = location

    def __repr__(self):
        return ('FidsError('
                f'id={self.id},'
                f'description={self.description},'
                f'location={self.location},'
                ')')
