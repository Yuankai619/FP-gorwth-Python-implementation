import numpy as np
import time
from numba import jit
import numba as nb
from multiprocessing import Pool

start_time = time.time()
file_path = 'date/test2.dat'
SIZE =8125  
def int_to_binary(n):
    rs=""
    while n:
        if n&1:
            rs+='1'
        else:
            rs+='0'
        n>>=1
    return rs[::-1]
# read data and transform to bit 
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
        self.root = TreeNode()
        self.leaves = []

    def insert(self, array):
        node = self.root
        for element in array:
            if itemCnt[element] < requireSize:
                continue
            if element not in node.children:
                new_node = TreeNode(element)
                new_node.parent = node
                node.children[element] = new_node
            else:
                node.children[element].count += 1
            node = node.children[element]

        # Update the leaves
        self._update_leaves(node)

    def _update_leaves(self, node):
        # Remove the node from leaves if it has children
        if node.children and node in self.leaves:
            self.leaves.remove(node)

        # Traverse up to remove any ancestor nodes that are no longer leaves
        current = node.parent
        while current and current != self.root:
            if current.children and current in self.leaves:
                self.leaves.remove(current)
            current = current.parent

        # Add the node as a leaf if it's not in leaves and has no children
        if not node.children and node not in self.leaves:
            self.leaves.append(node)

    def path_to_root(self, leaf):
        path = []
        node = leaf
        while node.parent is not None:
            path.append(node.value)
            node = node.parent
        return path[::-1]
    def remove_leaf(self, leaf):
        if leaf is None or leaf.parent is None or leaf not in self.leaves:
            return
        parent = leaf.parent
        del parent.children[leaf.value]
        self.leaves.remove(leaf)
        self._update_leaves(parent)

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
FPTree=Trie()
for row in data:
    row = sorted(row,key=lambda x: itemCnt[x], reverse=True)
    print(row)
    FPTree.insert(row)

print_trie(FPTree.root)

tops = np.zeros(27,dtype=int)
itemSets = np.zeros((27,27),dtype=int)
setsCnt = np.zeros((27,27),dtype=int)

while FPTree.root.children:#remove leaf until tree is Null
    # print("Leaves: ")
    # for i in FPTree.leaves:
    #     print(i.value,end=",")
    # print("")
    leaves = list(FPTree.leaves)
    for leaf in leaves:
        # print(f"before: {leaf.value}")
        path = FPTree.path_to_root(leaf)
        # print(f"after: {leaf.value}")
        # print(path)
        for i in path:
            setsCnt[leaf.value][i]+=leaf.count
    for leaf in leaves:
        FPTree.remove_leaf(leaf)
    # print_trie(FPTree.root)
    # print("-"*10)
for i in range(1,27):
    for j in range(1,27):
        if setsCnt[i][j] >= requireSize:
            itemSets[i][tops[i]]=j
            tops[i]+=1
# print_trie(FPTree.root)
for i in range(1,27):
    for j in range(0,tops[i]+1):
        print(itemSets[i][j],end=" ")
    print("")
