import time
from math import *
from statistics import median


def raw_cpu_benchmark(iterations: int | float) -> tuple[float, float]:
    scores: list[float] = []
    total: float = 0.0
    for _ in range(5):
        start = time.perf_counter()
        for i in range(int(iterations)):
            total += sin(cos(i)+sqrt(log(i+1)))
        end = time.perf_counter()
        elapsed = end-start
        score = round(iterations/(1000*elapsed), 1)
        scores.append(score)

    final_score = round(median(scores))
    return final_score, total
