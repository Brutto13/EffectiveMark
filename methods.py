import time
import multiprocessing as mp
from math import sin, cos, sqrt, log
import GPUtil
import pyopencl as cl
import numpy as np
import functools

GPU_ERROR: bool = False

platforms = cl.get_platforms()
_devices = None

for platform in platforms:
    try:
        _devices = platform.get_devices(device_type=cl.device_type.GPU)
        if _devices: break
    except:
        continue

# CPU-fallback
if not _devices:
    for platform in platforms:
        _devices = platform.get_devices(device_type=cl.device_type.CPU)
        if _devices:
            GPU_ERROR = True
            break

device = _devices[0]
ctx = cl.Context([device])
queue = cl.CommandQueue(ctx)

def force_gpu(func):
    def wrapper(*args, **kwargs):
        return func(ctx, queue, *args, **kwargs)
    return wrapper


def raw_cpu_benchmark(iterations: int) -> tuple[float, float]:
    scores: list[float] = []
    total: float = 0.0
    for _ in range(2):
        print(_)
        start = time.perf_counter()
        for i in range(int(iterations)):
            total += sin(cos(i)+sqrt(log(i+1)))
        end = time.perf_counter()
        elapsed = end-start
        score = round(iterations/(1000*elapsed), 1)
        scores.append(score)

    final_score = round(sum(scores)/len(scores), 1)
    return final_score, total


def cpu_benchmark(*, iterations=2e9, cores=1):
    ipc = iterations // cores

    start = time.perf_counter()
    with mp.Pool(processes=cores) as pool:
        pool.map(raw_cpu_benchmark, [ipc]*cores)
    end = time.perf_counter()

    elapsed = end-start

    score = round((iterations*cores)/((1000*elapsed)+1))
    return score


def get_opencl_device():
    for platform in cl.get_platforms():
        try:
            devs = platform.get_devices(device_type=cl.device_type.GPU)
            if devs:
                return platform, devs[0]
        except:
            pass
    for platform in cl.get_platforms():
        devs = platform.get_devices(device_type=cl.device_type.CPU)
        if devs:
            return platform, devs[0]
    raise RuntimeError("No OpenCL device found.")

# gpus = GPUtil.getGPUs()
# @force_gpu
# def add_arrays(ctx, queue, a_np, b_np):
#     assert a_np.shape == b_np.shape
#
#     size = a_np.size
#     mf = cl.mem_flags
#     a_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a_np)
#     b_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b_np)
#     c_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=c_np)
#     res_g = cl.Buffer(ctx, mf.WRITE_ONLY, a_np.nbytes)
#
#     program = cl.Program(ctx, """
#         __kernel void sum(__global const float *a,
#                           __global const float *b,
#                           __global float *res)
#         {
#             int gid = get_global_id(0);
#             res[gid] = a[gid] + b[gid];
#         }
#         """).build()
#
#     program.sum(queue, a_np.shape, None, a_g, b_g, res_g)
#
#     res_np = np.empty_like(a_np)
#     cl.enqueue_copy(queue, res_np, res_g)
#     return res_np


if __name__ == "__main__":
    # print(GPU_ERROR)
    # print(device)
    # a = np.random.rand(1024**2*64).astype(np.float32)
    # b = np.random.rand(1024**2*64).astype(np.float32)
    #
    #
    # result = add_arrays(a, b)
    # print(result)
    raw_cpu_benchmark(2e7)