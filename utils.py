

class ProbCalc:
    import math

    @classmethod
    def union(cls, *args):
        return 1 - cls.math.prod(1 - prob for prob in args)


class Timer:
    import time

    def __init__(self, text):
        self._text = text
        self._start_time = self.time.time()
        print(f"{self._text} starts.")

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        print(f"... ends.", f"({round(self.time.time() - self._start_time, 2)} sec)")
