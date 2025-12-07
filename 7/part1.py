input = open('input.txt', 'r')
lines = input.read().splitlines()

tachyon_start = lines[0].index('S')
tachyon_locations = set([tachyon_start])
num_splits = 0

for line in lines[1:]:
    new_tachyon_locations = set([])
    for tachyon_location in tachyon_locations:
        if line[tachyon_location] == '^':
            new_tachyon_locations.add(tachyon_location - 1)
            new_tachyon_locations.add(tachyon_location + 1)
            num_splits += 1
        else:
            new_tachyon_locations.add(tachyon_location)
    tachyon_locations = new_tachyon_locations



with open('output.txt', 'w+') as out:
    out.write(str(num_splits))