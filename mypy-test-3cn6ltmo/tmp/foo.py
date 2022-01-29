from typing import List, Any

def foo():
    return {'x': 5}

def bar():
    return {}

def baz() -> List[Any]:
    return [{'x': 5}]

def quux() -> List[Any]:
    return [1]

def spam(x):
    pass

spam({'x': 5})