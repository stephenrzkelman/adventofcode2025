input = open('input.txt', 'r')
lines = input.read().splitlines()

# assuming DAG, so that DFS ends eventually,
# and so that the number of paths from "you" to "out" is finite

from collections import Counter

adjacency_fft = {}
seen_fft = set([])
final_fft = set([])

for line in lines:
    source_tail = line.split(':')
    source = source_tail[0]
    destinations = source_tail[1].strip().split()
    adjacency_fft[source] = Counter(destinations)
    seen_fft.add(source)
    seen_fft.update(destinations)
adjacency_fft.pop("fft")

final_fft = seen_fft.difference(set(adjacency_fft.keys()))

def update(source):
    if source in final_fft:
        if source in adjacency_fft:
            return adjacency_fft[source]
        else:
            return Counter([source])
    result = Counter()
    for item, count in adjacency_fft[source].items():
        result = result + scalar_multiply_counter(count, update(item))
    if result == adjacency_fft[source]:
        final_fft.add(source)
    else:
        adjacency_fft[source] = result
    return result
    

def scalar_multiply_counter(scalar, original_counter):
    multiplied_counter = {}
    for item, count in original_counter.items():
        multiplied_counter[item] = count * scalar
    return Counter(multiplied_counter)

while len(seen_fft.difference(final_fft)) > 0:
    update(seen_fft.difference(final_fft).pop())


adjacency_dac = {}
seen_dac = set([])
final_dac = set([])

for line in lines:
    source_tail = line.split(':')
    source = source_tail[0]
    destinations = source_tail[1].strip().split()
    adjacency_dac[source] = Counter(destinations)
    seen_dac.add(source)
    seen_dac.update(destinations)
adjacency_dac.pop("dac")

final_dac = seen_dac.difference(set(adjacency_dac.keys()))

def update(source):
    if source in final_dac:
        if source in adjacency_dac:
            return adjacency_dac[source]
        else:
            return Counter([source])
    result = Counter()
    for item, count in adjacency_dac[source].items():
        result = result + scalar_multiply_counter(count, update(item))
    if result == adjacency_dac[source]:
        final_dac.add(source)
    else:
        adjacency_dac[source] = result
    return result
    

def scalar_multiply_counter(scalar, original_counter):
    multiplied_counter = {}
    for item, count in original_counter.items():
        multiplied_counter[item] = count * scalar
    return Counter(multiplied_counter)

while len(seen_dac.difference(final_dac)) > 0:
    update(seen_dac.difference(final_dac).pop())

# print(adjacency_dac)

adjacency_out = {}
seen_out = set([])
final_out = set([])

for line in lines:
    source_tail = line.split(':')
    source = source_tail[0]
    destinations = source_tail[1].strip().split()
    adjacency_out[source] = Counter(destinations)
    seen_out.add(source)
    seen_out.update(destinations)

final_out = seen_out.difference(set(adjacency_out.keys()))

def update(source):
    if source in final_out:
        if source in adjacency_out:
            return adjacency_out[source]
        else:
            return Counter([source])
    result = Counter()
    for item, count in adjacency_out[source].items():
        result = result + scalar_multiply_counter(count, update(item))
    if result == adjacency_out[source]:
        final_out.add(source)
    else:
        adjacency_out[source] = result
    return result
    

def scalar_multiply_counter(scalar, original_counter):
    multiplied_counter = {}
    for item, count in original_counter.items():
        multiplied_counter[item] = count * scalar
    return Counter(multiplied_counter)

while len(seen_out.difference(final_out)) > 0:
    update(seen_out.difference(final_out).pop())

# print(adjacency_out)

with open('output.txt', 'w+') as out:
    svr_fft_dac_out = adjacency_fft['svr']['fft'] * adjacency_dac['fft']['dac'] * adjacency_out['dac']['out']
    svr_dac_fft_out = adjacency_dac['svr']['dac'] * adjacency_fft['dac']['fft'] * adjacency_out['fft']['out']
    
    out.write(str(svr_dac_fft_out + svr_fft_dac_out))