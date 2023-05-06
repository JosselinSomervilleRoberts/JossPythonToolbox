from toolbox.printing import warn, print_color
import numpy as np
from toolbox.printing import debug
from dataclasses import dataclass
warn("Importing torch, this might take a while...")
import torch
print_color("Import Done!\n", "green")


class ClassTest:
    """A class with some arguments and methods just to test the behavior of the debug function."""

    def __init__(self):
        self.test1 = 1
        self.test2 = [1,2,3]
        self.test3 = np.ones((12,12,12))
        self.test4 = {"a": 1, "b": 2, "c": 3}
        self.test5 = "test5"

    def method1(self):
        print("method1")

class ClassTestWithStrMethod(ClassTest):
    """A class with some arguments and methods just to test the behavior of the debug function."""

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "This is a string representation of the class."
    
@dataclass
class DataClassTest:
    """A class with some arguments and methods just to test the behavior of the debug function."""

    variabelTest: int
    varImportant: bool
    varList: list
    var15: float
    anotherVar: str

    def method1(self):
        print("method1")
    

exampleNumpy = np.ones((12,12,12))
exampleList = list(range(100))
exampleDict = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h":8, "i": 9, "j": 10}
exampleShortList = [3,4,5,6]
exampleInt = 22
exampleBool = True
exampleNestedList = [[[1,2,3], [4,5,6], [7,8,9]], [[1,2,3], [4,5,6], [7,8,9]], [[1,2,3], [4,5,6], [7,8,9]]]
exampleSmallNestedLsit = [list(range(50)), list(range(50)), list(range(50))]
exampleTensor = torch.ones((12,12,12))
exampleString = "lore ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
exampleClass = ClassTest()
exampleClassWithStrMethod = ClassTestWithStrMethod()
exampleDataClass = DataClassTest(1, True, [1,2,3], 1.5, "test")

debug(exampleNumpy)
debug(exampleList)
debug(exampleDict)
debug(exampleShortList)
debug(exampleInt)
debug(exampleBool)
debug(exampleNestedList)
debug(exampleSmallNestedLsit)
debug(exampleTensor)
debug(exampleString)
debug(exampleClass)
debug(exampleClassWithStrMethod)
debug(exampleDataClass)