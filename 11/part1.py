input = open('input.txt', 'r')
lines = input.read().splitlines()

# assuming DAG, so that DFS ends eventually,
# and so that the number of paths from "you" to "out" is finite

from collections import Counter

adjacency = {}
seen = set([])
final = set([])

for line in lines:
    source_tail = line.split(':')
    source = source_tail[0]
    destinations = source_tail[1].strip().split()
    adjacency[source] = Counter(destinations)
    seen.add(source)
    seen.update(destinations)

final = seen.difference(set(adjacency.keys()))

def update(source):
    if source in final:
        if source in adjacency:
            return adjacency[source]
        else:
            return Counter([source])
    result = Counter()
    for item, count in adjacency[source].items():
        result = result + scalar_multiply_counter(count, update(item))
    if result == adjacency[source]:
        final.add(source)
    else:
        adjacency[source] = result
    return result
    

def scalar_multiply_counter(scalar, original_counter):
    multiplied_counter = {}
    for item, count in original_counter.items():
        multiplied_counter[item] = count * scalar
    return Counter(multiplied_counter)

while len(seen.difference(final)) > 0:
    print(seen.difference(final))
    print(adjacency)
    print()
    update(seen.difference(final).pop())

print(adjacency)

with open('output.txt', 'w+') as out:
    out.write(str(adjacency["you"]["out"]))