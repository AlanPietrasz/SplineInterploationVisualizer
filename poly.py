from typing import Any

EPS = 1e-9

def eq_eps(a, b, eps=EPS):
    return abs(a - b) < eps

class Poly:
    def create_coeff(coeff):
        if coeff == [] or coeff == [0]:
            return [], -1
        n = len(coeff) - 1
        while n >= 0:
            if coeff[n] != 0:
                break
            n -= 1
        return coeff[:n+1], n



    def __init__(self, coeff=[]):
        self.coeff, self.n = Poly.create_coeff(list(reversed(coeff)))

    def __setitem__(self, i, v):
        if v == 0 and i > self.n:
            return
        if v == 0 and self.n == i:
            self.coeff, self.n = Poly.create_coeff(self.coeff[:-1])
            return
        if self.n < i:
            j = self.n + 1
            while j <= i:
                self.coeff.append(0)
                j += 1
            self.n = i
        self.coeff[i] = v
        
    def __getitem__(self, i):
        if i > self.n:
            return 0
        return self.coeff[i]
    
    def __call__(self, x):
        res = self[self.n]
        for i in range(self.n-1, -1, -1):
            res *= x
            res += self[i]
        return res

    def __add__(self, other):
        if not isinstance(other, Poly):
            other = Poly([other])
        if self.n > other.n:
            n = self.n
        else:
            n = other.n
        res_poly = Poly()
        for i in range(n+1):
            v = 0
            v += self[i] + other[i]
            res_poly[i] = v
        return res_poly
    
    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        return self + (-1 * other)
    
    def __rsub__(self, other):
        return - self + other
    
    def __neg__(self):
        return self * (-1)
    

    
    def __mul__(self, other):
        if not isinstance(other, Poly):
            other = Poly([other])
        def convolution(k):
            sum_ = 0
            for i in range(0, k+1):
                sum_ += self[i] * other[k-i]
            return sum_
        
        res_poly = Poly()
        for i in range(self.n + other.n + 1):
            res_poly[i] = convolution(i)
        return res_poly
    
    def __rmul__(self, other):
        return self * other
    
    def deriv(self):
        res_poly = Poly()
        for i in range(1, self.n+1):
            res_poly[i-1] = i * self[i]
        return res_poly
    
    
    
    def __str__(self):
        if self.n == -1:
            return "0"
        def aux(a, i, with_sign=True):
            res = ''
            if with_sign:
                res += f" {'+' if a >= 0 else '-'}"
            if int(a) == a:
                res += f"{int(abs(a)) if a != 1 or i == 0 else ''}"
            else:
                res += f"{abs(a)}"
            if i != 0:
                res +=  f"x^{i}"
            return res
        
        res_str = f""
        if self[self.n] < 0:
            res_str += '-'
        for i in range(self.n, 0, -1):
            if self[i] == 0:
                continue
            res_str += aux(self[i], i, not i==self.n)
        if self[0] != 0:
            res_str += aux(self[0], 0, not 0==self.n)
        if res_str[-1] in ['+', '-']:
            return res_str[:-1]
        return res_str
    
    def __pow__(self, n):
        if n == 0:
            return Poly([1])
        return (self ** (n-1)) * self




class PolyRange(Poly):
    def __init__(self, poly_list, ranges):
        self.poly_list = poly_list
        self.ranges = ranges

    def __call__(self, x):
        for i in range(len(self.ranges)-1):
            b = self.ranges[i]
            e = self.ranges[i+1]
            if b <= x and x <= e:
                return self.poly_list[i](x)
        raise ValueError
    
    def __str__(self):
        res_str = ''
        for i in range(len(self.ranges)-1):
            b = self.ranges[i]
            e = self.ranges[i+1]
            res_str += f"{b} <= x <= {e}  :  "
            res_str += str(self.poly_list[i])
            res_str += '\n'

        return res_str
    
    def deriv(self):
        return PolyRange([s.deriv() for s in self.poly_list], self.ranges)
    
    def is_continuous(self):
        for i in range(1, len(self.ranges)-1):
            if not eq_eps(self.poly_list[i-1](self.ranges[i]), self.poly_list[i](self.ranges[i])):
                return False
        return True
        
    def is_NIFS3(self):
        if not self.is_continuous():
            return False
        first_deriv = self.deriv()
        print("f'(x) = ")
        print(first_deriv)
        if not first_deriv.is_continuous():
            return False
        second_deriv = first_deriv.deriv()
        print("f\"(x) = ")
        print(second_deriv)
        if not second_deriv.is_continuous():
            return False
        if not second_deriv(self.ranges[0]) == 0 == second_deriv(self.ranges[-1]):
            return False
        
        return True
        
# print(PolyRange([Poly([1, 2, 3, 4]), Poly([1, 1, 1, 1])], [-1, 0, 1]).deriv())