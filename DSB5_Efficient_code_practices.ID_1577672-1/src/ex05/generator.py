#!/usr/bin/env python
import sys
import psutil

process = psutil.Process()

def read_lines(filename):
    with open(filename) as f:
        for line in f:
            yield line

def main():

    if len(sys.argv) != 2:
        sys.exit(1)

    for line in read_lines(sys.argv[1]):
        pass

    memory = process.memory_info().rss / (1024**3)
    cpu = process.cpu_times().user + process.cpu_times().system

    print(f"Peak Memory Usage = {memory:.3f} GB")
    print(f"User Mode Time + System Mode Time = {cpu:.2f}s")

if __name__ == '__main__':
    main()