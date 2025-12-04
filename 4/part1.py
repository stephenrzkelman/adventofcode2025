input = open('input.txt', 'r')
grid = input.read().splitlines()

width = len(grid[0])
height = len(grid)

def is_paper_towel(x, y):
    return grid[y][x] == '@'

def is_accessible(x, y):
    num_paper_towels = 0
    x_neighbors = [0]
    y_neighbors = [0]
    if x > 0:
        x_neighbors.append(-1)
    if x < width - 1:
        x_neighbors.append(1)
    if y > 0:
        y_neighbors.append(-1)
    if y < height - 1:
        y_neighbors.append(1)
    for x_diff in x_neighbors:
        for y_diff in y_neighbors:
            if (x_diff, y_diff) == (0,0):
                continue
            if grid[y+y_diff][x+x_diff] == '@':
                num_paper_towels += 1
    return num_paper_towels < 4

num_accessible = 0
for y, row in enumerate(grid):
    for x, char in enumerate(row):
        if is_paper_towel(x,y) and is_accessible(x,y):
            num_accessible += 1

with open('output.txt', 'w+') as out:
    out.write(str(num_accessible))