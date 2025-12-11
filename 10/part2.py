input = open('input.txt', 'r')
lines = [line.split() for line in input.read().splitlines()]

# import heapq
from ast import literal_eval
import sys
import math

class LookupHeap:
    def __init__(self, starter):
        self.items = starter if starter is not None else []
        self.reverse_index_lookup = {}

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

usable_buttons_memo = {}
buttons_to_use_memo = {}
min_remaining_joltage_memo = {}
heuristic_memo = {}

def button_press_reverse(joltage_config, buttons, button_presses):
    new_joltage_config = list(joltage_config[:])
    nested_button_presses = button_presses
    for button in buttons:
        for link in button:
            new_joltage_config[link] -= nested_button_presses[0]
        if len(nested_button_presses) > 1:
            nested_button_presses = nested_button_presses[1]
    return tuple(new_joltage_config)
    
class JoltageConfigdfs:
    def __init__(self, cur_config, prev_num_presses, biggest_button):
        self.cur_config = cur_config
        self.prev_num_presses = prev_num_presses
        self.biggest_button = biggest_button

    def min_to_zero(self):
        return self.prev_num_presses + sum(self.cur_config)//self.biggest_button
    
    def __lt__(self, other):
        if self.prev_num_presses > other.prev_num_presses:
            return True
        elif self.prev_num_presses == other.prev_num_presses:
            return self.min_to_zero() < other.min_to_zero()
        else:
            return False
        
class JoltageConfigAstar:
    def __init__(self, cur_config, prev_num_presses, buttons_links, max_min):
        self.cur_config = cur_config
        self.prev_num_presses = prev_num_presses
        global usable_buttons_memo
        global buttons_to_use_memo
        if cur_config not in usable_buttons_memo:
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
            usable_buttons_memo[cur_config] = all_usable_buttons
            buttons_to_use_memo[cur_config] = all_usable_buttons
            min_remaining_joltage_memo[cur_config] = min_remaining_joltage
            if len(self.buttons_to_use) == 0:
                self.heuristic = max_min + 1
            else:
                self.heuristic = self.compute_heuristic()
            heuristic_memo[cur_config] = self.heuristic
        else:
            self.usable_buttons = usable_buttons_memo[cur_config]
            self.buttons_to_use = buttons_to_use_memo[cur_config]
            self.min_remaining_joltage = min_remaining_joltage_memo[cur_config]
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
        max_dot_product = max([dot_product(self.cur_config, make_binary_vector(button_links, len(self.cur_config)))/vector_magnitude(self.cur_config) for button_links in self.usable_buttons])
        if max_dot_product == 0:
            return 1000000
        min_step_bound = math.ceil(vector_magnitude(self.cur_config)/max_dot_product)
        return min_step_bound
    
    def greedy_heuristic(self):
        num_ops = 0
        remaining_state = list(self.cur_config[:])
        while max(remaining_state) > 0:
            nonzero_elts = set([])
            for i, elt in enumerate(remaining_state):
                if elt > 0:
                    nonzero_elts.add(i)
            max_overlap = None
            max_overlap_size = 0
            max_overlap_proportion = 0
            min_nonzero_in_max_overlap = 1000000
            for button in self.usable_buttons:
                overlap = button.intersection(nonzero_elts)
                overlap_size = len(overlap)
                overlap_proportion = len(overlap)/len(button)
                min_nonzero_in_overlap = min([remaining_state[i] for i in overlap]) if overlap_size > 0 else -1
                if (overlap_proportion, overlap_size, min_nonzero_in_overlap) > (max_overlap_proportion, max_overlap_size, min_nonzero_in_max_overlap):
                    max_overlap = overlap
                    max_overlap_proportion = overlap_proportion
                    max_overlap_size = overlap_size
                    min_nonzero_in_max_overlap = min_nonzero_in_overlap
            if max_overlap_size == 0:
                return 1000000
            for index in max_overlap:
                remaining_state[index] -= min_nonzero_in_max_overlap
            num_ops += min_nonzero_in_max_overlap
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
        


