from poly import Poly

# Basic tests and examples for the Poly class.
p1 = Poly([1, 2, 3, 4])
print(p1.coeff, p1.n)

p2 = Poly([0, 0, 1, 2])
print(p2.coeff, p2.n)

print(p1)
print(p2)

print(p1+p2)
p3 = Poly([1, 2, 3, 9])
p3[7] = 10
print(p3)
p3[7] = 0
print(p3)
p3[7] = 0

print(Poly([7, 8, 2]) * Poly([8, 6, 5]))
print(Poly([1, -2]) * Poly([1, 3, -5]))
print(Poly([1, -1]) ** 3)
print(Poly([1, 1, 2]) + Poly([-1, 1, 3]))
print(Poly([3, 4, 2]) * 4)
print(4 * Poly([3, 4, 2]))
print(Poly([1, 1, 2]) - Poly([-1, 1, 3]))
print(Poly([1, 1, 2]) - Poly([-1, 1, 3]) + 1)
print(1 + Poly([-1, 1, 3]))
print(1 - Poly([-1, 1, 3]))
