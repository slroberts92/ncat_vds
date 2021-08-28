import sys
import datetime

def log(*args, **kwargs):

    print(f'{datetime.datetime.now()}: ', file=sys.stderr, end='')
    print(*args, file=sys.stderr, **kwargs)

