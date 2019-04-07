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


#print for_all_red([1, 0, 8],  lambda x, y: x*y, lambda x: x>0)

