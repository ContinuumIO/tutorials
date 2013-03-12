import time

class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

def _fib(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)

def fib(N):
    return [_fib(n) for n in xrange(N)]

def plotfib(N=20, func=fib, trials=10, setup=True):
    from pylab import plot, show, gca, xlabel, ylabel, title
    kvals = range(5,N)
    times = []
    for k in kvals:
        index = trials
        val = 1
        while index > 0 :
            with Timer() as t:
                result = func(k)
            val = min(val, t.interval)
            index -= 1     
        times.append(val)
    plot(kvals, [time*1000 for time in times], linewidth=10)
    if setup:
        ax = gca()
        for label in ax.xaxis.get_majorticklabels():
            label.set_fontsize(24)
        for label in ax.yaxis.get_majorticklabels():
            label.set_fontsize(24)       
        xlabel('N', fontsize=36)
        ylabel('CPU Time (ms)', fontsize=36)
        title('Time to create N Fibonnacci numbers', fontsize=36)
    show()

def fib1(N):
    result = [0,1]
    for k in range(2,N):
        result.append(result[k-1] + result[k-2])
    return result

from numpy import roots, arange
r1, r2 = roots([1,-1,-1])
C = 1.0/(r1-r2)
def fib2a(N):
    n = arange(N,dtype=float)
    return C*(r1**n - r2**n)

def fib2(N):
    return fib2a(N).astype(int)


from scipy.signal import lfilter
from numpy import zeros, array
b = array([1.0])
a = array([1.,-1,-1])
zi = array([0, 1.0])
def fib3a(N):
    y, zf = lfilter(b, a,
                    zeros(N,dtype=float),zi=zi)
    return y

def fib3(N):
    return fib3a(N).astype(int)

