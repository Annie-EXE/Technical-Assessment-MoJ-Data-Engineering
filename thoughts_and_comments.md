## Challenge 1

### `is_log_line()`

- While thinking about how to approach this task, I realised my solution would make certain assumptions about how valid data is structured (for example, the order of values and, how values are separated, and the format of the values). This means the code will have limited reusability for files other than `sample.log`
- I have decided to use helper functions (such as a function to verify whether a timestamp is valid), to isolate aspects of the code for testing, and to make my code more readable
- Using parse() to identify the timestamp as valid allows me to account for some variation in timestamp format, thus making the code more reusable
- If I could restructure the code (the section we are told not to change), I would have this function return a tuple: the first value being boolean, and the second being a message specifying why this log line is invalid
- Because I am trying to manipulate the log line as if it is a string which meets certain specifications, I need to make sure this function handles errors gracefully

### `get_dict()`

- Because I am using the code structure given by the assessment, there is some repetition between the previous function and this one (e.g., having to split the line again)
- There is little error handling to do in this function as I already checked for valid values in the `is_log_line()` function, which is called as a prerequisite to this one

## Challenge 2

- My approach was to first create a function which extracts each individual's data from `people.csv`, and creates a list of dictionaries (where each list is one person's data)
- I then created a function which takes a postcode and a court type, and returns the nearest court of the specified type
- I then called this function for each person in my data list
- My `get_data_from_csv()` function takes a file path as an argument, to increase code reusability
- I created the helper function `process_csv_row()` to improve testability
- In the `get_nearest_relevant_court()`, I created a list of relevant courts (courts of the correct type within the top 10 closest courts) so that the functionality to display a list of options to an individual can be implemented easily
- The task description mentions that the API request returns the ten nearest courts to a postcode, but does not specify that these are ordered by distance to the postcode. Although this is the pattern I have observed while interacting with the API, I have still designed my code to ensure that my selected court is the _nearest_ appropriate court
- I am making the assumption that 'distance' is measured in miles, based on typing court names into Google Maps
- Finally, I made the `generate_output()` function, which accepts one individual's data as a dictionary, then calls the `get_nearest_relevant_court()` function on this data. It prints the relevant data in a user-friendly way
