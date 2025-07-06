# Effective Mark PC Benchmark

## Overview
Complete PC Benchmark written in Python 3.11 allows to run CPU, GPU and RAM
benchmark. Also measures connection speed.

## Download
There is no download site. To download application you will have to
use git clone command. Then build it with software like "PyInstaller",
also download all dependencies needed to build (see more in dependencies)

## Dependencies
Following dependencies are required to run in Python:
1) Textual
2) Moderngl (moderngl, moderngl_window)
3) psutil
4) speedtest (speedtest-cli)
5) cpuinfo (py-cpuinfo)
6) GPUtil (gputil)

## CPU Benchmark
### Overview
Classic CPU Benchmark. Measures time of performing CPU-heavy operations
like sines, cosines or logarithms. The returned score depends on time,
higher score means shorter time.

## GPU Benchmark
### Overview
Uses GPU to render 10k objects which use heavy calculations.
This test returns average FPS.

## RAM Benchmark
### Overview
This test uses RAM to allocate big list of numbers. Write test is test needed to
assign this variable while read test is measured as time that is needed to add all elements together,
so it's partially depends on CPU.

## HDD Benchmark
### Overview
This test generates 1GB-sized content and measures write and read time.
Then calculates read and write rates. 
WARNING: Most of the time takes content generation!