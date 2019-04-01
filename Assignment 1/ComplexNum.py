import math


class ComplexNum(object):

    @staticmethod
    def type_check(other, message="not a complex number"):
        if type(other) is not ComplexNum:
            raise TypeError(message)

    def __init__(self, a, b):
        if type(a) is not int or type(b) is not int:
            raise TypeError("one of the following is not a number: a=" + str(a) + " b=" + str(b))
        self.a = a
        self.b = b

    def re(self):
        return self.a

    def im(self):
        return self.b

    def to_tuple(self):
        return self.a, self.b

    def __repr__(self):
        new_b = self.b
        sign = " + "
        if self.b < 0:
            new_b *= -1
            sign = " - "
        return str(self.a) + sign + str(new_b) + "i"

    def __eq__(self, other):
        if type(other) is not ComplexNum:
            return False
        return self.a == other.a and self.b == other.b

    def __add__(self, other):
        self.type_check(other)
        return ComplexNum(self.a + other.a, self.b + other.b)

    def __neg__(self):
        return ComplexNum(-1 * self.a, -1 * self.b)

    def __sub__(self, other):
        self.type_check(other)
        return self + -other

    def __mul__(self, other):
        self.type_check(other, "Complex multiplication only defined for Complex Numbers")
        return ComplexNum(self.a * other.a - self.b * other.b,
                          self.a * other.b + self.b * other.a)

    def conjugate(self):
        return ComplexNum(self.a, -self.b)

    def __abs__(self):
        return math.sqrt((self * self.conjugate()).re())


# TODO: check if need to support 1+complex and check about neg and abs!
# TODO: z.neg() not working, just -z
# TODO: z.abs not working, just abs(z)

# Tests
z = ComplexNum(1, 2)
print str(z)
print z == ComplexNum(1, 1)
print z == ComplexNum(1, 2)
print str(z + ComplexNum(1, -3))
print str(-z)
print str(z - ComplexNum(4, 3))
print str(z * z)
print str(z * ComplexNum(2, 3))
print str(z.conjugate())
print str(abs(z))
