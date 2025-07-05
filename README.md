# "EffectiveMark" PC Benchmark

## Description
This application is a complete PC benchmark running best on Windows 10, but it works also
on Windows 11. It offers CPU, RAM and GPU Benchmarking. It also offers internet speed measuring.
It's also planned to add more functions (like HDD/SSD benchmark or saving results into file)

## Branches
### main
main branch contains stable version of the application.
### experimental
experimental branch contains version it's being improved.
It can (and usually is) very unstable so it's not recommended to clone
from this branch

## Details
### CPU Benchmark
#### Description
This is a simple CPU benchmark. Runs ONE thread on CPU and measures time
The "score" of the CPU is related to time (shorter time means higher score).
Benchmark is ran 10 times to stabilize results.
#### Ranking Information
No data available now

### RAM Benchmark
#### Description
Little more complex than CPU benchmark. Tests both read and write requests
to RAM. Write request is tested by allocating big list of integers into RAM. Read
is measured as time needed to sum all it's content.
#### Ranking Information
No data available

### GPU Benchmark
#### Description
Classic GPU Render test. Requests GPU to render around 10k of triangles ordered as
simple yellow rectangle. It pushes GPU usage of "3D core" up to 100%.
#### Ranking information
Not available
