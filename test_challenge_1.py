import pytest
from challenge_1 import is_log_line, validate_timestamp, get_dict
from dateutil.parser import parse


# The below tests are for the is_log_line() function:

def test_is_log_line_returns_bool():
    """Checks that the function returns a boolean value"""
    result = is_log_line("i am not a log line")
    assert isinstance(result, bool)


def test_valid_log_line_returns_true():
    """Checks that the function returns true if passed a valid
    line from the log file"""
    result = is_log_line("03/11/21 08:51:06 TRACE   :...read_physical_netif: Home list entries returned = 7")
    assert result == True


def test_is_log_line_returns_false_if_input_type_invalid():
    """Checks that the function handles invalid input types"""
    result1 = is_log_line(6)
    assert result1 == False
    result2 = is_log_line(True)
    assert result2 == False


def test_is_log_line_returns_false_if_input_has_insufficient_values():
    """Checks that the function returns false if the input string
    contains insufficient values"""
    result = is_log_line("03/11/21 08:51:06 TRACE")
    assert result == False


def test_is_log_line_returns_false_if_log_level_is_not_valid():
    result = is_log_line("03/11/21 08:51:06 beep :...read_physical_netif: Home list entries returned = 7")
    assert result == False


def test_is_log_line_returns_false_if_any_values_are_empty():
    result1 = is_log_line("TRACE :...read_physical_netif: Home list entries returned = 7")
    assert result1 == False
    result2 = is_log_line("03/11/21 08:51:06   :...read_physical_netif: Home list entries returned = 7")
    assert result2 == False
    result3 = is_log_line("03/11/21 08:51:06 TRACE   this is not a valid message")
    assert result3 == False


# The below tests are for the validate_timestamp() function:

def test_validate_timestamp_returns_bool():
    """Checks that the function takes a string and returns a boolean value"""
    result = validate_timestamp("hello")
    assert isinstance(result, bool)


def test_valid_timestamp_returns_true():
    """Checks that the function will return True if given a valid
    timestamp from the log"""
    result = validate_timestamp("03/11/21 08:51:06")
    assert result == True


def test_invalid_timestamp_returns_false():
    """Checks that the function will return False if given an
    invalid timestamp string"""
    result1 = validate_timestamp("well well well")
    assert result1 == False


def test_validate_timestamp_returns_false_if_given_invalid_data_type():

    result2 = validate_timestamp(6)
    assert result2 == False
    result3 = validate_timestamp(True)
    assert result3 == False


def test_validate_timestamp_accounts_for_variation_in_valid_timestamp_format():
    
    result1 = validate_timestamp("08:51:01 03/11/21")
    assert result1 == True
    result2 = validate_timestamp("2023-07-25T12:30:47.806485+01:00")
    assert result2 == True
    result3 = validate_timestamp("Jan-2003")
    assert result3 == True


# The following tests are for the get_dict() function:

def test_get_dict_returns_dict():
    result = get_dict("03/11/21 08:51:06 TRACE   :...read_physical_netif: Home list entries returned = 7")
    assert isinstance(result, dict)


def test_get_dict_has_all_relevant_keys():
    result = get_dict("03/11/21 08:51:06 TRACE   :...read_physical_netif: Home list entries returned = 7")
    assert 'timestamp' in result
    assert 'log_level' in result
    assert 'message' in result


def test_get_dict_identifies_timestamp_and_log_level_and_message_correctly():
    result = get_dict("03/11/21 08:51:06 TRACE   :...read_physical_netif: Home list entries returned = 7")
    assert result['timestamp'] == '03/11/21 08:51:06'
    assert result['log_level'] == 'TRACE'
    assert result['message'] == ':...read_physical_netif: Home list entries returned = 7'