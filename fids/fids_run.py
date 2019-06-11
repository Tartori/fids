import pytsk3
import hashlib
import uuid
from datetime import datetime, timezone


class FidsRun:
    def __init__(
            self,
            config=None,
            id=None,
            start=None,
            finish=None,
            config_hash=None,
    ):
        if config is not None:
            self.id = uuid.uuid1().hex
            self.config_hash = hashlib.sha256(
                f'{config}'.encode('ascii')).hexdigest()
            self.start_time = self._get_now()
        else:
            self.set_everything(id, start, finish, config_hash)

    def set_everything(self, id, config_hash, start_time, finish_time):
        self.id = id
        self.config_hash = config_hash
        self.start_time = start_time
        self.finish_time = finish_time

    def finish_run(self):
        self.finish_time = self._get_now()

    def _get_now(self):
        now = datetime.now()
        return now.replace(tzinfo=timezone.utc).timestamp()
