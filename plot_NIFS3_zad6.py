import matplotlib.pyplot as plt
from NIFS3_zad6 import NIFS3
STEP = 0.001

def frange(a, b, step):
    while a <= b:
        yield a
        a += step

def plot_NIFS3_zad6(ts, xs, ys, step=STEP):
    [fxs, fys] =  NIFS3(ts, [xs, ys])
    xs_plot = [fxs(t) for t in frange(ts[0], ts[-1], step)]
    ys_plot = [fys(t) for t in frange(ts[0], ts[-1], step)]
    plt.plot(xs_plot, ys_plot)
    plt.show()