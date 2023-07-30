from dateutil.parser import parse

# [TODO]: step 1
# Update the is_log_line function below to skip lines that are not valid log lines.
# Valid log lines have a timestamp, error type, and message. For example, lines 1, 3,
# 7 and 37 are all examples of lines (from sample.log) that would be filtered out.
# There's no perfect way to do this: just decide what you think is reasonable to get
# the test to pass. The only thing you are not allowed to do is filter out log lines
# based on the exact row numbers you want to remove.
def is_log_line(line: str) -> bool:
    """Takes a log line and returns True if it is a valid log line and returns nothing
    if it is not.
    """
    try:
        line_segments = line.split(" ")

        if len(line_segments) < 4:
            return False

        timestamp_str = " ".join(line_segments[:2])
        log_level = line_segments[2]
        message = " ".join(line_segments[3:]).strip()

        if not validate_timestamp(timestamp_str):
            return False
        
        if log_level.lower() not in ["info", "trace", "warning"]:
            return False
        
        if not message or message[0] != ":":
            return False

        return True

    except ValueError:
        return False
    
    except TypeError:
        return False
    
    except AttributeError:
        return False

def validate_timestamp(timestamp_str: str) -> bool:
    """Returns 'True' if a string is found to be a timestamp"""
    try:
        parse(timestamp_str)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


# [TODO]: step 2
# Update the get_dict function below so it converts a line of the logs into a
# dictionary with keys for "timestamp", "log_level", and "message". The valid log
# levels are `INFO`, `TRACE`, and `WARNING`. See lines 67 to 71 for how we expect the
# results to look.
def get_dict(line: str) -> dict:
    """Takes a log line and returns a dict with
    `timestamp`, `log_level`, `message` keys
    """
    line_segments = line.split(" ")

    timestamp_str = " ".join(line_segments[:2])
    timestamp = parse(timestamp_str)
    log_level = line_segments[2]
    message = " ".join(line_segments[3:]).strip()

    data = {"timestamp": timestamp_str, "log_level": log_level, "message": message}

    return data


# YOU DON'T NEED TO CHANGE ANYTHING BELOW THIS LINE
if __name__ == "__main__": #pragma: no cover
    # these are basic generators that will return
    # 1 line of the log file at a time
    def log_parser_step_1(log_file):
        f = open(log_file)
        for line in f:
            if is_log_line(line):
                yield line

    def log_parser_step_2(log_file):
        f = open(log_file)
        for line in f:
            if is_log_line(line):
                yield get_dict(line)

    # ---- OUTPUT --- #
    # You can print out each line of the log file line by line
    # by uncommenting this code below
    # for i, line in enumerate(log_parser("sample.log")):
    #     print(i, line)

    # ---- TESTS ---- #
    # DO NOT CHANGE

    def test_step_1():
        with open("tests/step1.log") as f:
            test_lines = f.readlines()
        actual_out = list(log_parser_step_1("sample.log"))

        if actual_out == test_lines:
            print("STEP 1 SUCCESS")
        else:
            print(
                "STEP 1 FAILURE: step 1 produced unexpecting lines.\n"
                "Writing to failure.log if you want to compare it to tests/step1.log"
            )
            with open("step-1-failure-output.log", "w") as f:
                f.writelines(actual_out)

    def test_step_2():
        expected = {
            "timestamp": "03/11/21 08:51:01",
            "log_level": "INFO",
            "message": ":.main: *************** RSVP Agent started ***************",
        }
        actual = next(log_parser_step_2("sample.log"))

        if expected == actual:
            print("STEP 2 SUCCESS")
        else:
            print(
                "STEP 2 FAILURE: your first item from the generator was not as expected.\n"
                "Printing both expected and your output:\n"
            )
            print(f"Expected: {expected}")
            print(f"Generator Output: {actual}")

    try:
        test_step_1()
    except Exception:
        print("step 1 test unable to run")

    try:
        test_step_2()
    except Exception:
        print("step 2 test unable to run")
