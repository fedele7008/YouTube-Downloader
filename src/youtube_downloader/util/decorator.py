"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

from typing import List
from functools import wraps

from PySide6.QtCore import QObject

def block_signal(*obj_getters):
    """
    A decorator that temporarily blocks signals from QObjects during the execution of the decorated function.

    This decorator is designed to be used with methods of a class that contain QObjects.
    It takes one or more getter functions as arguments, which should return QObjects when called with the instance of the class.

    Args:
        *obj_getters: Variable number of callable objects. Each should be a function that, when called with
                      the instance of the decorated method's class, returns a QObject.

    Returns:
        callable: A decorator function.

    Raises:
        TypeError: If any of the objects returned by the getter functions is not a QObject.

    Example:
    ```
        class MyClass:
            def __init__(self):
                self.obj1 = QObject()
                self.obj2 = QObject()

            @block_signal(lambda self: self.obj1, lambda self: self.obj2)
            def my_method(self):
                # No signals will be emitted from obj1 and obj2 during the execution of my_method
                pass
    ```

    Note:
        This decorator will only block signals for QObjects that are not already blocked.
        If a QObject is already blocked, it will be ignored.
        It ensures that signals are unblocked after the function execution, even if an exception occurs.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            objs: List[QObject] = [getter(self) for getter in obj_getters]
            for obj in objs:
                if not isinstance(obj, QObject):
                    raise TypeError(f"Expected a QObject, got {type(obj).__name__}")
                
            objs_to_block: List[QObject] = [obj for obj in objs if not obj.signalsBlocked()]
            
            for obj in objs_to_block:
                obj.blockSignals(True)
            
            try:
                result = func(self, *args, **kwargs)
            finally:
                for obj in objs_to_block:
                    obj.blockSignals(False)
            
            return result
        return wrapper
    return decorator
