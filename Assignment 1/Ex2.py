def isInstancePPL(object1, classInfo):
    if type(object1) is type:
        raise TypeError("object1 is not of type 'object'")
    if type(classInfo) is not type:
        raise TypeError("classInfo is not of type 'type'")
    print type(object1)
    print classInfo
    return type(object1) >= classInfo

class A(object): pass
class B(A): pass
class C(B): pass

c = C()
print isInstancePPL(c, A)