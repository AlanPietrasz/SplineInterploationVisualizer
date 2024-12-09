from poly import Poly, PolyRange

def iloraz_roznicowy(xs, ys):
    if len(xs) != len(ys):
        raise ValueError
    n = len(xs) - 1
    for i in range(1, n+1):
        for k in range(n, i-1, -1):
            ys[k] = (ys[k] - ys[k-1]) / (xs[k] - xs[k-i])
    return ys[n]



def NIFS3(xs, ys_list):
    if len(xs) != len(ys_list[0]):
        raise ValueError
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
            d[m][i] = 6 * iloraz_roznicowy(xs[i-1:i+1+1], ys_list[m][i-1:i+1+1])

    for i in range(1, N):
        p[i] = lam[i] * q[i-1] + 2
        q[i] = (lam[i] -1) / p[i]

    for i in range(1, N):
        for m in range(M):
            u[m][i] = (d[m][i] - lam[i]*u[m][i-1]) / p[i]

    M_ = [[None] * (N + 1) for _ in range(M)]
    for m in range(M):
        M_[m][N] = 0
        M_[m][0] = 0
        M_[m][N-1] = u[m][N-1]
    for i in range(N-2, 1 -1, -1):
        for m in range(M):
            M_[m][i] = u[m][i] + q[i] * M_[m][i+1]
    s_list = []
    for m in range(M):
        si_list = [] 
        for i in range(1, N+1):
            si = (1/h[i]) * ((1/6)*M_[m][i-1]*(Poly([-1, xs[i]])**3) +\
                            (1/6)*M_[m][i  ]*(Poly([1, -xs[i-1]])**3) +\
                            (ys_list[m][i-1]-(1/6)*M_[m][i-1]*(h[i]**2))*Poly([-1, xs[i]]) +\
                            (ys_list[m][i  ]-(1/6)*M_[m][i  ]*(h[i]**2))*Poly([1, -xs[i-1]]))
            si_list.append(si)
        s_list.append(PolyRange(si_list, xs))

    return s_list


# for i, s in enumerate(NIFS3([-1, 0, 2], [[48, -72, 96], [-1, 0, 2]])):
#     print(f"Funkcja s dla m = {i+1}")
#     print(s)

# print(iloraz_roznicowy([0, 1, 3, 5], [0, 1, 27, 125]))
# print(iloraz_roznicowy([-1, 0, 1], [2479, 1996, 4501]))