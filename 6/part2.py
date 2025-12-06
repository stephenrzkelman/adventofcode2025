from functools import reduce

input = open('input.txt', 'r')
lines = input.read().splitlines()

operations = lines[-1].split()
input_rows = [list(chars) for chars in lines[:-1]]
input_rows_transposed = [list(row) for row in zip(*input_rows)]
def toint(digit_string):
    if digit_string == "":
        return None
    else:
        return int(digit_string)
input_numbers = [toint("".join(row).strip()) for row in input_rows_transposed]
print(input_numbers)
grouped_input_numbers = [[]]
for input_number in input_numbers:
    if input_number is not None:
        grouped_input_numbers[-1].append(input_number)
    else:
        grouped_input_numbers.append([])

total_ans = 0
for i, operator in enumerate(operations):
    if operations[i] == '*':
        total_ans += reduce(lambda x,y: x*y, grouped_input_numbers[i], 1)
    else:
        total_ans += reduce(lambda x,y: x+y, grouped_input_numbers[i], 0)

with open('output.txt', 'w+') as out:
    out.write(str(total_ans))