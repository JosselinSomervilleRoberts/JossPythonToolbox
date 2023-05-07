
import numpy as np
from dataclasses import dataclass
print("Importing toolbox...")
from toolbox.printing import warn, print_color, debug, sdebug, ldebug, print_visible, print_centered, retrieve_name, print_full_line
print_color("Import Done!\n", "green")
warn("Importing torch and pandas, this might take a while...")
import torch
import pandas as pd
import torch.nn as nn
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
exampleFloat = 1.5
exampleBool = True
exampleNestedList = [[[1,2,3], [4,5,6], [7,8,9]], [[1,2,3], [4,5,6], [7,8,9]], [[1,2,3], [4,5,6], [7,8,9]]]
exampleSmallNestedLsit = [list(range(50)), list(range(50)), list(range(50))]
exampleTensor = torch.ones((12,12,12))
exampleString = "lore ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
exampleClass = ClassTest()
exampleClassWithStrMethod = ClassTestWithStrMethod()
exampleDataClass = DataClassTest(1, True, [1,2,3], 1.5, "test")
def exampleFunctionNoReturn(param1: int, param2: str, param3: bool) -> None:
    """This is an example function."""
    print("This is an example function.")
def exampleFunctionWithReturn(param1: int, param2: str, param3: bool) -> int:
    """This is an example function."""
    print("This is an example function.")
    return 1
def exampleFunctionNoArgs() -> None:
    """This is an example function."""
    print("This is an example function.")
exampleSeries = pd.Series([1,2,3,4,5,6,7,8,9,10])
exampleDf = pd.DataFrame({"a": [1,2,3,4,5,6,7,8,9,10], "b": [1,2,3,4,5,6,7,8,9,10], "c": [1,2,3,4,5,6,7,8,9,10], "d": [1,2,3,4,5,6,7,8,9,10], "e": [1,2,3,4,5,6,7,8,9,10], "f": [1,2,3,4,5,6,7,8,9,10], "g": [1,2,3,4,5,6,7,8,9,10], "h": [1,2,3,4,5,6,7,8,9,10], "i": [1,2,3,4,5,6,7,8,9,10], "j": [1,2,3,4,5,6,7,8,9,10]})
exampleSet = set(range(100))
exampleTuple = tuple(range(100))
exampleModule = nn.Sequential(
    nn.Linear(10, 10),
    nn.ReLU(),
    nn.Linear(10, 10),
    nn.ReLU(),
    nn.Linear(10, 1)
)
exampleNone = None

# Demo
funcs = [debug, sdebug, ldebug]
for func in funcs:
    print_centered(f"{str(func)} demo")
    print_color("\nVanilla types", "bold")
    func(exampleInt)
    func(exampleFloat)
    func(exampleBool)
    func(exampleString)
    func(exampleNone)

    print_color("\nList, Dict, Tuple, Set", "bold")
    func(exampleShortList)
    func(exampleNestedList)
    func(exampleSmallNestedLsit)
    func(exampleList)
    func(exampleDict)
    func(exampleTuple)
    func(exampleSet)

    print_color("\nNumpy", "bold")
    func(exampleNumpy)

    print_color("\nTorch", "bold")
    func(exampleTensor)
    func(exampleModule)

    print_color("\nPandas", "bold")
    func(exampleSeries)
    func(exampleDf)

    print_color("\nClasses", "bold")
    func(exampleClass)
    func(exampleClassWithStrMethod)
    func(exampleDataClass)

    print_color("\nFunctions", "bold")
    func(exampleFunctionNoArgs)
    func(exampleFunctionWithReturn)
    func(exampleFunctionNoReturn)

    func(exampleTuple, visible=True)

    print_full_line()
    print("\n")
    
debug(exampleTuple, visible=False)