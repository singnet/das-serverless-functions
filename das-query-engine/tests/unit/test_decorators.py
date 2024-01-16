# test_execution_helpers.py
import time

from utils.decorators import execution_time_tracker, remove_none_args


def test_remove_none_args():
    @remove_none_args
    def example_function(arg1, arg2, kwarg1="kwarg1", kwarg2="kwarg2"):
        return (arg1, arg2, kwarg1, kwarg2)

    result = example_function(1, 2, kwarg1="value", kwarg2=None)
    assert result == (1, 2, "value", "kwarg2")

    result_all_not_none = example_function(1, "2", kwarg1="value", kwarg2="another_value")
    assert result_all_not_none == (1, "2", "value", "another_value")


def test_execution_time_tracker():
    @execution_time_tracker
    def example_function():
        time.sleep(1)
        return "result"

    result, elapsed_time = example_function()
    assert result == "result"
    assert elapsed_time >= 1 and elapsed_time < 2
