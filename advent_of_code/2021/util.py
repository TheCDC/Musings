import time


class AdventTimer:
    def __init__(self):
        self.ti = time.time()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return self

    @property
    def duration(self):
        return time.time() - self.ti
