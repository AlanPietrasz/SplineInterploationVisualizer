from typing import Any

EPS = 1e-9

def eq_eps(a, b, eps=EPS):
    """
    Check if two values are approximately equal within a given epsilon.
    """
    return abs(a - b) < eps

class Poly:
    """
    A class representing a polynomial with real coefficients.
    Coefficients are stored in reversed order (coeff[i] is the coefficient of x^i).
    """
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
        """
        Initialize the polynomial with given coefficients.
        coeff[0] is the constant term, coeff[1] is x-term, etc.
        """
        self.coeff, self.n = Poly.create_coeff(list(reversed(coeff)))

    def __setitem__(self, i, v):
        """
        Set the coefficient at position i to value v.
        """
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
        """
        Get the coefficient at position i.
        """
        if i > self.n:
            return 0
        return self.coeff[i]
    
    def __call__(self, x):
        """
        Evaluate the polynomial at x.
        """
        res = self[self.n]
        for i in range(self.n-1, -1, -1):
            res *= x
            res += self[i]
        return res

    def __add__(self, other):
        """
        Add two polynomials or a polynomial and a scalar.
        """
        if not isinstance(other, Poly):
            other = Poly([other])
        n = max(self.n, other.n)
        res_poly = Poly()
        for i in range(n+1):
            v = self[i] + other[i]
            res_poly[i] = v
        return res_poly
    
    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        """
        Subtract two polynomials or a polynomial and a scalar.
        """
        return self + (-1 * other)
    
    def __rsub__(self, other):
        return - self + other
    
    def __neg__(self):
        return self * (-1)
    
    def __mul__(self, other):
        """
        Multiply two polynomials or a polynomial and a scalar.
        """
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
        """
        Compute the first derivative of the polynomial.
        """
        res_poly = Poly()
        for i in range(1, self.n+1):
            res_poly[i-1] = i * self[i]
        return res_poly
    
    def __str__(self):
        if self.n == -1:
            return "0"
        def aux(a, i, with_sign=True):
            res = ''
            sign = '+' if a >= 0 else '-'
            if with_sign:
                res += f" {sign}"
            val = abs(a)
            if i == 0:
                res += f"{int(val) if int(val)==val else val}"
            else:
                if int(val) == val and val == 1:
                    res += "x^{%d}" % i
                else:
                    res += f"{val}x^{i}"
            return res
        
        res_str = ''
        if self[self.n] < 0:
            res_str += '-'
        for i in range(self.n, 0, -1):
            if self[i] == 0:
                continue
            if i == self.n:
                # first term
                a = self[i]
                if i == 0:
                    res_str += f"{int(a) if int(a)==a else a}"
                else:
                    val = abs(a)
                    if int(val)==val and val==1:
                        res_str += f"x^{i}"
                    else:
                        res_str += f"{val}x^{i}"
            else:
                res_str += aux(self[i], i, True)
        if self[0] != 0:
            if self.n == 0:
                # only one term
                a = self[0]
                return f"{int(a) if int(a)==a else a}"
            else:
                res_str += aux(self[0], 0, True)
        if res_str[-1] in ['+', '-']:
            return res_str[:-1]
        return res_str

    def __pow__(self, n):
        """
        Compute this polynomial raised to the integer power n.
        """
        if n == 0:
            return Poly([1])
        return (self ** (n-1)) * self


class PolyRange(Poly):
    """
    A piecewise polynomial function defined over given ranges.
    """
    def __init__(self, poly_list, ranges):
        """
        poly_list : list of Poly
            List of polynomials for each sub-interval.
        ranges : list of float
            Boundary points defining the intervals.
        """
        self.poly_list = poly_list
        self.ranges = ranges

    def __call__(self, x):
        """
        Evaluate the piecewise polynomial at x.
        """
        for i in range(len(self.ranges)-1):
            b = self.ranges[i]
            e = self.ranges[i+1]
            if b <= x <= e:
                return self.poly_list[i](x)
        raise ValueError("x is out of the defined range.")
    
    def __str__(self):
        """
        String representation showing each interval and its polynomial.
        """
        res_str = ''
        for i in range(len(self.ranges)-1):
            b = self.ranges[i]
            e = self.ranges[i+1]
            res_str += f"{b} <= x <= {e}  :  {self.poly_list[i]}\n"
        return res_str
    
    def deriv(self):
        """
        Compute the piecewise derivative.
        """
        return PolyRange([s.deriv() for s in self.poly_list], self.ranges)
    
    def is_continuous(self):
        """
        Check continuity at internal nodes.
        """
        for i in range(1, len(self.ranges)-1):
            if not eq_eps(self.poly_list[i-1](self.ranges[i]), self.poly_list[i](self.ranges[i])):
                return False
        return True
        
    def is_cubic_spline(self):
        """
        Check if the piecewise polynomial meets the criteria of a 
        Natural Cubic Spline:
        - Continuous function
        - Continuous first derivative
        - Continuous second derivative
        - Zero second derivatives at the boundaries
        """
        if not self.is_continuous():
            return False
        first_deriv = self.deriv()
        if not first_deriv.is_continuous():
            return False
        second_deriv = first_deriv.deriv()
        if not second_deriv.is_continuous():
            return False
        if not (second_deriv(self.ranges[0]) == 0 == second_deriv(self.ranges[-1])):
            return False
        return True
