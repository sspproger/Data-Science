#!/usr/bin/env python3
import sys
import time
import psutil

process = psutil.Process()
with open(sys.argv[1]) as f:
    lines = f.readlines()

start = time.time()
for line in lines:
    pass
end = time.time()

memory = process.memory_info().rss / (1024**3)  # в GB
cpu = process.cpu_times().user + process.cpu_times().system

print(f"Peak Memory Usage = {memory:.3f} GB")
print(f"User Mode Time + System Mode Time = {cpu:.2f}s")