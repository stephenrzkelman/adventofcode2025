input = open('input.txt', 'r')
lines = input.read().splitlines()

total_power = 0

for line in lines:
    max_seen_reversed = [0]
    for char in reversed(line):
        max_seen_reversed.append(max(max_seen_reversed[-1], int(char)))
    max_joltage = 0
    for i, char in enumerate(line[:-1]):
        max_joltage = max(max_joltage, 10*int(char) + max_seen_reversed[-i-2])
    total_power += max_joltage

with open('output.txt', 'w+') as out:
    out.write(str(total_power))