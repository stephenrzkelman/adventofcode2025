import numpy as np

input = open('input.txt', 'r')
lines = input.read().splitlines()

# unstated assumptions, verified from inputs:
# - no more than 2 red tiles share a given x coordinate (or a given y coordinate)
# - no 2 listed coordinates are exactly the same (same x and y coordinate)

coordinates = [tuple([int(num) for num in line.split(',')]) for line in lines]
if coordinates[0][0] != coordinates[1][0]:
    coordinates.append(coordinates[0])
    coordinates.pop(0)
coordinates.sort(key=lambda x: x[0]) # must be stable sort
right_hand_orientation = True if coordinates[0][1] > coordinates[1][1] else False

def is_left_edge(coord1, coord2):
    if right_hand_orientation:
        return coord1[1] > coord2[1]
    else:
        return coord1[1] < coord2[1]
    
active_intervals = {}
active_red_tiles = []
max_area_found = 0

def update_max_area(corner1, corner2):
    global max_area_found
    (corner1_x, corner1_y) = corner1
    (corner2_x, corner2_y) = corner2
    area = (abs(corner1_x-corner2_x) + 1)*(abs(corner1_y-corner2_y) + 1)
    # print((corner1_x, corner1_y), (corner2_x, corner2_y), area)
    if area > max_area_found:
        max_area_found = area

def interval_subtract(lower1, upper1, lower2, upper2):
    result_intervals = []
    if lower1 > upper2 or lower2 > upper1:
        result_intervals.append((lower1, upper1))
    elif lower1 >= lower2:
        if upper1 <= upper2:
            pass
        else:
            result_intervals.append((upper2+1, upper1))
    else:
        result_intervals.append((lower1, lower2-1))
        if upper1 <= upper2:
            pass
        else:
            result_intervals.append((upper2+1, upper1))
    

for i in range(len(coordinates)//2):
    # print(active_red_tiles)
    coord1 = (coord1_x, coord1_y) = coordinates[2 * i]
    coord2 = (coord2_x, coord2_y) = coordinates[2 * i + 1]
    for (tile_x, tile_y), (lower_y, upper_y) in active_red_tiles:
        if coord1_y >= lower_y and coord1_y <= upper_y:
            update_max_area((tile_x, tile_y), coord1)
        if coord2_y >= lower_y and coord2_y <= upper_y:
            update_max_area((tile_x, tile_y), coord2)
    if is_left_edge(coord1, coord2):
        new_active_interval_lower = min(coord1_y, coord2_y)
        new_active_interval_upper = max(coord1_y, coord2_y)
        if new_active_interval_lower in active_intervals:
            new_active_interval_lower = active_intervals[new_active_interval_lower]
            active_intervals.pop(new_active_interval_lower)
        elif new_active_interval_lower - 1 in active_intervals:
            new_active_interval_lower = active_intervals[new_active_interval_lower - 1]
            active_intervals.pop(new_active_interval_lower - 1)
        if new_active_interval_upper in active_intervals:
            new_active_interval_upper = active_intervals[new_active_interval_upper]
            active_intervals.pop(new_active_interval_upper)
        elif new_active_interval_upper + 1 in active_intervals:
            new_active_interval_upper = active_intervals[new_active_interval_upper + 1]
            active_intervals.pop(new_active_interval_upper + 1)
        active_intervals[new_active_interval_lower] = new_active_interval_upper
        active_intervals[new_active_interval_upper] = new_active_interval_lower
        active_red_tiles.append((coord1, (new_active_interval_lower, new_active_interval_upper)))
        active_red_tiles.append((coord2, (new_active_interval_lower, new_active_interval_upper)))
    else:
        # print("RIGHTEND", coord1, coord2)
        y_interval = (min(coord1_y, coord2_y), max(coord1_y, coord2_y))
        intervals_to_end = [y_interval]
        if 2*i+2 < len(coordinates) and coordinates[2*i+2][0] == coord1_x + 1:
            next_y_lower = min(coordinates[2*i+2][1], coordinates[2*i+3][1])
            next_y_upper= max(coordinates[2*i+2][1], coordinates[2*i+3][1])
            intervals_to_end = interval_subtract(y_interval[0], y_interval[1], next_y_lower, next_y_upper)
        new_active_red_tiles = []
        for (tile_x, tile_y), (lower_y, upper_y) in active_red_tiles:
            still_active = True
            for (lower_y_end, upper_y_end) in intervals_to_end:
                if tile_y >= lower_y_end and tile_y <= upper_y_end:
                    still_active = False
                    break
                elif upper_y_end < tile_y and upper_y_end >= lower_y:
                    lower_y = upper_y_end
                    if lower_y in active_intervals:
                        upper_end = active_intervals.pop(lower_y)
                        active_intervals[upper_end] = upper_y_end
                        active_intervals[upper_y_end] = upper_end
                elif lower_y_end > tile_y and lower_y_end <= upper_y:
                    upper_y = lower_y_end
                    if upper_y in active_intervals:
                        lower_end = active_intervals.pop(upper_y)
                        active_intervals[lower_end] = lower_y_end
                        active_intervals[lower_y_end] = lower_end
            if still_active:
                new_active_red_tiles.append(((tile_x, tile_y), (lower_y, upper_y)))
        active_red_tiles = new_active_red_tiles



with open('output.txt', 'w+') as out:
    out.write(str(max_area_found))