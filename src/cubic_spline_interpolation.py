from poly import Poly, PolyRange

def divided_difference(xs, ys):
    """
    Compute the divided difference for given x and y values.

    Parameters
    ----------
    xs : list of float
        The x-values.
    ys : list of float
        The y-values, corresponding to xs.

    Returns
    -------
    float
        The highest-order divided difference.
    """
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length.")
    n = len(xs) - 1
    for i in range(1, n+1):
        for k in range(n, i-1, -1):
            ys[k] = (ys[k] - ys[k-1]) / (xs[k] - xs[k-i])
    return ys[n]

def cubic_spline_interpolation_multidim(xs, ys_list):
    """
    Perform a natural cubic spline interpolation in multiple dimensions.

    Parameters
    ----------
    xs : list of float
        Sorted list of x-values.
    ys_list : list of lists
        Each element of ys_list is a list of y-values corresponding to xs for one dimension.

    Returns
    -------
    list of PolyRange
        Each element is a piecewise polynomial (PolyRange) representing
        the cubic spline interpolation in one dimension.
    """
    if len(xs) != len(ys_list[0]):
        raise ValueError("Length of xs must match length of each y-vector.")
    N = len(xs) - 1
    M = len(ys_list)
    q = [None] * N
    p = [None] * N
    u = [[None] * N for _ in range(M)]
    for m in range(M):
        q[0] = 0
        p[0] = 0
        u[m][0] = 0

    h = [None] * (N+1)
    for i in range(1, N+1):
        h[i] = xs[i] - xs[i-1]

    lam = [None] * (N+1)
    for i in range(1, N):
        lam[i] = h[i] / (h[i] + h[i+1])

    d = [[None] * N for _ in range(M)]
    for i in range(1, N):
        for m in range(M):
            d[m][i] = 6 * divided_difference(xs[i-1:i+1+1], ys_list[m][i-1:i+1+1])

    for i in range(1, N):
        p[i] = lam[i] * q[i-1] + 2
        q[i] = (lam[i] - 1) / p[i]
        for m in range(M):
            u[m][i] = (d[m][i] - lam[i]*u[m][i-1]) / p[i]

    M_ = [[None] * (N + 1) for _ in range(M)]
    for m in range(M):
        M_[m][N] = 0
        M_[m][0] = 0
        M_[m][N-1] = u[m][N-1]

    for i in range(N-2, -1, -1):
        for m in range(M):
            M_[m][i] = u[m][i] + q[i] * M_[m][i+1]

    s_list = []
    for m in range(M):
        si_list = []
        for i in range(1, N+1):
            si = (1/h[i]) * ((1/6)*M_[m][i-1]*(Poly([-1, xs[i]])**3) +
                             (1/6)*M_[m][i]*(Poly([1, -xs[i-1]])**3) +
                             (ys_list[m][i-1]-(1/6)*M_[m][i-1]*(h[i]**2))*Poly([-1, xs[i]]) +
                             (ys_list[m][i]-(1/6)*M_[m][i]*(h[i]**2))*Poly([1, -xs[i-1]]))
            si_list.append(si)
        s_list.append(PolyRange(si_list, xs))

    return s_list
