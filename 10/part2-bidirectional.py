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

enumerated_stars_and_bars = {}

def stars_and_bars_enumerate(bins, total):
    if (bins, total) in enumerated_stars_and_bars:
        return enumerated_stars_and_bars[(bins, total)]
    if bins == 1:
        enumerated_stars_and_bars[(bins, total)] = [(total,)]
        return [(total,)]
    all_configurations = []
    for i in range(total + 1):
        all_configurations += [[i, tail] for tail in stars_and_bars_enumerate(bins - 1, total - i)]
    enumerated_stars_and_bars[(bins, total)] = all_configurations
    return all_configurations

reverse_usable_buttons_memo = {}
reverse_buttons_to_use_memo = {}
reverse_min_remaining_joltage_memo = {}
reverse_heuristic_memo = {}
forward_usable_buttons_memo = {}
forward_buttons_to_use_memo = {}
forward_min_remaining_joltage_memo = {}
forward_heuristic_memo = {}

def button_press_reverse(joltage_config, buttons, button_presses):
    new_joltage_config = list(joltage_config[:])
    nested_button_presses = button_presses
    for button in buttons:
        for link in button:
            new_joltage_config[link] -= nested_button_presses[0]
        if len(nested_button_presses) > 1:
            nested_button_presses = nested_button_presses[1]
    return tuple(new_joltage_config)

def button_press_forward(joltage_config, buttons, button_presses):
    new_joltage_config = list(joltage_config[:])
    nested_button_presses = button_presses
    for button in buttons:
        for link in button:
            new_joltage_config[link] += nested_button_presses[0]
        if len(nested_button_presses) > 1:
            nested_button_presses = nested_button_presses[1]
    return tuple(new_joltage_config)
        
class ReverseJoltageConfig:
    def __init__(self, cur_config, prev_num_presses, buttons_links, max_min):
        self.cur_config = cur_config
        self.prev_num_presses = prev_num_presses
        global reverse_usable_buttons_memo
        global reverse_buttons_to_use_memo
        global reverse_min_remaining_joltage_memo
        global reverse_heuristic_memo
        if cur_config not in reverse_usable_buttons_memo:
            zeroed_indices = set([])
            min_remaining_joltage = 1000000
            min_remaining_joltage_index = -1
            for i in range(len(cur_config)):
                if cur_config[i] == 0:
                    zeroed_indices.add(i)
                elif cur_config[i] < min_remaining_joltage:
                    min_remaining_joltage = cur_config[i]
                    min_remaining_joltage_index = i
            buttons_to_use = []
            all_usable_buttons = []
            for button_links in buttons_links:
                if len(zeroed_indices.intersection(button_links)) == 0:
                    all_usable_buttons.append(button_links)
                    if min_remaining_joltage_index in button_links:
                        buttons_to_use.append(button_links)
                        
            self.usable_buttons = all_usable_buttons
            self.buttons_to_use = buttons_to_use
            self.min_remaining_joltage = min_remaining_joltage
            reverse_usable_buttons_memo[cur_config] = all_usable_buttons
            reverse_buttons_to_use_memo[cur_config] = all_usable_buttons
            reverse_min_remaining_joltage_memo[cur_config] = min_remaining_joltage
            if len(self.buttons_to_use) == 0:
                self.heuristic = max_min + 1
            else:
                self.heuristic = self.compute_heuristic()
            reverse_heuristic_memo[cur_config] = self.heuristic
        else:
            self.usable_buttons = reverse_usable_buttons_memo[cur_config]
            self.buttons_to_use = reverse_buttons_to_use_memo[cur_config]
            self.min_remaining_joltage = reverse_min_remaining_joltage_memo[cur_config]
            self.heuristic = reverse_heuristic_memo[cur_config]
        

    def compute_heuristic(self):
        num_ops = 0
        local_cur_config = list(self.cur_config)
        self.usable_buttons.sort(key=lambda x: len(x))
        for button in reversed(self.usable_buttons):
            num_presses = 0
            for link in button:
                num_presses = max(num_presses, local_cur_config[link])
                local_cur_config[link] = 0
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
    def __init__(self, cur_config, prev_num_presses, buttons_links, max_min, goal_config):
        self.goal_config = goal_config
        self.cur_config = cur_config
        self.prev_num_presses = prev_num_presses
        global forward_usable_buttons_memo
        global forward_buttons_to_use_memo
        global forward_min_remaining_joltage_memo
        global forward_heuristic_memo
        if cur_config not in usable_buttons_memo:
            maxed_indices = set([])
            min_remaining_joltage = 1000000
            min_remaining_joltage_index = -1
            for i in range(len(cur_config)):
                if cur_config[i] == goal_config[i]:
                    maxed_indices.add(i)
                elif goal_config[i] - cur_config[i] < min_remaining_joltage:
                    min_remaining_joltage = goal_config[i] - cur_config[i]
                    min_remaining_joltage_index = i
            buttons_to_use = []
            all_usable_buttons = []
            for button_links in buttons_links:
                if len(maxed_indices.intersection(button_links)) == 0:
                    all_usable_buttons.append(button_links)
                    if min_remaining_joltage_index in button_links:
                        buttons_to_use.append(button_links)
                        
            self.usable_buttons = all_usable_buttons
            self.buttons_to_use = buttons_to_use
            self.min_remaining_joltage = min_remaining_joltage
            forward_usable_buttons_memo[cur_config] = all_usable_buttons
            forward_buttons_to_use_memo[cur_config] = all_usable_buttons
            forward_min_remaining_joltage_memo[cur_config] = min_remaining_joltage
            if len(self.buttons_to_use) == 0:
                self.heuristic = max_min + 1
            else:
                self.heuristic = self.compute_heuristic()
            forward_heuristic_memo[cur_config] = self.heuristic
        else:
            self.usable_buttons = forward_usable_buttons_memo[cur_config]
            self.buttons_to_use = forward_buttons_to_use_memo[cur_config]
            self.min_remaining_joltage = forward_min_remaining_joltage_memo[cur_config]
            self.heuristic = forward_heuristic_memo[cur_config]
        

    def compute_heuristic(self):
        num_ops = 0
        local_cur_config = list(self.cur_config)
        self.usable_buttons.sort(key=lambda x: len(x))
        for button in reversed(self.usable_buttons):
            num_presses = 0
            for link in button:
                num_presses = max(num_presses, goal_config[link] - local_cur_config[link])
                local_cur_config[link] = goal_config[link]
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
        return f"({self.cur_config}, {self.prev_num_presses})"
        


