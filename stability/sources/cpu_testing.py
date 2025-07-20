import os
import glob
import multiprocessing as mp
from math import *


def get_cpu_frequencies():
    freqs = {}
    cpu_paths = glob.glob('/sys/devices/system/cpu/cpu[0-9]*')
    for cpu_path in cpu_paths:
        cpu = os.path.basename(cpu_path)
        freq_file = os.path.join(cpu_path, 'cpufreq/scaling_cur_freq')
        try:
            with open(freq_file, 'r') as f:
                freq_khz = int(f.read().strip())
                freqs[cpu] = freq_khz / 1000.0  # MHz
        except FileNotFoundError:
            freqs[cpu] = None
    return freqs

def get_cpu_temperatures():
    temps = {}
    thermal_zones = glob.glob('/sys/class/thermal/thermal_zone*')
    for zone in thermal_zones:
        try:
            with open(os.path.join(zone, 'type'), 'r') as f:
                sensor_type = f.read().strip()
            with open(os.path.join(zone, 'temp'), 'r') as f:
                temp_milli = int(f.read().strip())
                temps[sensor_type] = temp_milli / 1000.0  # °C
        except (FileNotFoundError, ValueError):
            continue
    return temps


def worker(stop, complexity: int = 150) -> None:
    result = []

    while not stop.is_set():
        for x in range(complexity):
            n = (log(abs(sin(x)-cos(x))+1)-sqrt(abs(sin(tan(complexity-x))+1)+1))**(1/complexity)-complexity**(7/(x+1))
            result.append(n)
        x = sum(result)/len(result)
        # time.sleep(.01)
        # result.clear()
    result.clear()


def multi_cpu(cores: int = -1) -> None:
    # Check if custom number of processes is set (cores=...)
    # otherwise set count of processes equal to number of CPU cores
    if cores == -1: cores = os.cpu_count()

    for _ in range(cores):
        proc = mp.Process(target=worker)
        proc.start()
