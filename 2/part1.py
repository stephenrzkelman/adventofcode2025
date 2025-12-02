input = open('input.txt', 'r').read()
intervals = input.split(',')

sum_invalid = 0

def handle_constant_length_interval(lower, upper):
    global sum_invalid
    num_len = len(lower)
    if num_len % 2 == 1:
        return
    half_len = num_len//2
    multiplier = 10**(half_len) + 1
    lower_invalid = int(lower[:half_len]) if int(lower[:half_len]) >= int(lower[half_len:]) else int(lower[:half_len]) + 1
    upper_invalid = int(upper[:half_len]) if int(upper[:half_len]) <= int(upper[half_len:]) else int(upper[:half_len]) - 1
    if lower_invalid > upper_invalid:
        return
    sum_invalid += (lower_invalid + upper_invalid) * (upper_invalid - lower_invalid + 1) * multiplier // 2

for interval in intervals:
    lower = interval.split('-')[0]
    upper = interval.split('-')[1]
    for i in range(len(lower), len(upper) + 1):
        handle_constant_length_interval(
            str(max(int(lower), (10**(i-1)))),
            str(min(int(upper), int("9"*i)))
        )
with open("output.txt", "w+") as out:
    out.write(str(sum_invalid))