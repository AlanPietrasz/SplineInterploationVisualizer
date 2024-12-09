import matplotlib.pyplot as plt

STEP = 0.01

def frange(a, b, step):
    while a <= b:
        yield a
        a += step


def plot_NIFS3(xs, ys, fs_l, step=STEP):
    xs_plot = []
    ys_plot = []
    for i, f in enumerate(fs_l):
        curr_xs = [x for x in frange(xs[i], xs[i+1], step)]
        curr_ys = [f(x) for x in curr_xs]
        xs_plot += curr_xs
        ys_plot += curr_ys
    plt.plot(xs_plot, ys_plot)
    plt.scatter(xs, ys)
    plt.show()