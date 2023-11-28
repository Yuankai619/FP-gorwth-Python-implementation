import numpy as np
from numba import jit
import numba as nb
import time

start_time = time.time()
file_path = 'date\mushroom.dat'
data = np.loadtxt(file_path)
# data_list = []
# with open(file_path, 'r') as file:
#     for line in file:
#         row = [int(x) for x in line.strip().split()]
#         data_list.append(row)
# data=np.array(data_list,dtype=int)

# @nb.vectorize("float32(float32)",nopython=True)
# def findMax():
#     # MAX_val=np.int32(0)
#     total=0
#     for i in data:
#         for j in i:
#             total+=j
#     return total
print(np.sum(data))
end_time=time.time()
print(f'All processes have completed. cost {end_time-start_time} s')


