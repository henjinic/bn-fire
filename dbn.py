import math
import numpy as np
from spread_prob import SpreadProbGrid
from utils import ProbCalc


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

    def __init__(self, spread_prob_grid, fire_coords,
                 burn_down=True, burn_time=2, burn_threshold=0.7):
        self._shape = spread_prob_grid.shape

        self._burn_down = burn_down
        self._burn_time = burn_time
        self._burn_threshold = burn_threshold

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
                self._dbn.next(self._fire_time_grid <= self._burn_time)
                self._update_fire_time_grid()
            else:
                self._dbn.next()

    def save(self, path, fmt="%.4f"):
        np.savetxt(path, self._dbn.prob_grid, fmt=fmt, delimiter=',')

    def _update_fire_time_grid(self):
        self._fire_time_grid[self._dbn.prob_grid >= self._burn_threshold] += 1

    def __str__(self):
        return self._dbn.__str__()


def main():

    # Example

    spread_prob_grid = SpreadProbGrid(
        code_grid=np.array([
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1]
        ]),
        from_to_probs={
            1: {
                1: 0.3
            }
        },
        dem=np.array([
            [60, 30, 0, 0],
            [60, 30, 0, 0],
            [60, 30, 0, 0],
            [60, 30, 0, 0]
        ]),
        wind_theta=math.pi / 2,
        em=0.3,
        c1=0.045,
        c2=0.131,
        a=0.078,
        v=13,
        cell_size=30
    )

    model = FireSpreadModel(
        spread_prob_grid=spread_prob_grid,
        fire_coords=[
            (2, 1),
        ],
        burn_down=True,
        burn_time=2,
        burn_threshold=0.7
    )

    np.set_printoptions(4, suppress=True)
    for _ in range(5):
        model.run(1)
        print("t:", model.t)
        print(model.prob_grid)


if __name__ == "__main__":
    main()
