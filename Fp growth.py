import numpy as np
import time
from numba import jit
import numba as nb
from multiprocessing import Pool
from itertools import combinations
start_time = time.time()
file_path = 'date/test2.dat' 
data =[]
with open(file_path, 'r') as file:
    for line in file:
        row = [int(x) for x in line.strip().split()]
        data.append(row)
#debug
# for i in data:
#     print(i)

# #count item count in itemCnt 
itemCnt = np.zeros(27,dtype=int)
for i in data:
    for j in i:
        itemCnt[j]+=1

requireSize = 2
class TreeNode:
    def __init__(self, value=None):
        self.value = value
        self.count = 1
        self.children = {}
        self.parent = None

class Trie:
    def __init__(self):
        self.root = TreeNode()  # Root is a null node

    def insert(self, array):
        node = self.root
        for element in array:
            if itemCnt[element] < requireSize:
                continue
            if element not in node.children:
                new_node = TreeNode(element)
                new_node.parent = node  # Set parent for traversal
                node.children[element] = new_node
            node = node.children[element]
            node.count += 1

    def get_all_path(self):
        # nodeCnt={}
        paths = []
        self.dfs(self.root, [], paths)
        return paths

    def dfs(self, node, path, paths):
        if not node.children:  # If no children, it's a leaf
            paths.append(path.copy())
        for child in node.children.values():
            path.append(child)
            # nodeCnt[child.value]=child.cnt
            self.dfs(child, path, paths)
            path.pop()  # Remove the last element for backtracking
    

def print_trie(node, level=0):
    # Base case: if the node is None, return
    if node is None:
        return

    # Print the current node
    indent = " " * (level * 4)
    node_info = f"{indent}Node: {node.value}, Count: {node.count}" if node.value is not None else "Root"
    print(node_info)

    # Recursively print each child
    for child in node.children.values():
        print_trie(child, level + 1)

def generate_combinations(arr):
    result_set = []
    for r in range(1, len(arr) + 1):
        for combo in combinations(arr, r):
            result_set.append(combo)
    return result_set
FPTree=Trie()
for row in data:
    row = sorted(row,key=lambda x: itemCnt[x], reverse=True)
    # print(row)
    FPTree.insert(row)

# print_trie(FPTree.root)

Allpathnode = FPTree.get_all_path()
print(Allpathnode)

frequent_item_set={}
for nodes in Allpathnode:
    nodeCnt={}
    path = []
    # frequent_item_set={}
    # path.clear()
    # nodeCnt.clear()
    for node in nodes:
        path.append(node.value)
        nodeCnt[node.value]=node.count
    Allcomb = generate_combinations(path)
    for comb in Allcomb:
        comb_set = frozenset(comb)
        minval = 10000 
        for element in comb_set:
            minval = min(minval,nodeCnt[element])
        if comb_set not in frequent_item_set:
            frequent_item_set[comb_set] = minval
        else:
            frequent_item_set[comb_set] +=minval
#     # Allpath.append(FPTree.traverse_to_root(leaf))


for key, value in frequent_item_set.items():
    print(f'键：{key}，值：{value}')

