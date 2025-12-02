input = open('input.txt', 'r').read()
intervals = input.split(',')

sum_invalid = 0
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43] # not expecting integers longer than 43 digits

def handle_constant_lenth_interval_repetition(lower, upper, repetitions):
    global sum_invalid
    num_len = len(lower)
    if num_len % repetitions != 0:
        return
    segment_length = num_len // repetitions
    multiplier = int(("0" * (segment_length - 1) + "1") * repetitions)
    lower_is_invalid = True
    lower_compare = int(lower[:segment_length])
    for i in range(segment_length, num_len, segment_length):
        if int(lower[i: i+segment_length]) < lower_compare:
            break
        elif int(lower[i: i+segment_length]) > lower_compare:
            lower_is_invalid = False
            break
    lower_invalid = lower_compare if lower_is_invalid else lower_compare + 1
    upper_is_invalid = True
    upper_compare = int(upper[:segment_length])
    for i in range(segment_length, num_len, segment_length):
        if int(upper[i: i+segment_length]) > upper_compare:
            break
        elif int(upper[i: i+segment_length]) < upper_compare:
            upper_is_invalid = False
            break
    upper_invalid = upper_compare if upper_is_invalid else upper_compare - 1
    if upper_invalid < lower_invalid:
        return
    invalid_total = (lower_invalid + upper_invalid) * (upper_invalid - lower_invalid + 1) * multiplier // 2
    if repetitions in primes:
        sum_invalid += invalid_total
    else:
        num_primes = 0
        for p in primes:
            if p > repetitions:
                break
            if repetitions % p == 0:
                num_primes += 1
        if num_primes <= 1:
            return
        elif num_primes % 2 == 0:
            sum_invalid -= invalid_total
        else:
            sum_invalid += invalid_total

def handle_constant_length_interval(lower, upper):
    global primes
    num_len = len(lower)
    for n in range(2,num_len + 1):
        handle_constant_lenth_interval_repetition(lower, upper, n)


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