input = open('input.txt', 'r')
lines = input.readlines()

cur_pos = 50
num_zeros = 0

for line in lines:
    prev_pos = cur_pos
    if line[0] == 'R':
        cur_pos += int(line[1:])
    else:
        cur_pos -= int(line[1:])
    lower = min(cur_pos, prev_pos)
    upper = max(cur_pos, prev_pos)
    zeros_between = (upper - 1)//100 - lower//100
    num_zeros += zeros_between
    cur_pos %= 100
    if cur_pos == 0:
        num_zeros += 1

with open('output.txt', 'w+') as output:
    output.write(str(num_zeros))
