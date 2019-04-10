def isInstancePPL(object1, classInfo):
    if type(object1) is type:
        raise TypeError("object1 is not of type 'object'")
    if type(classInfo) is not type:
        raise TypeError("classInfo is not of type 'type'")
    print type(object1)
    print classInfo
    # return type(object1) >= classInfo
    return is_instance(type(object1), classInfo )


def numInstancePPL(object1, classInfo):
    if type(object1) is type:
        raise TypeError("object1 is not of type 'object'")
    if type(classInfo) is not type:
        raise TypeError("classInfo is not of type 'type'")
    # if not isInstancePPL(object1, classInfo):
    #     return 0
    print "1!!!"
    return num_instance(type(object1), classInfo, 0)



def num_instance(Cob1, cls, num):
    if Cob1 is cls:
        return num
    else:
        c = list(Cob1.__bases__)
        for base in c:
            return num_instance(base, cls, num+1)


def isSubclassPPL(cls, classInfo):

    pass

def is_instance(Cob1, cls):
    if Cob1 is cls:
        return True
    if Cob1 is object:
        False
    else:
        c = list(Cob1.__bases__)
        for base in c:
            return is_instance(base, cls)






class A(object): pass
class B(A): pass
class C(B): pass
class D(C): pass

c = A()
# print isInstancePPL(c, A)
print numInstancePPL(c, A)
# print C.__bases__ == B
# print list(type(c).__bases__)[0] == B
# print list(type(list(type(c).__bases__)[0]).__bases__)
# print B
# print type(c)
# print ((type(c).__bases__)[0].__bases__)[0].__bases__
# print c is C

print type(c).__bases__[0] is object