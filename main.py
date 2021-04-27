import math
import random
from dbn import FireSpreadModel
from spread_prob import SpreadProbGrid
from utils import Timer, read_dbf, csv_to_ftp


def main():
    code_grid = read_dbf("data/Fueltype.dbf", mapper=int)
    dem = read_dbf("data/Dem.dbf", mapper=float)
    from_to_probs = csv_to_ftp("data/spread_prob_table.csv")

    height, width = code_grid.shape
    r = random.randrange(height)
    c = random.randrange(width)

    spread_prob_grid = SpreadProbGrid(
        code_grid=code_grid,
        from_to_probs=from_to_probs,
        dem=dem,
        wind_theta=3 * math.pi / 2,         # 서풍: 0, 남풍: math.pi/2, 동풍: pi, 북풍: 3*math.pi/2 (극좌표 형식)
        em=0.3,
        c1=0.045,
        c2=0.131,
        a=0.078,
        v=13,
        cell_size=30
    )

    model = FireSpreadModel(
        spread_prob_grid=spread_prob_grid,
        fire_coords=[(r, c)],               # 최초 발화 지점 (r행 c열)
        burn_down=True,                     # False: 전소 효과 없음
        burn_time=2,
        burn_threshold=0.7
    )

    with Timer('model.run()'):
        model.run(100)

    model.save(f"results/{r}_{c}_{model.t}.csv", fmt="%.4f")


if __name__ == "__main__":
    main()
