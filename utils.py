import dbfread
import numpy as np
import pandas as pd


def read_dbf(path, mapper=float):
    result = []

    for record in dbfread.DBF(path, load=True).records[6:]:
        result.append([mapper(value) for value in record.values() if value != ""])

    return np.array(result)


def read_grid(path):
    return np.loadtxt(path, delimiter=",", skiprows=6) # 파라미터 데이터 규격에 맞게 적절히 바꾸세요.


def csv_to_ftp(path):
    prob_df = pd.read_csv(path, index_col="neighbor")
    prob_df.columns = prob_df.columns.astype(int)

    result = {}

    for from_code in prob_df.columns:
        to_probs = {}
        column = prob_df[from_code]

        for to_code in column.index:
            to_probs[to_code] = column[to_code]

        result[from_code] = to_probs

    return result


def csv_to_grid(path):
    return np.loadtxt(path, delimiter=",")


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
