import numpy as np
import time
from numba import jit
import numba as nb
from multiprocessing import Pool

start_time = time.time()
file_path = 'date/mushroom.dat'
SIZE =8125  
processed_data =[0]*SIZE# 0 base
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
with open(file_path, 'r') as file:
    id=0
    for line in file:
        row = [int(x) for x in line.strip().split()]
        for i in row:
            processed_data[id]|=(1<<i)
        id+=1

#debug
# for i in processed_data:
#     print(int_to_binary(i))

#count item count in itemCnt 
itemCnt = np.zeros((120,2),dtype=int)
for i in processed_data:
    tmp = i
    # itemCnt[i][1]=idx
    while tmp:
        lb=tmp&-tmp
        tmp &= ~lb
        id=0
        while lb:
            lb>>=1
            id+=1
        itemCnt[id-1][0]+=1
minCnt=2
delete_mask=0
for i in range(0,120):
    if itemCnt[i][0] < minCnt:
        delete_mask|=(1<<i)


for i in range(0,120):
    itemCnt[i][1]=i
sorted_itemCnt=itemCnt[np.argsort(itemCnt[:, 0])]
# #debug
# for id,i in enumerate(sorted_itemCnt):
#     print(id,i[0],i[1],sep=":")

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

