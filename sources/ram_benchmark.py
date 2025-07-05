import time

def ram_benchmark(size: int = 2e9):
    testlist = []
    writestart = time.perf_counter()
    for i in range(int(size)):
        testlist.append(7)
    writeend = time.perf_counter()
    writetime = writeend-writestart

    readstart = time.perf_counter()
    _ = sum(testlist)
    readend = time.perf_counter()

    readtime = readend-readstart

    return round((1e5/writetime)*(1e5/readstart), 1)