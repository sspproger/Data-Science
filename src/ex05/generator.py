#!/usr/bin/env python3
import sys
import time
import psutil

process = psutil.Process()

def read_lines(filename):
    with open(filename) as f:
        for line in f:
            yield line

start = time.time()
for line in read_lines(sys.argv[1]):
    pass
end = time.time()

memory = process.memory_info().rss / (1024**3)
cpu = process.cpu_times().user + process.cpu_times().system

print(f"Peak Memory Usage = {memory:.3f} GB")
print(f"User Mode Time + System Mode Time = {cpu:.2f}s")