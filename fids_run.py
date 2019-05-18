import pytsk3
import hashlib
import uuid
from datetime import datetime, timezone


class FidsRun:
    def __init__(
            self,
            config
    ):
        self.id = uuid.uuid1().hex
        self.config_hash = hashlib.sha256(
            f'{config}'.encode('ascii')).hexdigest()
        self.start_time = self._get_now()

    def finish_run(self):
        self.finish_time = self._get_now()

    def _get_now(self):
        now = datetime.now()
        return now.replace(tzinfo=timezone.utc).timestamp()
