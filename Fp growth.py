import numpy as np
import time
start_time = time.time()
file_path = 'date/test1.dat'
SIZE =11
processed_data =[0]*SIZE
def int_to_binary(n):
    binary_str = bin(n)
    return binary_str[2:]
# read data and transform to bit 
with open(file_path, 'r') as file:
    id=0
    for line in file:
        row = [int(x) for x in line.strip().split()]
        for i in row:
            processed_data[id]|=(1<<i)
        id+=1

# for i in processed_data:
#     print(int_to_binary(i))

itemCnt = np.zeros(120,dtype=int)
for i in processed_data:
    tmp = i
    while tmp:
        lb=tmp&-tmp
        tmp &= ~lb
        id=0
        while lb:
            lb>>=1
            id+=1
        itemCnt[id-1]+=1

# for id,i in enumerate(itemCnt):
#     print(id,i,sep=":")
minCnt=4
delete_bit=0
for i in range(1,10):
    if itemCnt[i] < minCnt:
        # print("s")
        delete_bit|=(1<<i)

print(int_to_binary(delete_bit))

a=~(delete_bit)
print(int_to_binary(a))

for i in enumerate(processed_data):
    processed_data[id]&=delete_bit
for i in processed_data:
    print(int_to_binary(i))

