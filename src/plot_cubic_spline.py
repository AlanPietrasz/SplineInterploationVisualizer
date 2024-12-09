import matplotlib.pyplot as plt
from cubic_spline_interpolation import cubic_spline_interpolation_multidim

STEP = 0.001

def frange(a, b, step):
    """
    Generate a range of floating point values from a to b with a given step.
    """
    while a <= b:
        yield a
        a += step

def plot_cubic_spline_multidim(ts, xs, ys, step=STEP):
    """
    Compute the cubic spline multidimensional interpolation for given ts, xs, ys
    and plot the resulting parametric curve (xs(t), ys(t)).

    Parameters
    ----------
    ts : list of float
        Parameter values.
    xs : list of float
        x-values for each parameter t.
    ys : list of float
        y-values for each parameter t.
    step : float, optional
        Step size for plotting, by default 0.001
    """
    [fxs, fys] = cubic_spline_interpolation_multidim(ts, [xs, ys])
    xs_plot = [fxs(t) for t in frange(ts[0], ts[-1], step)]
    ys_plot = [fys(t) for t in frange(ts[0], ts[-1], step)]
    plt.plot(xs_plot, ys_plot)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Cubic Spline Interpolation")
    plt.show()
