from typing import Any
from .utils import Colors, get_terminal_width, strike
import inspect
import dataclasses


def str_type(var: Any) -> str:
    t = type(var)
    if t == int:
        return "int"
    elif t == float:
        return "float"
    elif t == bool:
        return "bool"
    elif t == str:
        return "str"
    elif t == list:
        return "list"
    elif str(t) == "<class 'numpy.ndarray'>": # Trick to not import numpy
        return "ndarray"
    elif t == dict:
        return "dict"
    elif str(t) == "<class 'torch.Tensor'>": # Trick to not import torch
        return "Tensor"
    elif dataclasses.is_dataclass(var):
        return str(t).replace("<class '__main__.", "dataclass ").replace("'>", "")
    else:
        return str(t).replace("<class '__main__.", "class ").replace("'>", "")
    

def return_str_value(var: Any, max_length: int) -> str:
    """Returns a string representation of the value of a variable in at most max_length characters."""
    t = type(var)
    # Number, booleans
    if t == int or t == float or t == bool:
        str_info = str(var)
        if len(str_info) > max_length:
            str_info = str_info[:max_length - 8] + "..." + str_info[-5:]
        return str_info
    # Strings
    elif t == str:
        # Check if the string is too long
        if len(var) > max_length - 2:
            return f'"{var[:max_length - 8]}...{var[-3:]}"'
        else:
            return f'"{var}"'
    # Lists
    elif t == list:
        str_info = "["
        for i, elt in enumerate(var):
            length_available = max_length - len(str_info) - 6
            if i == len(var) - 1:
                length_available = max_length - len(str_info) - 1
            str_info += return_str_value(elt, length_available) + ", "
            if len(str_info) >= max_length - 4 and i != len(var) - 1:
                str_info = str_info[:max_length - 4] +  "...]"

                # Remove the dots that are too long (more than 3)
                # prev_len = -1
                # while prev_len != len(str_info):
                #     prev_len = len(str_info)
                #     str_info = str_info.replace("....", "...")
                
                return str_info
            elif len(str_info) >= max_length - 1 and i == len(var) - 1:
                str_info = str_info[:max_length - 1] + "]"
                return str_info
        str_info = str_info[:-2] + "]"
        return str_info
    # Numpy arrays
    elif str(t) == "<class 'numpy.ndarray'>": # Trick to not import numpy
        return return_str_value(var.tolist(), max_length)
    # Dictionaries
    elif t == dict:
        str_info = "{"
        for key, value in var.items():
            str_info += return_str_value(key, (max_length-8) / 2)
            str_info += ": "
            str_info += return_str_value(value, (max_length-len(str_info)-6)) + ", "
            # TODO: Handle the case where i == len(var) - 1
            if len(str_info) >= max_length - 4:
                str_info = str_info[:max_length-4] + "...}"
                return str_info
        str_info = str_info[:-2] + "}"
        return str_info
    # Pytorch tensors
    elif str(t) == "<class 'torch.Tensor'>": # Trick to not import torch
        # Copy to CPU if necessary
        var_cpu = var.cpu()
        return return_str_value(var_cpu.tolist(), max_length)
    # Dataclasses
    elif dataclasses.is_dataclass(var):
        list_infos = []
        list_types = []
        length_used = 0
        incomplete = False # Ture if we were not able to include all the fields
        for i, field in enumerate(dataclasses.fields(var)):
            list_infos.append(field.name + "=")
            length_available = max_length - length_used - len(list_infos[-1]) - 5
            if i == len(dataclasses.fields(var)) - 1:
                length_available += 5
            list_types.append(str_type(getattr(var, field.name)))
            list_infos[-1] += return_str_value(getattr(var, field.name), length_available)
            length_used += len(list_infos[-1]) + 2
            if length_used >= max_length - 3 and i != len(dataclasses.fields(var)) - 1:
                incomplete = True
                break
            elif length_used >= max_length:
                incomplete = True
                break

        # Now add the list_infos 
        # Fit as many types as possible
        last_type_index = -1
        for str_t in list_types:
            if length_used + 3 + len(str_t) <= max_length - incomplete * 3:
                length_used += 3 + len(str_t)
                last_type_index += 1
            else:
                break
        
        str_info = ""
        for i, info in enumerate(list_infos):
            str_info += info
            if i <= last_type_index:
                str_info += f" {Colors.BLUE}({list_types[i]}){Colors.END}"
            str_info += ", "
        str_info = str_info[:-2]
        if incomplete:
            str_info = str_info[:max_length - 3] + "..."
        return str_info
    # Other
    else:
        str_info = str(var)
        if len(str_info) > max_length:
            str_info = str_info[:max_length - 8] + "..." + str_info[-5:]
        return str_info
    

