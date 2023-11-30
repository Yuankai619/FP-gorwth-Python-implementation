import numpy as np
import time
from numba import jit
import numba as nb
from multiprocessing import Pool

start_time = time.time()
file_path = 'date/mushroom.dat'
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
itemCnt = np.zeros(120,dtype=int)
for i in data:
    for j in i:
        itemCnt[j]+=1

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

    def insert(self, items):
        node = self.root
        for element in items:
            if element not in node.children:
                new_node = TreeNode(element)
                new_node.parent = node
                node.children[element] = new_node
            else:
                node.children[element].count += 1
            node = node.children[element]
        self.leaves.append(node)

    def traverse_to_root(self, leaf):
        path = []
        node = leaf
        while node.parent is not None:
            path.append(node.value)
            node = node.parent
        return path[::-1]
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


# for i in processed_data:
#     tmp = i
#     # itemCnt[i][1]=idx
#     while tmp:
#         lb=tmp&-tmp
#         tmp &= ~lb
#         id=0
#         while lb:
#             lb>>=1
#             id+=1
#         itemCnt[id-1][0]+=1
# minCnt=2
# delete_mask=0
# for i in range(0,120):
#     if itemCnt[i][0] < minCnt:
#         delete_mask|=(1<<i)


# for i in range(0,120):
#     itemCnt[i][1]=i
# sorted_itemCnt=itemCnt[np.argsort(itemCnt[:, 0])]
# # #debug
# # for id,i in enumerate(sorted_itemCnt):
# #     print(id,i[0],i[1],sep=":")

mask = (1<<120)-1
delete_mask=~delete_mask&mask
#debug
# print(int_to_binary(delete_mask))
# print(delete_mask)

for i in range(0,8124):
    processed_data[i]&=delete_mask
#debug
# for i in processed_data:
#     print(int_to_binary(i))

tops = np.zeros(120,dtype=int)

trees = [[0 for _ in range(8125)] for _ in range(120)]

#預處理每個數字對於每個數字出現在相同筆數的數量
match = np.zeros((120, 120),dtype=int)
for i in range(1,120):
    cur = (1<<i)
    for j in range(0,8125):
        if cur&processed_data[j]:#如果有i出現在這筆

            trees[i][tops[i]]=processed_data[j]#建樹
            tops[i]+=1

            bit=2
            for k in range(1,120):
                if bit&processed_data[j]:#第k個item有跟i一起出現在同一筆，match[i][k]+=1
                    match[i][k]+=1
                bit<<=1



vis = np.zeros(120,dtype=int)
allset=set()
for i in sorted_itemCnt:#i是現在tree的index
    if i[0]<2:
        continue
    # print(f"now tree idx: {i[1]}")
    for j in range(0,tops[i[1]]):# 遍歷所有子樹,j是子樹的index
        bit = 2
        itemSet = []
        # print("other set node: ")
        for k in range(1,120):
            if bit&trees[i[1]][j] and match[i[1]][k]>=2 and vis[k]==0:
                # print(k,end="")
                itemSet.append(k)
            bit<<=1
        # print(itemSet)
        allset.add(tuple(itemSet))
    i[0]=0
    vis [i[1]]=1
end_time=time.time()
print(f'All processes have completed. cost {end_time-start_time} s')

# for i in allset:
#     print(i)

#debug
# for i in range(1,27):
#     for j in range(1,27):
#         print(match[i][j],end="")
#     print("")