def fewest_presses(goal_config, buttons_links):
    all_zeros = tuple([0 for _ in goal_config])
    if goal_config == all_zeros:
        return 0
    min_presses = sum(goal_config)
    start = JoltageConfigAstar(goal_config, 0, buttons_links, min_presses)
    joltage_configs_astar = LookupHeap([start])
    visited_configs_astar = set([])
    opened_configs_astar = {start.cur_config: start}
    while joltage_configs_astar.items and joltage_configs_astar.items[0].min_to_zero() < min_presses:
        sys.stdout.write(f"\rQueue Length:\t{len(joltage_configs_astar.items)}")
        cur_config = joltage_configs_astar.pop()
        joltage_config = cur_config.cur_config
        visited_configs_astar.add(joltage_config)
        prev_num_presses = cur_config.prev_num_presses
        buttons_to_use = cur_config.buttons_to_use
        button_presses_configs = stars_and_bars_enumerate(len(buttons_to_use), cur_config.min_remaining_joltage)
        for button_presses in button_presses_configs:
            new_config = button_press_reverse(joltage_config, buttons_to_use, button_presses)
            if new_config == all_zeros:
                min_presses = min(min_presses, prev_num_presses + cur_config.min_remaining_joltage)
            elif new_config in visited_configs_astar:
                continue
            else:
                neighbor = JoltageConfigAstar(new_config, prev_num_presses + cur_config.min_remaining_joltage, buttons_links, min_presses)
                if new_config in opened_configs_astar:
                    if neighbor < opened_configs_astar[new_config] and neighbor.min_to_zero() < min_presses:
                        opened_configs_astar[new_config].update_prev_num_presses(neighbor.prev_num_presses)
                        joltage_configs_astar.siftup(joltage_configs_astar.reverse_index_lookup[new_config])
                elif neighbor.min_to_zero() < min_presses:
                    joltage_configs_astar.push(neighbor)
                    opened_configs_astar[new_config] = neighbor
                else:
                    visited_configs_astar.add(neighbor.cur_config)
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


#######################
# PLAIN DFS
#######################
# cur_config = heapq.heappop(joltage_configs_dfs)
        # joltage_config = cur_config.cur_config
        # prev_num_presses = cur_config.prev_num_presses
        # zeroed_indices = set([])
        # min_remaining_joltage = 1000000
        # min_remaining_joltage_index = -1
        # for i in range(len(joltage_config)):
        #     if i not in zeroed_indices:
        #         if joltage_config[i] == 0:
        #             zeroed_indices.add(i)
        #         elif joltage_config[i] < min_remaining_joltage:
        #             min_remaining_joltage = joltage_config[i]
        #             min_remaining_joltage_index = i
        # buttons_to_use = []
        # for button_links in buttons_links:
        #     if min_remaining_joltage_index in button_links and len(zeroed_indices.intersection(button_links)) == 0:
        #         buttons_to_use.append(button_links)
        # if len(buttons_to_use) == 0:
        #     continue
        # button_presses_configs = stars_and_bars_enumerate(len(buttons_to_use), min_remaining_joltage)
        # for button_presses in button_presses_configs:
        #     new_config = button_press_reverse(joltage_config, buttons_to_use, button_presses)
        #     if new_config == all_zeros:
        #         min_presses = min(min_presses, prev_num_presses + min_remaining_joltage)
        #     elif new_config in visited_configs_dfs:
        #         if visited_configs_dfs[new_config] > prev_num_presses + min_remaining_joltage:
        #             visited_configs_dfs[new_config] = prev_num_presses + min_remaining_joltage
        #             heapq.heappush(joltage_configs_dfs, JoltageConfigdfs(new_config, prev_num_presses + min_remaining_joltage, biggest_button))
        #     else:
        #         visited_configs_dfs[new_config] = prev_num_presses + min_remaining_joltage
        #         heapq.heappush(joltage_configs_dfs, JoltageConfigdfs(new_config, prev_num_presses + min_remaining_joltage, biggest_button))
