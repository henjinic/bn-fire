# bn-fire

## Requirements

* `pip install pomegranate`

## Funtions

### `ProbCalculator.calc(*args)`
* Description
  * p<sub>1</sub> ∪ p<sub>2</sub> ∪ ... ∪ p<sub>n</sub>을 구하는 함수
* Parameters
  * 구하고자 하는 확률들 (p<sub>1</sub>, p<sub>2</sub>, ..., p<sub>n</sub>)
* Return
  * ~~p<sub>1</sub> + ... + p<sub>n</sub> - (p<sub>1</sub> * p<sub>2</sub> + ... p<sub>n-1</sub> * p<sub>n</sub>) + (p<sub>1</sub> * p<sub>2</sub> * p<sub>3</sub> + ... p<sub>n-2</sub> * p<sub>n-1</sub> * p<sub>n</sub>) - ...~~
  * 1 - (1 - p<sub>1</sub>)(1 - p<sub>2</sub>)...(1 - p<sub>n</sub>)
* Example
```py
>>> ProbCalculator.calc(0.25)
0.25
>>> ProbCalculator.calc(0.4, 0.7)
0.82
>>> ProbCalculator.calc(0.1, 0.15, 0.3)
0.4645
```

### `TruthTable.get(*args)`
* Description
  * 베이지안 네트워크 노드 생성에 필요한 조건부 확률 표 생성
* Parameters
  * 모든 부모 노드로부터의 확률 (동일 위치의 노드 제외)
  * 즉, Node<sub>r,c</sub>(t)의 조건부 확률 표를 구하고자 할 때
    * Node<sub>r-1,c</sub>(t-1) -> Node<sub>r,c</sub>(t))
    * Node<sub>r+1,c</sub>(t-1) -> Node<sub>r,c</sub>(t)
    * Node<sub>r,c-1</sub>(t-1) -> Node<sub>r,c</sub>(t)
    * Node<sub>r,c+1</sub>(t-1) -> Node<sub>r,c</sub>(t)
  * 이 확률들을 넣는다. (Node<sub>r,c</sub>(t-1)로부터의 확률은 넣지 않는다.)
* Return
  * 첫 번째 열에는 동일 위치 부모 노드의 진리값,
  * 두 번째 ~ N-2 번째 열에는 인접 위치 부모 노드들의 진리값,
  * N-1 번째 열에는 구하고자 하는 노드의 진리값,
  * 마지막(N) 열에는 확률이 나온다.
* Example
```py
>>> tt = TruthTable()
>>> tt.get(0.25)

[['T', 'T', 'T', 1],
['T', 'T', 'F', 0],
['T', 'F', 'T', 1],
['T', 'F', 'F', 0],
['F', 'T', 'T', 0.25],
['F', 'T', 'F', 0.75],
['F', 'F', 'T', 0],
['F', 'F', 'F', 1]]

>>> tt.get(0.4, 0.7)

[['T', 'T', 'T', 'T', 1],
['T', 'T', 'T', 'F', 0],
['T', 'T', 'F', 'T', 1],
['T', 'T', 'F', 'F', 0],
['T', 'F', 'T', 'T', 1],
['T', 'F', 'T', 'F', 0],
['T', 'F', 'F', 'T', 1],
['T', 'F', 'F', 'F', 0],
['F', 'T', 'T', 'T', 0.82],
['F', 'T', 'T', 'F', 0.18],
['F', 'T', 'F', 'T', 0.4],
['F', 'T', 'F', 'F', 0.6],
['F', 'F', 'T', 'T', 0.7],
['F', 'F', 'T', 'F', 0.3],
['F', 'F', 'F', 'T', 0],
['F', 'F', 'F', 'F', 1]]

>>> tt.get(0.1, 0.15, 0.3)

[['T', 'T', 'T', 'T', 'T', 1],
['T', 'T', 'T', 'T', 'F', 0],
['T', 'T', 'T', 'F', 'T', 1],
['T', 'T', 'T', 'F', 'F', 0],
['T', 'T', 'F', 'T', 'T', 1],
['T', 'T', 'F', 'T', 'F', 0],
['T', 'T', 'F', 'F', 'T', 1],
['T', 'T', 'F', 'F', 'F', 0],
['T', 'F', 'T', 'T', 'T', 1],
['T', 'F', 'T', 'T', 'F', 0],
['T', 'F', 'T', 'F', 'T', 1],
['T', 'F', 'T', 'F', 'F', 0],
['T', 'F', 'F', 'T', 'T', 1],
['T', 'F', 'F', 'T', 'F', 0],
['T', 'F', 'F', 'F', 'T', 1],
['T', 'F', 'F', 'F', 'F', 0],
['F', 'T', 'T', 'T', 'T', 0.4645],
['F', 'T', 'T', 'T', 'F', 0.5355],
['F', 'T', 'T', 'F', 'T', 0.235],
['F', 'T', 'T', 'F', 'F', 0.765],
['F', 'T', 'F', 'T', 'T', 0.37],
['F', 'T', 'F', 'T', 'F', 0.63],
['F', 'T', 'F', 'F', 'T', 0.1],
['F', 'T', 'F', 'F', 'F', 0.9],
['F', 'F', 'T', 'T', 'T', 0.405],
['F', 'F', 'T', 'T', 'F', 0.595],
['F', 'F', 'T', 'F', 'T', 0.15],
['F', 'F', 'T', 'F', 'F', 0.85],
['F', 'F', 'F', 'T', 'T', 0.3],
['F', 'F', 'F', 'T', 'F', 0.7],
['F', 'F', 'F', 'F', 'T', 0],
['F', 'F', 'F', 'F', 'F', 1]]
```