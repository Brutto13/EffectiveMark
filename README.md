# Effective Mark PC Benchmark

## Deprecation notices
Following functions will be deprecated in future release:
+ GPU Benchmarking
+ Internet SpeedTest

## Overview
Complete PC Benchmark written in Python 3.9 allows to run CPU, GPU and RAM
benchmark. Also measures connection speed.

## Download
There is no download site. To download application you will have to
use git clone command. Then build it with software like "PyInstaller",
also download all dependencies needed to build (see more in dependencies)
If you want to download stable release go to releases section of repository.

## Dependencies
Full dependencies list is available in
requirements.txt

## CPU Benchmark
### Overview
Classic CPU Benchmark. Measures time of performing CPU-heavy operations
like sines, cosines or logarithms. The returned score depends on time,
higher score means shorter time.

## GPU Benchmark (DEPRECATED)
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
**WARNING: Most of the time takes content generation!**