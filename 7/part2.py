input = open('input.txt', 'r')
lines = input.read().splitlines()

tachyon_start = lines[0].index('S')
tachyon_locations = {tachyon_start: 1}

for line in lines[1:]:
    new_tachyon_locations = {}
    for tachyon_location in tachyon_locations:
        if line[tachyon_location] == '^':
            if tachyon_location - 1 not in new_tachyon_locations:
                new_tachyon_locations[tachyon_location - 1] = 0
            if tachyon_location + 1 not in new_tachyon_locations:
                new_tachyon_locations[tachyon_location + 1] = 0
            new_tachyon_locations[tachyon_location - 1] += tachyon_locations[tachyon_location]
            new_tachyon_locations[tachyon_location + 1] += tachyon_locations[tachyon_location]
        else:
            if tachyon_location not in new_tachyon_locations:
                new_tachyon_locations[tachyon_location] = 0
            new_tachyon_locations[tachyon_location] += tachyon_locations[tachyon_location]
    tachyon_locations = new_tachyon_locations



with open('output.txt', 'w+') as out:
    out.write(str(sum(tachyon_locations.values())))