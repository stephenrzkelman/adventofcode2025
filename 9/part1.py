input = open('input.txt', 'r')
lines = input.read().splitlines()

# list not too long
coordinates = [tuple([int(num) for num in line.split(',')]) for line in lines]
max_area = 0
for index1, (x1,y1) in enumerate(coordinates[:-1]):
    for (x2,y2) in coordinates[index1 + 1:]:
        max_area = max(
            max_area,
            (abs(y2-y1)+1)*(abs(x2-x1)+1)
        )

with open('output.txt', 'w+') as out:
    out.write(str(max_area))