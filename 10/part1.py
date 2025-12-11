input = open('input.txt', 'r')
lines = [line.split() for line in input.read().splitlines()]

from collections import deque
from ast import literal_eval

def toggle(string_list, index):
    if string_list[index] == '.':
        string_list[index] = '#'
    else:
        string_list[index] = '.'

def fewest_presses(goal_config, buttons_links):
    all_off = "."*len(goal_config)
    if goal_config == all_off:
        return 0
    states = deque([(all_off,0)])
    visited = set([all_off])
    while states:
        cur_state, prev_num_presses = states.popleft()
        for button_links in buttons_links:
            next_state_list = list(cur_state)
            for link in button_links:
                toggle(next_state_list, link)
            next_state = "".join(next_state_list)
            if next_state in visited:
                continue
            elif next_state == goal_config:
                return prev_num_presses + 1
            else:
                states.append((next_state, prev_num_presses + 1))
                visited.add(next_state)

total_num_presses = 0
for line in lines:
    goal_config = line[0][1:-1]
    buttons_links = []
    for button_links_string in line[1:-1]:
        button_links = literal_eval(button_links_string)
        if isinstance(button_links, int):
            buttons_links.append((button_links,))
        else:
            buttons_links.append(button_links)
    total_num_presses += fewest_presses(goal_config, buttons_links)

with open('output.txt', 'w+') as out:
    out.write(str(total_num_presses))