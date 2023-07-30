def sum_current_time(time_str: str) -> int:
    """
    Expects data in the format HH:MM:SS
    If data is correctly formatted, the sum of the data's
    digits will be calculated
    """

    if not isinstance(time_str, str):
        raise TypeError("Invalid input - time should be given as a string")

    time_str = time_str.replace(" ", "")
    time_str = time_str.strip()

    if time_str.strip(" ") == "":
        raise ValueError("Invalid input - time string must not be empty")

    list_of_strings = time_str.split(":")

    if len(list_of_strings) != 3 or len(list_of_strings[0]) != 2 or len(list_of_strings[1]) != 2 or len(list_of_strings[2]) != 2:
        raise ValueError("Invalid input - time string must be in the format HH:MM:SS")

    list_of_nums = []

    for num in list_of_strings:

        if not num.isdigit():
            raise ValueError("Invalid input - input should be comprised of only numbers and colons,"
                             + " formatted as HH:MM:SS")

        int_num = int(num)

        if int_num < 0 or int_num >= 60:
            raise ValueError("Invalid input - hour, minute, and second "
                             + " values given should be within range")

        list_of_nums.append(int_num)

    if list_of_nums[0] >= 24:
        raise ValueError("Invalid input - hour, minute, and second values "
                         + "given should be within range")

    return sum(list_of_nums)

print(sum_current_time("01:02:03"))

print(sum_current_time("23:02:03"))
