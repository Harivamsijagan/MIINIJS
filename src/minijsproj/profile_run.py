import cProfile
import pstats
import sys

from interpreter import main

program = r"C:\Users\SAMSUNG\Desktop\minijsproj\src\minijsproj\test.mjs"

profiler = cProfile.Profile()
profiler.enable()
main(["interpreter.py", program])
profiler.disable()

stats = pstats.Stats(profiler)
stats.strip_dirs().sort_stats("cumulative").print_stats(20)