def fewest_presses(goal_config, buttons_links):
    all_zeros = tuple([0 for _ in goal_config])
    if goal_config == all_zeros:
        return 0
    min_presses = sum(goal_config)
    start = ForwardJoltageConfig(all_zeros, 0, buttons_links, min_presses, goal_config)
    end = ReverseJoltageConfig(goal_config, 0, buttons_links, min_presses)
    joltage_configs_reverse = LookupHeap([end])
    joltage_configs_forward = LookupHeap([start])
    visited_configs = {}
    opened_configs_reverse = {end.cur_config: end}
    opened_configs_forward = {start.cur_config: start}
    def process_reverse():
        nonlocal min_presses
        sys.stdout.write(f"\rQueue Length:\t{len(joltage_configs_reverse.items)}")
        cur_config = joltage_configs_reverse.pop()
        joltage_config = cur_config.cur_config
        prev_num_presses = cur_config.prev_num_presses
        if joltage_config in visited_configs:
            if visited_configs[joltage_config] >= 0:
                min_presses = min(min_presses, visited_configs[joltage_config] + prev_num_presses)
            else:
                print("ALERT!")
            return
        visited_configs[joltage_config] = -prev_num_presses - 1
        buttons_to_use = cur_config.buttons_to_use
        button_presses_configs = stars_and_bars_enumerate(len(buttons_to_use), cur_config.min_remaining_joltage)
        for button_presses in button_presses_configs:
            new_config = button_press_reverse(joltage_config, buttons_to_use, button_presses)
            if new_config == all_zeros:
                min_presses = min(min_presses, prev_num_presses + cur_config.min_remaining_joltage)
            elif new_config in visited_configs:
                if visited_configs[new_config] >= 0:
                    min_presses = min(min_presses, visited_configs[new_config] + prev_num_presses)
            else:
                neighbor = ReverseJoltageConfig(new_config, prev_num_presses + cur_config.min_remaining_joltage, buttons_links, min_presses)
                if new_config in opened_configs_reverse:
                    if neighbor < opened_configs_reverse[new_config] and neighbor.min_to_zero() < min_presses:
                        opened_configs_reverse[new_config].update_prev_num_presses(neighbor.prev_num_presses)
                        joltage_configs_reverse.siftup(joltage_configs_reverse.reverse_index_lookup[new_config])
                elif neighbor.min_to_zero() < min_presses:
                    joltage_configs_reverse.push(neighbor)
                    opened_configs_reverse[new_config] = neighbor
                else:
                    visited_configs[neighbor.cur_config] = min_presses + 1

    def process_forward():
        nonlocal min_presses
        cur_config = joltage_configs_forward.pop()
        joltage_config = cur_config.cur_config
        prev_num_presses = cur_config.prev_num_presses
        if joltage_config in visited_configs:
            if visited_configs[joltage_config] < 0:
                min_presses = min(min_presses, -visited_configs[joltage_config] - 1 + prev_num_presses)
            else:
                print("ALERT!")
            return
        buttons_to_use = cur_config.buttons_to_use
        button_presses_configs = stars_and_bars_enumerate(len(buttons_to_use), cur_config.min_remaining_joltage)
        for button_presses in button_presses_configs:
            new_config = button_press_forward(joltage_config, buttons_to_use, button_presses)
            if new_config == goal_config:
                min_presses = min(min_presses, prev_num_presses + cur_config.min_remaining_joltage)
            elif new_config in visited_configs:
                if visited_configs[new_config] < 0:
                    min_presses = min(min_presses, -visited_configs[joltage_config] - 1 + prev_num_presses)
            else:
                neighbor = ForwardJoltageConfig(new_config, prev_num_presses + cur_config.min_remaining_joltage, buttons_links, min_presses, goal_config)
                if new_config in opened_configs_forward:
                    if neighbor < opened_configs_forward[new_config] and neighbor.min_to_goal() < min_presses:
                        opened_configs_forward[new_config].update_prev_num_presses(neighbor.prev_num_presses)
                        joltage_configs_forward.siftup(joltage_configs_forward.reverse_index_lookup[new_config])
                elif neighbor.min_to_goal() < min_presses:
                    joltage_configs_forward.push(neighbor)
                    opened_configs_forward[new_config] = neighbor
                else:
                    visited_configs[neighbor.cur_config] = min_presses + 1

    while ((joltage_configs_reverse.items and 
           joltage_configs_reverse.items[0].min_to_zero() < min_presses) or
           (joltage_configs_forward.items and 
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
    usable_buttons_memo = {}
    buttons_to_use_memo = {}
    heuristic_memo = {}
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
