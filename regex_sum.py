import re

with open("regex_sum_2449223.txt", "r") as file:
    text = file.read()

numbers = re.findall("[0-9]+", text)
numbers = [int(n) for n in numbers]

total = sum(numbers)
print(total)