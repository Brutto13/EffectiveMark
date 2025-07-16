import os
import sys
import clr
import multiprocessing as mp
from math import *


def try_fetch_dll():
    try:
        dll_path = R"C:\Users\DeLl1\Desktop\EffectiveMark\LibreHardwareMonitorLib.dll"
        if not os.path.exists(dll_path):
            print(f"Missing DLL: {dll_path}")
            return None

        sys.path.append(os.path.dirname(dll_path))
        clr.AddReference(dll_path)
        from LibreHardwareMonitor import Hardware

        return True
    except Exception as error:
        print(error)
        return False


def get_cpu_temperature_from_dll() -> float | None:
    try:
        # Update the path to where OpenHardwareMonitorLib.dll is located
        dll_path = r"C:\Users\DeLl1\Desktop\EffectiveMark\LibreHardwareMonitorLib.dll"
        if not os.path.exists(dll_path):
            print(f"Missing DLL: {dll_path}")
            return None

        sys.path.append(os.path.dirname(dll_path))
        clr.AddReference(dll_path)

        from LibreHardwareMonitor import Hardware

        computer = Hardware.Computer()
        # computer.MainboardEnabled = False
        computer.CPUEnabled = True
        # computer.GPUEnabled = False
        # computer.RAMEnabled = False
        # computer.FanControllerEnabled = False
        # computer.HDDEnabled = False
        computer.Open()

        temps = []
        for hardware in computer.Hardware:
            if hardware.HardwareType == Hardware.HardwareType.CPU:
                hardware.Update()
                for sensor in hardware.Sensors:
                    if sensor.SensorType == Hardware.SensorType.Temperature:
                        if sensor.Value is not None:
                            temps.append(sensor.Value)

        computer.Close()
        if temps:
            return round(max(temps))
        else:
            return 0

    except Exception as error:
        print(f"[OpenHardwareMonitor DLL Error] {error}")
        return 0


def worker(stop, complexity: int = 150) -> None:
    result = []

    while not stop.is_set():
        for x in range(complexity):
            n = (log(abs(sin(x)-cos(x))+1)-sqrt(abs(sin(tan(complexity-x))+1)+1))**(1/complexity)-complexity**(7/(x+1))
            result.append(n)
        x = sum(result)/len(result)
        # result.clear()
    result.clear()


def multi_cpu(cores: int = -1) -> None:
    # Check if custom number of processes is set (cores=...)
    # otherwise set count of processes equal to number of CPU cores
    if cores == -1: cores = os.cpu_count()

    for _ in range(cores):
        proc = mp.Process(target=worker)
        proc.start()


if __name__ == '__main__':
    print(get_cpu_temperature_from_dll())
    input()
