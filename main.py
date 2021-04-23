import random
from dbn import FireSpreadModel, csv_to_ftp, csv_to_grid
from utils import Timer


def main():
    code_grid = csv_to_grid("data/Italy_fueltype.csv")
    from_to_probs = csv_to_ftp("data/spread_prob_table.csv")

    height, width = code_grid.shape

    for i in range(10):
        r = random.randrange(height)
        c = random.randrange(width)

        with Timer(i):
            model = FireSpreadModel(
                code_grid,
                from_to_probs,
                [(r, c)]
            )
            model.run(10)
            model.save(f"results/{r}_{c}_{model.t}.csv")

if __name__ == "__main__":
    main()
