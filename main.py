import random
from dbn import FireSpreadModel
from utils import Timer


def main():
    for i in range(10):
        r = random.randrange(140)
        c = random.randrange(117)
        with Timer(i):
            model = FireSpreadModel([(r, c)])
            model.run(50)
            model.save(f"results/{r}_{c}_{model.t}.csv")

if __name__ == "__main__":
    main()
