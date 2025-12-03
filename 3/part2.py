input = open('input.txt', 'r')
lines = input.read().splitlines()

total_power = 0
num_digits = 12

for line in lines:
    if len(line) < num_digits:
        continue
    largest_subsequent_nminus1_digit_numbers = [0 for char in line]
    for i in range(num_digits - 1):
        largest_subsequent_n_digit_numbers = [0]
        for j in range(-1, -len(largest_subsequent_nminus1_digit_numbers), -1):
            largest_subsequent_n_digit_numbers.append(max(
                largest_subsequent_n_digit_numbers[-1],
                10**(i) * int(line[-i+j]) + largest_subsequent_nminus1_digit_numbers[j]
            ))
        largest_subsequent_nminus1_digit_numbers = list(reversed(largest_subsequent_n_digit_numbers[1:]))
    max_joltage = 0
    for i, largest_subsequent_nminus1_digit_num in enumerate(largest_subsequent_nminus1_digit_numbers):
        max_joltage = max(
            max_joltage,
            10**(num_digits - 1) * int(line[i]) + largest_subsequent_nminus1_digit_num
        )
    total_power += max_joltage



with open('output.txt', 'w+') as out:
    out.write(str(total_power))