def isInstancePPL(object1, classInfo):
    if type(object1) is type:
        raise TypeError("object1 is not of type 'object'")
    if type(classInfo) is not type:
        raise TypeError("classInfo is not of type 'type'")
    print type(object1)
    print classInfo
    return type(object1) >= classInfo


def numInstancePPL(object1, classInfo):
    if type(object1) is type:
        raise TypeError("object1 is not of type 'object'")
    if type(classInfo) is not type:
        raise TypeError("classInfo is not of type 'type'")
    # if not isInstancePPL(object1, classInfo):
    #     return 0
    print "1!!!"
    ans = 0
    classOb = type(object1)

    c = list(classOb.__bases__)
    for base in c:
        print base
        print type(object1)
        ans = ans + 1
        if base == classInfo:
            return ans
        classOb = type(base.__bases__)
        print  classOb



class A(object): pass
class B(A): pass
class C(B): pass

c = C()
print isInstancePPL(c, A)
# print numInstancePPL(c, A)
print C.__bases__ == B
print list(type(c).__bases__)[0] == B
print list(type(list(type(c).__bases__)[0]).__bases__)
print B