import numpy as np
import pandas as pd
from utils import ProbCalc


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


class SpreadProbGrid:

    def __init__(self, code_grid, from_to_probs):
        self._code_grid = code_grid
        self._from_to_probs = from_to_probs

    def get_prob(self, from_coord, to_coord):
        return self._from_to_probs[self._code_grid[from_coord]][self._code_grid[to_coord]]


class DBN:

    def __init__(self, initial_prob_grid, spread_prob_grid):
        self._prob_grid = initial_prob_grid
        self._spread_prob_grid = spread_prob_grid
        self._t = 0

    @property
    def prob_grid(self):
        return self._prob_grid.copy()

    @property
    def t(self):
        return self._t

    def next(self, mask=None):
        new_prob_grid = np.zeros(self._prob_grid.shape)

        for (r, c), prob in np.ndenumerate(self._prob_grid):
            probs = self._get_adjacent_probs(r, c, mask)
            probs.append(prob)
            new_prob_grid[r, c] = ProbCalc.union(*probs)

        self._t += 1

        self._prob_grid = new_prob_grid

        return self._prob_grid

    def _get_adjacent_probs(self, r, c, mask):
        result = []

        for ar, ac in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if not self._is_valid_coord((ar, ac)):
                continue

            if (mask is not None) and not (mask[ar, ac]):
                continue

            prob = self._spread_prob_grid.get_prob((ar, ac), (r, c)) * self._prob_grid[ar, ac]

            result.append(prob)

        return result

    def _is_valid_coord(self, coord):
        if coord[0] < 0 or coord[1] < 0:
            return False

        if coord[0] >= self._prob_grid.shape[0] or coord[1] >= self._prob_grid.shape[1]:
            return False

        return True

    def __str__(self):
        return self._prob_grid.__str__()


class FireSpreadModel:

    BURNDOWN_TIME = 2
    BURN_THRESHOLD = 0.7

    def __init__(self, code_grid, from_to_probs, fire_coords, burn_down=True):
        self._shape = code_grid.shape

        spread_prob_grid = SpreadProbGrid(code_grid, from_to_probs)

        self._burn_down = burn_down

        self._fire_time_grid = np.zeros(self._shape)

        initial_prob_grid = np.zeros(self._shape)

        for coord in fire_coords:
            initial_prob_grid[coord] = 1

        self._dbn = DBN(initial_prob_grid, spread_prob_grid)

        if self._burn_down:
            self._update_fire_time_grid()

    @property
    def t(self):
        return self._dbn.t

    @property
    def prob_grid(self):
        return self._dbn.prob_grid

    def run(self, t):
        for _ in range(t):
            if self._burn_down:
                self._dbn.next(self._fire_time_grid <= FireSpreadModel.BURNDOWN_TIME)
                self._update_fire_time_grid()
            else:
                self._dbn.next()

    def save(self, path, fmt="%.4f"):
        np.savetxt(path, self._dbn.prob_grid, fmt=fmt, delimiter=',')

    def _update_fire_time_grid(self):
        self._fire_time_grid[self._dbn.prob_grid >= FireSpreadModel.BURN_THRESHOLD] += 1

    def __str__(self):
        return self._dbn.__str__()

def main():
    model = FireSpreadModel(
        code_grid=np.array([
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1]
        ]),
        from_to_probs={
            1: {
                1: 0.5
            }
        },
        fire_coords=[
            (2, 1),
        ],
        burn_down=True
    )

    for _ in range(10):
        model.run(1)
        print(model.prob_grid)


if __name__ == "__main__":
    main()
