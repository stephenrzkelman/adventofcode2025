input = open('input.txt', 'r')
lines = input.read().splitlines()

fresh_ranges = []
for line in lines:
    if '-' in line:
        range_elts = line.split('-')
        fresh_ranges.append((int(range_elts[0]), int(range_elts[1])))

fresh_ranges.sort()
total_fresh_ingredients = 0
combined_fresh_ranges = [fresh_ranges[0]]
for start, end in fresh_ranges[1:]:
    prev_start, prev_end = combined_fresh_ranges[-1]
    if prev_end >= start:
        combined_fresh_ranges.pop()
        combined_fresh_ranges.append((prev_start, max(prev_end, end)))
    else:
        total_fresh_ingredients += prev_end - prev_start + 1
        combined_fresh_ranges.append((start, end))

prev_start, prev_end = combined_fresh_ranges[-1]
total_fresh_ingredients += prev_end - prev_start + 1


with open('output.txt', 'w+') as out:
    out.write(str(total_fresh_ingredients))