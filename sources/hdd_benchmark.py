import time
import os


def hdd_benchmark(size_gb=1):
    # Create File
    size: int = round(size_gb * (1024**3))
    content: str = "a"

    # Write Test
    try:
        with open("1gb-file", "x") as file:
            write_start = time.perf_counter()
            file.write(content*size)
            write_end = time.perf_counter()
    except PermissionError: return False, False  # Return Error Flag

    # Read Test
    try:
        with open("1gb-file", "r") as file:
            read_start = time.perf_counter()
            _ = file.read()
            read_end = time.perf_counter()
    except PermissionError: return False, False  # Return Error Flag

    os.remove("1gb-file")

    # Calculate times into transfer
    read_transfer = round((1024*size_gb)/(read_end-read_start), 1)    # Unit: MB/s
    write_transfer = round((1024*size_gb)/(write_end-write_start), 1)  # Unit: MB/s

    # Return Transfer Data
    return read_transfer, write_transfer


if __name__ == "__main__": print(hdd_benchmark(1))
