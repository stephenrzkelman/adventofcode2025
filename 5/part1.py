input = open('input.txt', 'r')
lines = input.read().splitlines()

fresh_ranges = []
available_ingredients = []
for line in lines:
    if line == "":
        continue
    elif '-' in line:
        range_elts = line.split('-')
        fresh_ranges.append((int(range_elts[0]), int(range_elts[1])))
    else:
        available_ingredients.append(int(line))

fresh_ranges.sort()
available_ingredients.sort()
available_ingredient_index = 0
num_available_ingredients = len(available_ingredients)
total_fresh_ingredients = 0
combined_fresh_ranges = [fresh_ranges[0]]
for start, end in fresh_ranges[1:]:
    prev_start, prev_end = combined_fresh_ranges[-1]
    while available_ingredient_index < num_available_ingredients and available_ingredients[available_ingredient_index] <= prev_end:
        if available_ingredients[available_ingredient_index] >= prev_start:
            total_fresh_ingredients += 1
        available_ingredient_index += 1
    if prev_end >= start:
        combined_fresh_ranges.pop()
        combined_fresh_ranges.append((prev_start, max(prev_end, end)))
    else:
        combined_fresh_ranges.append((start, end))
while available_ingredient_index < num_available_ingredients and available_ingredients[available_ingredient_index] <= prev_end:
    if available_ingredients[available_ingredient_index] >= prev_start:
        total_fresh_ingredients += 1
    available_ingredient_index += 1


with open('output.txt', 'w+') as out:
    out.write(str(total_fresh_ingredients))