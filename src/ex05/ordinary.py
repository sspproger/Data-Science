#!/usr/bin/env python
import sys
import psutil

process = psutil.Process()

def main():

    if len(sys.argv) != 2:
        sys.exit(1)
        
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    for line in lines:
        pass

    memory = process.memory_info().rss / (1024**3) 
    cpu = process.cpu_times().user + process.cpu_times().system

    print(f"Peak Memory Usage = {memory:.3f} GB")
    print(f"User Mode Time + System Mode Time = {cpu:.2f}s")

if __name__ == '__main__':
    main()    