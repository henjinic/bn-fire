import itertools
import math
import numpy as np
import pomegranate as pg
import time


init_coords = [ # row, col
    (2, 1),
]

from_to_probs = {
    1: {
        1: 0.3,
        2: 0.375,
        3: 0.45,
        4: 0.225,
        5: 0.25,
        6: 0.075,
        7: 0
    },
    2: {
        1: 0.375,
        2: 0.375,
        3: 0.475,
        4: 0.325,
        5: 0.25,
        6: 0.1,
        7: 0
    },
    3: {
        1: 0.25,
        2: 0.35,
        3: 0.475,
        4: 0.25,
        5: 0.3,
        6: 0.075,
        7: 0
    },
    4: {
        1: 0.275,
        2: 0.4,
        3: 0.475,
        4: 0.35,
        5: 0.475,
        6: 0.275,
        7: 0
    },
    5: {
        1: 0.25,
        2: 0.3,
        3: 0.375,
        4: 0.2,
        5: 0.35,
        6: 0.075,
        7: 0
    },
    6: {
        1: 0.25,
        2: 0.375,
        3: 0.475,
        4: 0.35,
        5: 0.25,
        6: 0.075,
        7: 0
    },
    7: {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0
    }
}


class DBN:

    def __init__(self, code_grid, max_t):
        self._code_grid = code_grid
        self._height = self._code_grid.shape[0]
        self._width = self._code_grid.shape[1]
        self._size = self._code_grid.size

        self._max_t = max_t

        self._truth_table = TruthTable()

        self._model = pg.BayesianNetwork("dbn")

        self._t_raw_grids = {}
        self._t_node_grids = {}

        self._t_raw_grids[0] = self._get_empty_grid()
        self._t_node_grids[0] = self._get_empty_grid()

        # init t0 nodes
        for (r, c), _ in np.ndenumerate(self._t_raw_grids[0]):
            if (r, c) in init_coords:
                self._t_raw_grids[0][r, c] = pg.DiscreteDistribution({"T": 1, "F": 0})
            else:
                self._t_raw_grids[0][r, c] = pg.DiscreteDistribution({"T": 0, "F": 1})

            node = pg.Node(self._t_raw_grids[0][r, c], name=f"t0({r}, {c})")
            self._t_node_grids[0][r, c] = node
            self._model.add_state(node)

        # init t1 ~ tmax nodes and edges
        for t in range(1, self._max_t + 1):
            self._t_raw_grids[t] = self._get_empty_grid()
            self._t_node_grids[t] = self._get_empty_grid()

            for (r, c), _ in np.ndenumerate(self._t_raw_grids[t]):
                parents = [self._t_raw_grids[t - 1][r, c]]
                parent_nodes = [self._t_node_grids[t - 1][r, c]]
                probs = []

                for (dr, dc), direction in zip([(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)],
                                               ["down", "up", "right", "left"]):
                    if self._is_valid_coord(dr, dc):
                        parents.append(self._t_raw_grids[t - 1][dr, dc])
                        parent_nodes.append(self._t_node_grids[t - 1][dr, dc])
                        probs.append(from_to_probs[self._code_grid[dr, dc]][self._code_grid[r, c]])

                self._t_raw_grids[t][r, c] = pg.ConditionalProbabilityTable(self._truth_table.get(*probs), parents)
                node = pg.Node(self._t_raw_grids[t][r, c], name=f"t{t}({r}, {c})")
                self._t_node_grids[t][r, c] = node
                self._model.add_state(node)

                for parent_node in parent_nodes:
                    self._model.add_edge(parent_node, node)

        with Timer("baking"):
            self._model.bake()

    def predict(self):
        row = ["F"] * self._height * self._width
        row.extend([None] * self._height * self._width * self._max_t)

        for r, c in init_coords:
            row[r * self._width + c] = "T"

        with Timer("prediction"):
            nodes = self._model.predict_proba([row])[0]

        result = {}

        for t in range(1, self._max_t + 1):
            probs = [node.probability("T") for node in nodes[self._size * t: self._size * (t + 1)]]
            result[t] = np.array(probs)
            result[t] = result[t].reshape((self._height, self._width))

        return result

    def _is_valid_coord(self, r, c):
        if r < 0 or c < 0:
            return False

        if r >= self._height or c >= self._width:
            return False

        return True

    def _get_empty_grid(self):

        return np.empty((self._height, self._width), dtype=object)


class TruthTable: # [[self(t-1), ..., self(t)], ...]

    def __init__(self):
        self._cache = {}

    def get(self, *args):
        if args in self._cache:
            return self._cache[args]

        result = []
        for truths in itertools.product("TF", repeat=len(args) + 2):
            if truths[0] == "T" and truths[-1] == "F":
                result.append([*truths, 0])
            elif truths[0] == "T" and truths[-1] == "T":
                result.append([*truths, 1])
            elif all(True if truth == "F" else False for truth in truths[:-1]):
                result.append([*truths, 0 if truths[-1] == "T" else 1])
            else:
                indices = [i for i, truth in enumerate(truths[1: -1]) if truth == "T"]
                if len(indices) == 1:
                    prob = args[indices[0]]
                    result.append([*truths, prob if truths[-1] == "T" else 1 - prob])
                elif len(indices) >= 2:
                    prob = ProbCalculator.calc(*(args[idx] for idx in indices))
                    result.append([*truths, prob if truths[-1] == "T" else 1 - prob])

        self._cache[args] = result

        return result


class ProbCalculator:

    MIN_COUNT = 2
    MAX_COUNT = 5

    count_rank_pairs = {}
    for count in range(MIN_COUNT, MAX_COUNT + 1):
        count_rank_pairs[count] = {}

        for rank in range(1, count + 1):
            count_rank_pairs[count][rank] = list(itertools.combinations(range(count), rank))

    @classmethod
    def calc(cls, *args):
        result = 0
        sign = 1
        for rank in range(1, len(args) + 1):
            pairs = ProbCalculator.count_rank_pairs[len(args)][rank]
            result += sum(math.prod(map(lambda x: args[x], pair)) for pair in pairs) * sign
            sign *= -1

        return result


class Timer:

    def __init__(self, text):
        self._text = text
        self._start_time = time.time()
        print(f"{self._text} starts.")

    def __enter__(self):
        return

    def __exit__(self, type, value, traceback):
        print(f"{self._text} ends.", f"({round(time.time() - self._start_time, 2)} sec)")


def main():
    grid = np.loadtxt("data/Italy_fueltype.csv", delimiter=",")[:25, :25]

    dbn = DBN(grid, 5)

    result = dbn.predict()

    for t in result:
        np.savetxt(f"results/t{t}.csv", result[t], fmt="%.4f")

if __name__ == "__main__":
    main()
