import torch

def count_learnable_parameters(model: torch.nn.Module) -> int:
    """
    Counts the number of trainable parameters in a model.
    """
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def count_parameters(model: torch.nn.Module) -> int:
    """
    Counts the number of parameters in a model.
    """
    return sum(p.numel() for p in model.parameters())

def get_all_modules(model: torch.nn.Module) -> list:
    """
    Returns all the modules in a model.
    """
    # Source: https://stackoverflow.com/questions/54846905/pytorch-get-all-layers-of-model
    l = [module for module in model.modules() if not isinstance(module, torch.nn.Sequential)]
    return l
