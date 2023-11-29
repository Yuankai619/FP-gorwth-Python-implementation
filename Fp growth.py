import numpy as np
import time
start_time = time.time()
file_path = 'date/test2.dat'
SIZE =9     
processed_data =[0]*SIZE
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
for i in range(0,27):
    if itemCnt[i][0] < minCnt:
        delete_mask|=(1<<i)


for i in range(0,120):
    itemCnt[i][1]=i
sorted_itemCnt=itemCnt[np.argsort(itemCnt[:, 0])]
# #debug
# for id,i in enumerate(sorted_itemCnt):
#     print(id,i[0],i[1],sep=":")

mask = (1<<27)-1
delete_mask=~delete_mask&mask
#debug
# print(int_to_binary(delete_mask))
# print(delete_mask)

for i in range(0,9):
    processed_data[i]&=delete_mask
#debug
# for i in processed_data:
#     print(int_to_binary(i))

tops = np.zeros(27,dtype=int)
trees = np.zeros((27,10),dtype=int)

#預處理每個數字對於每個數字出現在相同筆數的數量
match = np.zeros((27, 27),dtype=int)
for i in range(1,27):
    for data in processed_data:
        if (1<<i)&data:#如果有i出現在這筆

            trees[i][tops[i]]=data#建樹
            tops[i]+=1

            bit=2
            for k in range(1,27):
                if bit&data:#第k個item有跟i一起出現在同一筆，match[i][k]+=1
                    match[i][k]+=1
                bit<<=1
allset=[]
for i in sorted_itemCnt:#i是現在tree的index
    if i[0]<2:
        continue
    for j in range(0,tops[i[1]]):# 遍歷所有子樹,j是子樹的index
        bit = 2
        itemSet = []
        for k in range(1,27):
            if bit&trees[i[1]][j] and match[i[1]][k]>=2:
                itemSet.append(k)
        allset.append(itemSet)

for i in allset:
    print(i)

#debug
# for i in range(1,27):
#     for j in range(1,27):
#         print(match[i][j],end="")
#     print("")

