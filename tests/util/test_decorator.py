"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

import pytest
from PySide6.QtCore import QObject
from unittest.mock import MagicMock

from youtube_downloader.util.decorator import block_signal

class TestBlockSignalDecorator:

    def test_block_signals(self):
        # Create actual QObjects
        class TestObject(QObject):
            pass

        obj1 = TestObject()
        obj2 = TestObject()
        assert obj1.signalsBlocked() == False
        assert obj2.signalsBlocked() == False

        # Define a class using the decorator
        class MyClass:
            @block_signal(lambda self: obj1, lambda self: obj2)
            def my_method(self):
                # Inside the method, signals should be blocked
                assert obj1.signalsBlocked() == True
                assert obj2.signalsBlocked() == True
                # Perform some operation
                return "method executed"

        instance = MyClass()
        result = instance.my_method()

        # Check that the method executed correctly
        assert result == "method executed"

        # Ensure that signals are unblocked after method execution
        assert obj1.signalsBlocked() == False
        assert obj2.signalsBlocked() == False

    def test_already_blocked_signals(self):
        # Create actual QObjects
        class TestObject(QObject):
            pass

        obj1 = TestObject()
        obj2 = TestObject()
        obj2.blockSignals(True)

        assert obj1.signalsBlocked() == False
        assert obj2.signalsBlocked() == True

        # Define a class using the decorator
        class MyClass:
            @block_signal(lambda self: obj1, lambda self: obj2)
            def my_method(self):
                # Inside the method, signals should be blocked
                assert obj1.signalsBlocked() == True
                assert obj2.signalsBlocked() == True
                # Perform some operation
                return "method executed"

        instance = MyClass()
        result = instance.my_method()

        # Check that the method executed correctly
        assert result == "method executed"

        # Ensure that signals are still blocked
        assert obj1.signalsBlocked() == False
        assert obj2.signalsBlocked() == True

    def test_block_signals_with_non_qobject(self):
        # Create a non-QObject
        non_qobject = MagicMock()

        # Define a class using the decorator with a non-QObject
        class MyClass:
            @block_signal(lambda self: non_qobject)
            def my_method(self):
                pass

        instance = MyClass()
        
        # Expect a TypeError when the method is called
        with pytest.raises(TypeError) as exc_info:
            instance.my_method()
        
        assert "Expected a QObject" in str(exc_info.value)

if __name__ == "__main__":
    pytest.main([__file__])
