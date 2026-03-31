import cProfile
import sys
sys.argv = ['financial.py', 'MSFT', 'Total Revenue']
cProfile.run('import financial', filename='profile_nosleep.prof')
