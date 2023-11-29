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
def print_bit(n):
    ret=""
    while(n):
        if(n&1):
            ret+='1'
        else:
            ret+='0'

minCnt=4
delete_bit=0
for i in range(119,1,-1):
    if itemCnt[i] < minCnt:
        delete_bit|=(1<<i)

print(delete_bit)