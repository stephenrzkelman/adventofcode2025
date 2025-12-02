input = open('input.txt', 'r')
lines = input.readlines()

cur_pos = 50
num_zeros = 0

for line in lines:
    if line[0] == 'R':
        cur_pos += int(line[1:])
    else:
        cur_pos -= int(line[1:])
    cur_pos %= 100
    if cur_pos == 0:
        num_zeros += 1

with open('output.txt', 'w+') as output:
    output.write(str(num_zeros))
