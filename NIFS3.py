from poly import Poly

def iloraz_roznicowy(xs, ys):
    if len(xs) != len(ys):
        raise ValueError
    n = len(xs) - 1
    for i in range(1, n+1):
        for k in range(n, i-1, -1):
            ys[k] = (ys[k] - ys[k-1]) / (xs[k] - xs[k-i])
    return ys[n]

def NIFS3(xs, ys):
    if len(xs) != len(ys):
        raise ValueError
    n = len(xs) - 1
    q = [None] * n
    u = [None] * n
    p = [None] * n
    q[0] = 0
    u[0] = 0

    h = [None] * (n+1)
    for i in range(1, n+1):
        h[i] = xs[i] - xs[i-1]
    lam = [None] * (n+1)
    for i in range(1, n):
        lam[i] = h[i] / (h[i] + h[i+1])
    
    d = [None] * n
    for i in range(1, n):
        d[i] = 6 * iloraz_roznicowy(xs[i-1:i+1+1], ys[i-1:i+1+1])

    for i in range(1, n):
        p[i] = lam[i] * q[i-1] + 2
        q[i] = (lam[i] -1) / p[i]
        u[i] = (d[i] - lam[i]*u[i-1]) / p[i]

    M = [None] * (n + 1)
    M[n] = 0
    M[0] = 0
    M[n-1] = u[n-1]
    for i in range(n-2, 1 -1, -1):
        M[i] = u[i] + q[i] * M[i+1]
    s_list = []
    for i in range(1, n+1):
        s = (1/h[i]) * ((1/6)*M[i-1]*(Poly([-1, xs[i]])**3) +\
                        (1/6)*M[i  ]*(Poly([1, -xs[i-1]])**3) +\
                        (ys[i-1]-(1/6)*M[i-1]*(h[i]**2))*Poly([-1, xs[i]]) +\
                        (ys[i  ]-(1/6)*M[i  ]*(h[i]**2))*Poly([1, -xs[i-1]]))
        s_list.append(s)

    return s_list

for s in NIFS3([-1, 0, 2], [48, -72, 96]):
    print(s)
# print(iloraz_roznicowy([0, 1, 3, 5], [0, 1, 27, 125]))
# print(iloraz_roznicowy([-1, 0, 1], [2479, 1996, 4501]))