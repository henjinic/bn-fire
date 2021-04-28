import math
import os
import random
from datetime import datetime
from dbn import FireSpreadModel
from spread_prob import SpreadProbGrid
from utils import Timer, read_dbf, csv_to_ftp


def cur_time():
    return datetime.strftime(datetime.today(), '%y%m%d-%H%M%S')


def get_model(r, c):
    code_grid = read_dbf("data/Fueltype.dbf", mapper=int)
    dem = read_dbf("data/Dem.dbf", mapper=float)
    from_to_probs = csv_to_ftp("data/spread_prob_table.csv")

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

    return model


def main():

    start_coord = (2, 2)
    end_coord = (3, 4)

    for r in range(start_coord[0], end_coord[0] + 1):
        for c in range(start_coord[1], end_coord[1] + 1):
            dir_name = f"{cur_time()}_{r}_{c}"

            os.mkdir(f"results/{dir_name}")

            model = get_model(r, c)

            with Timer(f"({r}, {c})"):
                for _ in range(5):
                    model.run(1)
                    model.save(f"results/{dir_name}/{model.t}.csv", fmt="%.4f")


if __name__ == "__main__":
    main()
