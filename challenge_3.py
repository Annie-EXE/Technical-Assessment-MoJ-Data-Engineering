# The below function doesn't work correctly. It should sum all the numbers at the
# current time. For example, 01:02:03 should return 6. Improve and fix the function,
# and write unit test(s) for it. Use any testing framework you're familiar with.


# [TODO]: fix the function
def sum_current_time(time_str: str) -> int:
    """Expects data in the format HH:MM:SS"""

    if time_str.strip(" ") == "":
        raise ValueError("Invalid input - time string must not be empty")

    list_of_strings = time_str.split(":")

    if len(list_of_strings) != 3:
        raise ValueError("Invalid input - time string must be in the format HH:MM:SS")

    list_of_nums = []

    for num in list_of_strings:
        int_num = int(num)
        list_of_nums.append(int_num)

    return sum(list_of_nums)


# def test_sum_current_time_returns_int()

print(sum_current_time("01:02:03"))