input = open('input.txt', 'r')
lines = input.read().splitlines()

operations = lines[-1].split()
input_rows = [[int(digit_string) for digit_string in line.split()] for line in lines[:-1]]

answers = [1 if operation == '*' else 0 for operation in operations]
for input_row in input_rows:
    for i, input in enumerate(input_row):
        if operations[i] == '*':
            answers[i] *= input
        else:
            answers[i] += input

with open('output.txt', 'w+') as out:
    out.write(str(sum(answers)))