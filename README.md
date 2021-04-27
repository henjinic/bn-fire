# bn-fire

## Requirements

* `pip install numpy`
* `pip install pandas`

## Usage
```py
>>> import math
>>> import numpy as np
>>> from dbn import FireSpreadModel
>>> from spread_prob import SpreadProbGrid

>>> spread_prob_grid = SpreadProbGrid(
...     code_grid=np.array([
...         [1, 1, 1, 1],
...         [1, 1, 1, 1],
...         [1, 1, 1, 1],
...         [1, 1, 1, 1]
...     ]),
...     from_to_probs={
...         1: {
...             1: 0.7
...         }
...     },
...     dem=np.array([
...         [60, 30, 0, 0],
...         [60, 30, 0, 0],
...         [60, 30, 0, 0],
...         [60, 30, 0, 0]
...     ]),
...     wind_theta=math.pi / 2,
...     em=0.3,
...     c1=0.045,
...     c2=0.131,
...     a=0.078,
...     v=13,
...     cell_size=30
... )

>>> model = FireSpreadModel(
...     spread_prob_grid=spread_prob_grid,
...     fire_coords=[
...         (2, 1),
...     ],
...     burn_down=True,
...     burn_time=2,
...     burn_threshold=0.7
... )
```
```py
>>> model.run(5)
>>> model.t
5
>>> model.prob_grid
array([[1.59966691e-02, 1.26870940e-01, 1.79224924e-02, 6.79589589e-04],
       [5.82766160e-02, 2.68276094e-01, 6.52493211e-02, 4.27386948e-03],
       [6.22752267e-02, 1.00000000e+00, 7.00733918e-02, 7.99568608e-03],
       [2.73269917e-03, 1.28117503e-02, 3.06900512e-03, 1.94915687e-04]])
```
```py
>>> model.save("results/file_name.csv", fmt="%.4f")
```