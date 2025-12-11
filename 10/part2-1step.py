input = open('input.txt', 'r')
lines = [line.split() for line in input.read().splitlines()]

# import heapq
from ast import literal_eval
import sys

class LookupHeap:
    def __init__(self, starter):
        self.items = starter if starter is not None else []
        self.reverse_index_lookup = {starter_item.lookupkey(): i for i, starter_item in enumerate(starter)} if starter is not None else {}

    def _swap(self, index1, index2):
        self.reverse_index_lookup[self.items[index1].lookupkey()] = index2
        self.reverse_index_lookup[self.items[index2].lookupkey()] = index1
        tmp = self.items[index1]
        self.items[index1] = self.items[index2]
        self.items[index2] = tmp

    def _poplast(self):
        self.reverse_index_lookup.pop(self.items[-1].lookupkey())
        return self.items.pop()
    
    def _append(self, new_item):
        self.reverse_index_lookup[new_item.lookupkey()] = len(self.items)
        self.items.append(new_item)
    
    def siftup(self, index):
        while self.items[index] < self.items[index//2]:
            self._swap(index, index//2)
            index = index//2

    def siftdown(self, index):
        while 2 * index + 1 < len(self.items):
            min_child_index = 2 * index + 1
            if 2 * index + 2 < len(self.items) and self.items[min_child_index] > self.items[min_child_index + 1]:
                min_child_index += 1
            self._swap(index, min_child_index)
            index = min_child_index

    def pop(self):
        self._swap(0, -1)
        popped = self._poplast()
        self.siftdown(0)
        return popped

    def push(self, item):
        self._append(item)
        self.siftup(len(self.items) - 1)

    def __str__(self):
        string = "["
        for item in self.items:
            string += str(item) + ", "
        string += "]"
        return string

reverse_heuristic_memo = {}
forward_heuristic_memo = {}

def button_press_reverse(joltage_config, button, num_times):
    new_joltage_config = list(joltage_config[:])
    for link in button:
        new_joltage_config[link] -= num_times
    return tuple(new_joltage_config)

def button_press_forward(joltage_config, button, num_times):
    new_joltage_config = list(joltage_config[:])
    for link in button:
        new_joltage_config[link] += num_times
    return tuple(new_joltage_config)
        
class ReverseJoltageConfig:
    def __init__(self, cur_config, prev_num_presses, buttons_links, last_button):
        self.cur_config = cur_config
        self.prev_num_presses = prev_num_presses
        self.last_button = last_button
        self.buttons_links = buttons_links
        global reverse_heuristic_memo
        if cur_config not in reverse_heuristic_memo:
            self.heuristic = self.compute_heuristic()
            reverse_heuristic_memo[cur_config] = self.heuristic
        else:
            self.heuristic = reverse_heuristic_memo[cur_config]

    def compute_heuristic(self):
        num_ops = 0
        buttons_links_descending_size = sorted(self.buttons_links[:self.last_button], key=lambda links:len(links), reverse=True)
        joltage_copy = list(self.cur_config)
        for button_links in buttons_links_descending_size:
            num_presses = 0
            for link in button_links:
                num_presses = max(num_presses, joltage_copy[link])
                joltage_copy[link] = 0
            num_ops += num_presses
        return num_ops

    def min_to_zero(self):
        return self.prev_num_presses + self.heuristic
    
    def __lt__(self, other):
        if self.min_to_zero() < other.min_to_zero():
            return True
        elif self.min_to_zero == other.min_to_zero():
            return self.prev_num_presses > other.prev_num_presses
        else:
            return False
    
    def update_prev_num_presses(self, new_num_presses):
        self.prev_num_presses = new_num_presses

    def lookupkey(self):
        return self.cur_config
        

class ForwardJoltageConfig:
    def __init__(self, cur_config, prev_num_presses, buttons_links, goal_config, next_button):
        self.goal_config = goal_config
        self.cur_config = cur_config
        self.prev_num_presses = prev_num_presses
        self.buttons_links = buttons_links
        self.next_button = next_button
        global forward_heuristic_memo
        if cur_config not in forward_heuristic_memo:
            self.heuristic = self.compute_heuristic()
            forward_heuristic_memo[cur_config] = self.heuristic
        else:
            self.heuristic = forward_heuristic_memo[cur_config]
        
    def compute_heuristic(self):
        num_ops = 0
        buttons_links_descending_size = sorted(self.buttons_links[self.next_button:], key=lambda links:len(links), reverse=True)
        joltage_copy = list(self.cur_config)
        for button_links in buttons_links_descending_size:
            num_presses = 0
            for link in button_links:
                num_presses = max(num_presses, goal_config[link] - joltage_copy[link])
                joltage_copy[link] = goal_config[link]
            num_ops += num_presses
        return num_ops

    def min_to_goal(self):
        return self.prev_num_presses + self.heuristic
    
    def __lt__(self, other):
        if self.min_to_goal() < other.min_to_goal():
            return True
        elif self.min_to_goal == other.min_to_goal():
            return self.prev_num_presses > other.prev_num_presses
        else:
            return False
    
    def update_prev_num_presses(self, new_num_presses):
        self.prev_num_presses = new_num_presses

    def lookupkey(self):
        return self.cur_config
    
    def __str__(self):
        return f"(config: {self.cur_config}, press count:{self.prev_num_presses})"


def fewest_presses(goal_config, buttons_links):
    buttons_links.sort(key=lambda links: len(links), reverse=True)
    all_zeros = tuple([0 for _ in goal_config])
    if goal_config == all_zeros:
        return 0
    min_presses = sum(goal_config)
    start = ForwardJoltageConfig(all_zeros, 0, buttons_links, goal_config, 0)
    end = ReverseJoltageConfig(goal_config, 0, buttons_links, len(buttons_links))
    joltage_configs_reverse = LookupHeap([end])
    joltage_configs_forward = LookupHeap([start])
    visited_configs_forward = {}
    visited_configs_reverse  = {}
    opened_configs_reverse = {(end.cur_config, len(buttons_links)): end}
    opened_configs_forward = {(start.cur_config, -1): start}
    def process_reverse():
        nonlocal min_presses
        sys.stdout.write(f"\rQueue Length:\t{len(joltage_configs_reverse.items)}")
        next_reverse_joltage_config = joltage_configs_reverse.pop()
        cur_config = next_reverse_joltage_config.cur_config
        prev_num_presses = next_reverse_joltage_config.prev_num_presses
        button_to_press_index = next_reverse_joltage_config.last_button - 1
        button_to_press = buttons_links[button_to_press_index]
        if cur_config in visited_configs_forward:
            min_presses = min(min_presses, visited_configs_forward[cur_config] + prev_num_presses)
        if cur_config in visited_configs_reverse:
            visited_configs_reverse[cur_config] = min(visited_configs_reverse[cur_config], prev_num_presses)
        else:
            visited_configs_reverse[cur_config] = prev_num_presses
        max_num_button_presses = max(cur_config)
        for link in button_to_press:
            max_num_button_presses = min(max_num_button_presses, cur_config[link])
        for sub_presses in range(max_num_button_presses + 1):
            new_config = button_press_reverse(cur_config, button_to_press, sub_presses)
            if new_config == all_zeros:
                min_presses = min(min_presses, prev_num_presses + sub_presses)
            elif new_config in visited_configs_forward:
                min_presses = min(min_presses, visited_configs_forward[new_config] + prev_num_presses + sub_presses)
            else:
                neighbor = ReverseJoltageConfig(new_config, prev_num_presses + sub_presses, buttons_links, button_to_press_index)
                if button_to_press_index <= 0:
                    return
                elif (new_config, button_to_press_index) in opened_configs_reverse:
                    if neighbor < opened_configs_reverse[(new_config, button_to_press_index)] and neighbor.min_to_zero() < min_presses:
                        opened_configs_reverse[(new_config, button_to_press_index)].update_prev_num_presses(neighbor.prev_num_presses)
                        joltage_configs_reverse.siftup(joltage_configs_reverse.reverse_index_lookup[new_config])
                elif neighbor.min_to_zero() < min_presses:
                    joltage_configs_reverse.push(neighbor)
                    opened_configs_reverse[(new_config, button_to_press_index)] = neighbor
                else:
                    visited_configs_reverse[neighbor.cur_config] = min_presses + 1

    def process_forward():
        nonlocal min_presses
        next_forward_joltage_config = joltage_configs_forward.pop()
        cur_config = next_forward_joltage_config.cur_config
        prev_num_presses = next_forward_joltage_config.prev_num_presses
        button_to_press_index = next_forward_joltage_config.next_button
        button_to_press = buttons_links[button_to_press_index]
        if cur_config in visited_configs_reverse:
            min_presses = min(min_presses, visited_configs_reverse[cur_config] + prev_num_presses)
        if cur_config in visited_configs_forward:
            visited_configs_forward[cur_config] = min(visited_configs_forward[cur_config], prev_num_presses)
        else:
            visited_configs_forward[cur_config] = prev_num_presses
        max_num_button_presses = max(goal_config)
        for link in button_to_press:
            max_num_button_presses = min(max_num_button_presses, goal_config[link] - cur_config[link])
        for sub_presses in range(max_num_button_presses + 1):
            new_config = button_press_forward(cur_config, button_to_press, sub_presses)
            if new_config == goal_config:
                min_presses = min(min_presses, prev_num_presses + sub_presses)
            elif new_config in visited_configs_reverse:
                    min_presses = min(min_presses, visited_configs_reverse[new_config] + prev_num_presses + sub_presses)
            else:
                next_button_to_press = button_to_press_index + 1
                neighbor = ForwardJoltageConfig(new_config, prev_num_presses + sub_presses, buttons_links, goal_config, next_button_to_press)
                if next_button_to_press >= len(buttons_links):
                    return
                elif (new_config, next_button_to_press) in opened_configs_forward:
                    if neighbor < opened_configs_forward[(new_config, next_button_to_press)] and neighbor.min_to_goal() < min_presses:
                        opened_configs_forward[(new_config, next_button_to_press)].update_prev_num_presses(neighbor.prev_num_presses)
                        joltage_configs_forward.siftup(joltage_configs_forward.reverse_index_lookup[new_config])
                elif neighbor.min_to_goal() < min_presses:
                    joltage_configs_forward.push(neighbor)
                    opened_configs_forward[(new_config, next_button_to_press)] = neighbor
                else:
                    visited_configs_forward[neighbor.cur_config] = min_presses + 1

    while ((joltage_configs_forward.items and 
           joltage_configs_forward.items[0].min_to_goal() < min_presses)):
        if (joltage_configs_reverse.items and joltage_configs_reverse.items[0].min_to_zero() < min_presses):
            process_reverse()
        if (joltage_configs_forward.items and joltage_configs_forward.items[0].min_to_goal() < min_presses):
            process_forward()
    return min_presses

import time

original_start_time = time.perf_counter()



total_num_presses = 0
i = 0
for line in lines:
    lap_start_time = time.perf_counter()
    reverse_usable_buttons_memo = {}
    reverse_heuristic_memo = {}
    i += 1
    goal_config = literal_eval(f"({line[-1][1:-1]},)")
    buttons_links = []
    for button_links_string in line[1:-1]:
        button_links = literal_eval(button_links_string)
        if isinstance(button_links, int):
            buttons_links.append(set([button_links]))
        else:
            buttons_links.append(set(button_links))
    print()
    fewest = fewest_presses(goal_config, buttons_links)
    print()
    total_num_presses += fewest
    lap_end_time = time.perf_counter()
    print(i, end="\t")
    print(f"press_count: {fewest}", end='\t')
    print(f"lap: {lap_end_time - lap_start_time}")

final_end_time = time.perf_counter()
elapsed_time = final_end_time - original_start_time
print(f"Elapsed time: {elapsed_time:.4f} seconds")   


with open('output.txt', 'w+') as out:
    out.write(str(total_num_presses))
