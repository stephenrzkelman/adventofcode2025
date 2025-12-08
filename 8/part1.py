input = open('input.txt', 'r')
lines = input.read().splitlines()

coordinates = [tuple([int(coord) for coord in coords.split(',')]) for coords in lines]
distances = []
for index_1, box_1 in enumerate(coordinates[:-1]):
    for index_2, box_2 in enumerate(coordinates[index_1+1:]):
        true_index_2 = index_1 + index_2 + 1
        distances.append((
            (box_1[0]-box_2[0])**2 + (box_1[1]-box_2[1])**2 + (box_1[2]-box_2[2])**2,
            (index_1, true_index_2)
        ))

class Union_Find:
    def __init__(self, num_elts):
        self.parents = {
            elt: elt for elt in range(num_elts)
        }
        self.sizes = {
            elt: 1 for elt in range(num_elts)
        }
        self.parent_elts = set([
            elt for elt in range(num_elts)
        ])

    def lookup_parent(self, elt):
        cur = elt
        in_path = []
        while cur != self.parents[cur]:
            in_path.append(cur)
            cur = self.parents[cur]
        final_parent = cur
        for intermediate in in_path:
            self.parents[intermediate] = final_parent
        return final_parent
    
    def merge_groups(self, elt1, elt2):
        parent1 = self.lookup_parent(elt1)
        parent2 = self.lookup_parent(elt2)
        if parent1 != parent2:
            self.parents[parent2] = parent1
            self.sizes[parent1] += self.sizes[parent2]
            self.parent_elts.remove(parent2)

circuits = Union_Find(len(coordinates))
distances.sort()
num_wires = 1000
for distance, (index_1, index_2) in distances[:num_wires]:
    circuits.merge_groups(index_1, index_2)
group_sizes = [circuits.sizes[circuit_parent] for circuit_parent in circuits.parent_elts]
group_sizes.sort(reverse=True)


with open('output.txt', 'w+') as out:
    out.write(str(group_sizes[0] * group_sizes[1] * group_sizes[2]))