def return_short_str_info(var_name: str, var: Any, max_length: int = 90) -> str:
    t = type(var)
    str_t = str_type(var)
    prefix = f"{var_name} {Colors.BLUE}({str_t}){Colors.END} = "
    str_info = ""
    length_available = max_length - len(var_name) - len(str_t) - 6
    # Number, booleans
    if t == int or t == float:
        str_info = return_str_value(var, length_available)
    # Strings
    elif t == str:
        str_info2 = " (" + str(len(var)) + " chars)"
        str_info = return_str_value(var, length_available - len(str_info2))
        str_info += f"{Colors.PURPLE}{str_info2}{Colors.END}"
    # Lists
    elif t == list:
        length = len(var)
        str_info2 = " (" + str(length) + " elts)"
        str_info3 = f" ({str_type(var[0])})"
        str_info = return_str_value(var, length_available - len(str_info2) - len(str_info3))
        str_info += f"{Colors.PURPLE}{str_info2}{Colors.END}"
        str_info += f"{Colors.BLUE}{str_info3}{Colors.END}"
    # Numpy arrays
    elif str(t) == "<class 'numpy.ndarray'>": # Trick to not import numpy
        shape = var.shape
        str_info2 = " " + str(shape)
        str_info3 = f" ({var.dtype})"
        str_info = return_str_value(var, length_available - len(str_info2) - len(str_info3))
        str_info += f"{Colors.PURPLE}{str_info2}{Colors.END}"
        str_info += f"{Colors.BLUE}{str_info3}{Colors.END}"
    # Dictionaries
    elif t == dict:
        length = len(var)
        str_info2 = " (" + str(length) + " elts)"
        str_info3 = f" ({str_type(list(var.keys())[0])} -> {str_type(list(var.values())[0])})"
        str_info = return_str_value(var, length_available - len(str_info2) - len(str_info3))
        str_info += f"{Colors.PURPLE}{str_info2}{Colors.END}"
        str_info += f"{Colors.BLUE}{str_info3}{Colors.END}"
    # Pytorch tensors
    elif str(t) == "<class 'torch.Tensor'>": # Trick to not import torch
        shape = var.shape
        device = var.device
        req_grad = var.requires_grad
        str_info2 = " " + str(shape).replace("torch.Size", "").replace('[', '').replace(']', '')
        str_info3 = f" ({str(var.dtype).replace('torch.', '')})"
        str_info4 = f" ({device})"
        str_info5 = "(req-grad)" if req_grad else "(" + strike("req-grad") + ")"
        str_info = return_str_value(var, length_available - len(str_info2) - len(str_info3) - len(str_info4) - len(" (req-grad)"))
        str_info += f"{Colors.PURPLE}{str_info2}{Colors.END}"
        str_info += f"{Colors.BLUE}{str_info3}{Colors.END}"
        str_info += f"{Colors.RED}{str_info4}{Colors.END}"
        str_info += f" {Colors.GREEN}{str_info5}{Colors.END}"
    # Dataclasses
    elif dataclasses.is_dataclass(var):
        str_info = return_str_value(var, length_available)
    # Other str_types
    else:
        str_info = return_str_value(var, length_available)
    return prefix + str_info

def retrieve_name(var, call_context: int = 0):
    """
    Gets the name of var. Use call-context to get the name of the variable in the caller function
    after call_context nested calls.
    Usage:
    >>> a = 1
    >>> retrieve_name(a, call_context=0)
    'a'
    >>> def f(var):
    >>>     return retrieve_name(var, call_context=1)
    >>> f(a)
    'a'
    >>> def g(var):
    >>>     return retrieve_name(var, call_context=0)
    >>> g(a)
    'var'
    """
    stacks = inspect.stack()
    try:
        func = stacks[0 + call_context].function
        code = stacks[1 + call_context].code_context[0]
        s = code.index(func)
        s = code.index("(", s + len(func)) + 1
        e = code.index(")", s)
        return code[s:e].strip()
    except:
        return ""

def debug(var):
    width = get_terminal_width() - 1
    var_name = retrieve_name(var, call_context=1)
    print(f"{Colors.BOLD}DEBUG: {Colors.END}{return_short_str_info(var_name, var, max_length=width-7)}")