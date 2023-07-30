from dateutil.parser import parse

timestamp = parse("03/11/21 08:51:01")
print(type(timestamp))

new_timestamp = parse("08:51:01 03/11/21")
print(new_timestamp)
print(timestamp)