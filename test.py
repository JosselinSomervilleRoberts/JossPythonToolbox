import numpy as np
#import torch
print("Start importing...")
from toolbox.printing import debug
print("Done importing.")


class Test:
    """A class with some arguments and methods just to test the behavior of the debug function."""

    def __init__(self, a, b, c, d, e, f, g, h, i, j):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h
        self.i = i
        self.j = j

    def method1(self):
        print("method1")

    def method2(self):
        print("method2")


class Test2:
    """A class with some arguments and methods just to test the behavior of the debug function."""

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def method1(self):
        print("method1")

    def method2(self):
        print("method2")

    def __str__(self):
        return f"Test2(a={self.a}, b={self.b}, c={self.c}"
    
import inspect
def retrieve_name_ex(var):
    stacks = inspect.stack()
    try:
        func = stacks[0].function
        code = stacks[1].code_context[0]
        s = code.index(func)
        s = code.index("(", s + len(func)) + 1
        e = code.index(")", s)
        return code[s:e].strip()
    except:
        return ""
    

aasda = np.ones((12,12,12))
b = list(range(100))
c = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h":8, "i": 9, "j": 10}
d = [3,4,5,6]
e = 6
f = 6
g = False
h = [[[1,2,3], [4,5,6], [7,8,9]], [[1,2,3], [4,5,6], [7,8,9]], [[1,2,3], [4,5,6], [7,8,9]]]
i = [list(range(50)), list(range(50)), list(range(50))]
#j = torch.ones((12,12,12))
l = "lore ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
m = Test2(aasda, 12, c)
debug(aasda)
debug(b)
debug(c)
debug(d)
debug(g)
debug(h)
debug(i)
#debug(j)
debug(l)
debug(m)
debug(m.b)
print(retrieve_name_ex(aasda))
print(retrieve_name_ex(m.b))