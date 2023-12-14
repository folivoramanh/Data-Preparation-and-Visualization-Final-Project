import time
from contextlib import contextmanager


@contextmanager
def timer(title):
    '''
    This function is used to calculate the time it takes to run a function
    '''

    t0 = time.time()
    yield
    print("{} - done in {:.0f}s".format(title, time.time() - t0))
