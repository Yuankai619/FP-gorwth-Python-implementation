import numpy as np
import time
start_time = time.time()
file_path = 'date/test1.dat'

data = []
with open(file_path, 'r') as file:
    for line in file:
        row = [int(x) for x in line.strip().split()]
        data.append(row)

itemCnt = np.zeros(120)
for i in data:
    itemCnt[i]+=1
def int_to_binary(n):
    binary_str = bin(n)
    return binary_str[2:]

minCnt=4
delete_bit=0
for i in range(119,1,-1):
    if itemCnt[i] < minCnt:
        delete_bit|=(1<<i)

# print(delete_bit)
print(int_to_binary(delete_bit))

processed_data = np.array(8125)

a = 86
print(int_to_binary(a))
print(a&-a)
print(int_to_binary(~(1<<(a&-a))))
a &=~(1<<(a&-a))
print(int_to_binary(a))