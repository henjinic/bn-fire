# bn-fire

## Requirements

* `pip install numpy`
* `pip install pandas`

## Usage
```py
>>> from dbn import FireSpreadModel
>>> import numpy as np
>>> model = FireSpreadModel(
...     code_grid=np.array([
...         [1, 1, 1, 1],
...         [1, 1, 1, 1],
...         [1, 1, 1, 1],
...         [1, 1, 1, 1]
...     ]),
...     from_to_probs={
...         1: {
...             1: 0.4
...         }
...     },
...     init_coords=[
...         (2, 1)
...     ]
... )
```
```py
>>> model.run(1)
>>> model.prob_grid
array([[0. , 0. , 0. , 0. ],
       [0. , 0.4, 0. , 0. ],
       [0.4, 1. , 0.4, 0. ],
       [0. , 0.4, 0. , 0. ]])

>>> model.run(1)
>>> model.prob_grid
array([[0.    , 0.16  , 0.    , 0.    ],
       [0.2944, 0.64  , 0.2944, 0.    ],
       [0.64  , 1.    , 0.64  , 0.16  ],
       [0.2944, 0.64  , 0.2944, 0.    ]])

>>> model.run(1)
>>> model.prob_grid
array([[0.17422336, 0.37504   , 0.17422336, 0.        ],
       [0.609425  , 0.73772805, 0.609425  , 0.17422336],
       [0.71979493, 1.        , 0.73772805, 0.37504   ],
       [0.609425  , 0.71979493, 0.609425  , 0.17422336]])

>>> model.t
3
```
```py
>>> model1 = FireSpreadModel(
...    ..., # same as above
...    burn_down=True
... )
>>> model1.run(10)
>>> model1.prob_grid
array([[0.92921432, 0.96677885, 0.97499918, 0.88709497],
       [0.97078053, 0.99298095, 0.99071377, 0.97499918],
       [0.97090482, 1.        , 0.99298095, 0.96677885],
       [0.91265688, 0.97090482, 0.97078053, 0.92921432]])

>>> model2 = FireSpreadModel(
...    ..., # same as above
...    burn_down=False
... )
>>> model2.run(10)
>>> model2.prob_grid
array([[0.99811222, 0.9998865 , 0.99975185, 0.99459267]
       [0.9999684 , 0.9999996 , 0.99999782, 0.99975185]
       [0.99999189, 1.        , 0.9999996 , 0.9998865 ]
       [0.99958082, 0.99999189, 0.9999684 , 0.99811222]])
```
```py
>>> model.save("results/file_name.csv")
```