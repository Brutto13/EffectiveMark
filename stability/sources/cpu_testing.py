import os
import multiprocessing as mp
from math import *


def worker(stop, complexity: int = 150) -> None:
    result = []

    while not stop.is_set():
        for x in range(complexity):
            n = (log(abs(sin(x)-cos(x))+1)-sqrt(abs(sin(tan(complexity-x))+1)+1))**(1/complexity)-complexity**(7/(x+1))
            result.append(n)

        result.clear()


def multi_cpu(cores: int = -1) -> None:
    # Check if custom number of processes is set (cores=...)
    # otherwise set count of processes equal to number of CPU cores
    if cores == -1: cores = os.cpu_count()

    for _ in range(cores):
        proc = mp.Process(target=worker)
        proc.start()


if __name__ == '__main__':
    # print(get_cpu_temperature_from_dll())
    input()
