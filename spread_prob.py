import math
import numpy as np


class SpreadProbGrid:

    def __init__(self, code_grid, from_to_probs, dem, wind_theta=3 * math.pi / 2,
                 em=0.3, c1=0.045, c2=0.131, a=0.078, v=13, cell_size=30):
        self._wind_theta = wind_theta # → (west wind): 0, ↑ (south wind): pi/2, ← (east wind): pi, ↓ (north wind): 3*pi/2
        self._em = em
        self._c1 = c1
        self._c2 = c2
        self._a = a # = as
        self._v = v
        self._cell_size = cell_size
        self._code_grid = code_grid
        self._from_to_probs = from_to_probs
        self._dem = dem

    @property
    def shape(self):
        return self._code_grid.shape

    def get_prob(self, from_coord, to_coord):
        theta = self._wind_theta - self._coord_to_theta(from_coord, to_coord)
        e_diff = self._dem[from_coord] - self._dem[to_coord]

        return (1 - (1 - self._pn(from_coord, to_coord)) ** self._awh(theta, e_diff)) * self._em

    def _coord_to_theta(self, from_coord, to_coord):
        fr, fc = from_coord
        tr, tc = to_coord

        if fr == tr and fc < tc: # →
            return 0
        elif fc == tc and fr > tr: # ↑
            return math.pi / 2
        elif fr == tr and fc > tc: # ←
            return math.pi
        elif fc == tc and fr < tr: # ↓
            return 3 * math.pi / 2
        else:
            raise Exception("invalid coords")

    def _pn(self, from_coord, to_coord):
        return self._from_to_probs[self._code_grid[from_coord]][self._code_grid[to_coord]]

    def _awh(self, theta, e_diff):
        return self._aw(theta) * self._ah(e_diff)

    def _aw2(self, theta): # for performance?
        return math.exp(self._v * (self._c1 + self._c2 * (math.cos(theta) - 1)))

    def _aw(self, theta): # = Pw
        return math.exp(self._c1 * self._v) * self._f(theta)

    def _f(self, theta):
        return math.exp(self._v * self._c2 * (math.cos(theta) - 1))

    def _ah(self, e_diff): # = Ps
        return math.exp(self._a * self._slope_angle(e_diff))

    def _slope_angle(self, e_diff):
        return math.atan(e_diff / self._cell_size)


def main():

    # Example

    spg = SpreadProbGrid(
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
        wind_theta=3 * math.pi / 2,
        em=0.3,
        c1=0.045,
        c2=0.131,
        a=0.078,
        v=13,
        cell_size=30
    )

    from_coord = (1, 1)
    r, c = from_coord
    for (dr, dc) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        to_coord = (r + dr, c + dc)
        print(from_coord, "->", to_coord, "prob:", spg.get_prob(from_coord, to_coord))


if __name__ == "__main__":
    main()
