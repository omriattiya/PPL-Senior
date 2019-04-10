##########################1111##########################

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
            sign = "-"
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

    def abs(self):
        return self.__abs__()

    def neg(self):
        return self.__neg__()

#######################2222222#####################


def isInstancePPL(object1, classInfo):
    if type(object1) is type:
        raise TypeError("object1 is not of type 'object'")
    if type(classInfo) is not type:
        raise TypeError("classInfo is not of type 'type'")
    return is_instance(type(object1), classInfo)


def numInstancePPL(object1, classInfo):
    if type(object1) is type:
        raise TypeError("object1 is not of type 'object'")
    if type(classInfo) is not type:
        raise TypeError("classInfo is not of type 'type'")
    if not isInstancePPL(object1, classInfo):
        return 0
    return num_instance(type(object1), classInfo, 1)



def num_instance(Cob1, cls, num):
    if Cob1 is cls:
        return num
    else:
        c = list(Cob1.__bases__)
        maxans = num
        for base in c:
            if is_instance(Cob1, cls):
                maxans = max(maxans, num_instance(base, cls, num+1))
        return maxans


def isSubclassPPL(cls, classInfo):
    if type(cls) is not type:
        raise TypeError("classInfo is not of type 'type'")
    if type(classInfo) is not type:
        raise TypeError("classInfo is not of type 'type'")
    return is_instance(cls, classInfo)


def is_instance(Cob1, cls):
    if Cob1 is cls:
        return True
    if Cob1 is object:
        return False
    else:
        c = list(Cob1.__bases__)
        ans = False
        for base in c:
            ans = ans or is_instance(base, cls)
        return ans


def numSubclassPPL(class1, classInfo):
    if type(class1) is not type:
        raise TypeError("class1 is not of type 'type'")
    if type(classInfo) is not type:
        raise TypeError("classInfo is not of type 'type'")
    return num_instance(class1, classInfo, 0)

class A(object): pass
class B(A): pass
class C(B): pass
class D(object): pass

c = D()
# print isInstancePPL(c, D)
# print numInstancePPL(c, D)
# print C.__bases__ == B
# print list(type(c).__bases__)[0] == B
# print list(type(list(type(c).__bases__)[0]).__bases__)
# print B
# print type(c)
# print ((type(c).__bases__)[0].__bases__)[0].__bases__
# print c is C

# print type(c).__bases__[0] is object


#######################33333333333##############################3


def count_if(arr, func):
    if callable(func) and isinstance(arr, list):
        return reduce(lambda x,y: 1+ x if func(y) else x, arr, 0)
    raise ValueError ("Value don't much")


def for_all(lst, apply, pred):
    if callable(apply) and callable(pred) and isinstance(lst, list):
        return reduce(lambda x, y: x if pred(apply(y)) else False, lst, True)
    raise ValueError("Value don't much")


def for_all_red(lst, apply, pred):
    if callable(apply) and callable(pred) and isinstance(lst, list):
        return pred( reduce(apply,lst))
    raise ValueError("Value don't much")


## if we need only in high order function

def there_exists(lst, n, pred):
    return reduce(lambda x, y: x+ 1 if pred(y) else x,lst, 0) >= n
