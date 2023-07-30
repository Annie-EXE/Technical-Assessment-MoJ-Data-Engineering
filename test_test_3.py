import pytest
from test_3 import sum_current_time


def test_sum_current_time_returns_int():

    assert isinstance(sum_current_time("01:02:03"), int)


def test_sum_current_time_calculates_sum_correctly():

    assert sum_current_time("01:02:03") == 6


# def test_sum-current_input

def test_sum_current_input_handles_empty_string():

    with pytest.raises(ValueError):

        sum_current_time("")


def test_sum_current_input_handles_whitespace_string():

    with pytest.raises(ValueError):

        sum_current_time("      ")


def test_sum_current_input_handles_incorrect_input_type():

    with pytest.raises(TypeError):

        sum_current_time(6)

    with pytest.raises(TypeError):

        sum_current_time(6.5)

    with pytest.raises(TypeError):

        sum_current_time(False)


def test_sum_current_input_handles_incorrect_separators():

    with pytest.raises(ValueError):

        sum_current_time("01-02-03")


def test_sum_current_input_handles_negative_time_values():

    with pytest.raises(ValueError):

        sum_current_time("-23:04:05")


def test_sum_current_input_handles_missing_values():

    with pytest.raises(ValueError):

        sum_current_time("04:05:")
    
    with pytest.raises(ValueError):

        sum_current_time("12:30")


def test_sum_current_input_handles_decimal_values():

    with pytest.raises(ValueError):

        sum_current_time("12.5:30:06")

    with pytest.raises(ValueError):

        sum_current_time("15:30.5:06")
    
    with pytest.raises(ValueError):

        sum_current_time("15:.6:06")


def test_sum_current_input_handles_decimal_values():

    with pytest.raises(ValueError):

        sum_current_time("12.5:30:06")

    with pytest.raises(ValueError):

        sum_current_time("15:30.5:06")
    
    with pytest.raises(ValueError):

        sum_current_time("15:.6:06")


def test_sum_current_input_handles_non_numeric_values():

    with pytest.raises(ValueError):

        sum_current_time("HH:MM:SS")

    with pytest.raises(ValueError):

        sum_current_time("1A:2B:3C")
    
    with pytest.raises(ValueError):

        sum_current_time("A01:02:03")



def test_sum_current_input_handles_out_of_range_values():

    with pytest.raises(ValueError):

        sum_current_time("25:64:556958")
    
    with pytest.raises(ValueError):

        sum_current_time("25:01:01")
    
    with pytest.raises(ValueError):

        sum_current_time("01:61:01")
    
    with pytest.raises(ValueError):

        sum_current_time("01:01:61")

    with pytest.raises(ValueError):

        sum_current_time("999:999:999")


def test_sum_current_input_handles_single_digit_values():


    with pytest.raises(ValueError):

        sum_current_time("1:2:3")
    
    with pytest.raises(ValueError):

        sum_current_time("23:1:01")

    with pytest.raises(ValueError):

        sum_current_time("3:01:01")
    
    with pytest.raises(ValueError):

        sum_current_time("03:01:1")