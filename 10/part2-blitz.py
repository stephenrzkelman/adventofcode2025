input = open('input.txt', 'r')
lines = [line.split() for line in input.read().splitlines()]

# import heapq
from ast import literal_eval
import sys
import math

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

heuristic_memo = {}

def button_press(joltage_config, button, num_times):
    new_joltage_config = list(joltage_config[:])
    for link in button:
        new_joltage_config[link] -= num_times
    return tuple(new_joltage_config)

class JoltageConfig:
    def __init__(self, cur_config, prev_num_presses, buttons_links, remaining_buttons_links_indices):
        self.cur_config = cur_config
        self.prev_num_presses = prev_num_presses
        self.buttons_links = buttons_links
        self.remaining_buttons_links_indices = remaining_buttons_links_indices
        global heuristic_memo
        if cur_config not in heuristic_memo:
            self.heuristic = self.compute_heuristic()
            heuristic_memo[cur_config] = self.heuristic
        else:
            self.heuristic = heuristic_memo[cur_config]

    def compute_heuristic(self):
        if self.lookupkey() not in heuristic_memo:
            heuristic_memo[self.lookupkey()] = max(self.dot_product_heuristic(), self.greedy_heuristic())
        return heuristic_memo[self.lookupkey()]

    def dot_product_heuristic(self):
        if max(self.cur_config) == 0:
            return 0
        def vector_magnitude(vector):
            return math.sqrt(sum([x**2 for x in vector]))
        def dot_product(v1, v2):
            return sum([v1[i] * v2[i] for i in (range(max(len(v1), len(v2))))])
        def make_binary_vector(one_indices, length):
            binary_vector = [0 for _ in range(length)]
            for index in one_indices:
                binary_vector[index] = 1
            return binary_vector
        max_dot_product = max([dot_product(self.cur_config, make_binary_vector(buttons_links[index], len(self.cur_config)))/vector_magnitude(self.cur_config) for index in self.remaining_buttons_links_indices])
        if max_dot_product == 0:
            return 1000000
        min_step_bound = math.ceil(vector_magnitude(self.cur_config)/max_dot_product)
        return min_step_bound

    def greedy_heuristic(self):
        num_ops = 0
        buttons_links_descending_size = sorted(
                [button_links for i, button_links in enumerate(self.buttons_links) if i in self.remaining_buttons_links_indices], 
                key=lambda links:len(links), 
                reverse=True
            )
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
        return (self.cur_config, tuple(self.remaining_buttons_links_indices))
        
def fewest_presses(goal_config, buttons_links):
    all_zeros = tuple([0 for _ in goal_config])
    if goal_config == all_zeros:
        return 0
    min_presses = sum(goal_config)
    end = JoltageConfig(goal_config, 0, buttons_links, set(range(len(buttons_links))))
    joltage_configs = LookupHeap([end])
    visited_configs  = {}
    opened_configs = {end.lookupkey(): end}        

    while ((joltage_configs.items and 
           joltage_configs.items[0].min_to_zero() < min_presses)):
        sys.stdout.write(f"\rQueue Length:\t{len(joltage_configs.items)}")
        next_joltage_config = joltage_configs.pop()
        opened_configs.pop(next_joltage_config.lookupkey())
        config_key = next_joltage_config.lookupkey()
        cur_config = next_joltage_config.cur_config
        prev_num_presses = next_joltage_config.prev_num_presses
        button_to_press_indices = next_joltage_config.remaining_buttons_links_indices
        if cur_config in visited_configs:
            visited_configs[config_key] = min(visited_configs[config_key], prev_num_presses)
        else:
            visited_configs[config_key] = prev_num_presses
        max_num_button_presses = max(cur_config)
        for button_to_press_index in button_to_press_indices:
            button_to_press = buttons_links[button_to_press_index]
            for link in button_to_press:
                max_num_button_presses = min(max_num_button_presses, cur_config[link])
            for sub_presses in range(max_num_button_presses + 1):
                new_config = button_press(cur_config, button_to_press, sub_presses)
                if new_config == all_zeros:
                    min_presses = min(min_presses, prev_num_presses + sub_presses)
                elif len(button_to_press_indices) == 1:
                    continue
                else:
                    neighbor = JoltageConfig(new_config, prev_num_presses + sub_presses, buttons_links, button_to_press_indices - {button_to_press_index})
                    neighbor_key = neighbor.lookupkey()
                    if neighbor_key in opened_configs:
                        if neighbor < opened_configs[neighbor_key] and neighbor.min_to_zero() < min_presses:
                            opened_configs[neighbor_key].update_prev_num_presses(neighbor.prev_num_presses)
                            joltage_configs.siftup(joltage_configs.reverse_index_lookup[neighbor_key])
                    elif neighbor.min_to_zero() < min_presses:
                        joltage_configs.push(neighbor)
                        opened_configs[neighbor_key] = neighbor
                    else:
                        visited_configs[neighbor_key] = min_presses + 1
    return min_presses

import time

original_start_time = time.perf_counter()



total_num_presses = 0
i = 0
for line in lines:
    lap_start_time = time.perf_counter()
    usable_buttons_memo = {}
    heuristic_memo = {}
    i += 1
    goal_config = literal_eval(f"({line[-1][1:-1]},)")
    buttons_links = []
    for button_links_string in line[1:-1]:
        button_links = literal_eval(button_links_string)
        if isinstance(button_links, int):
            buttons_links.append((button_links,))
        else:
            buttons_links.append(button_links)
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
