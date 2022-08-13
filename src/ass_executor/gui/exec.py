import importlib
import inspect
from functools import wraps
from typing import List


def exec_ui():
    """
    Decorates the function as a UI button.

    Returns:
        The wrapper function object.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # only use a wrapper if you need extra code to be run here
            response = func(*args, **kwargs)
            # or here
            return response
        wrapper.__UI_BUTTON__ = True
        return wrapper

    return decorator


def find_ui_button_functions(module_path: str) -> List:

    mod = importlib.import_module(module_path)

    return [
        (name, member)
        for name, member in inspect.getmembers(mod)
        if inspect.isfunction(member)  and hasattr(member, "__UI_BUTTON__")
    ]
