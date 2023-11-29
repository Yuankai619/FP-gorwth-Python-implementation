import numpy as np
import timeit

# 定義一個較大的數組和列表以進行測試
array = np.arange(10000)
lst = list(array)

# 測量將 NumPy 數組轉換為元組的時間
time_array_to_tuple = timeit.timeit(lambda: tuple(array), number=1000)

# 測量將列表轉換為元組的時間
time_list_to_tuple = timeit.timeit(lambda: tuple(lst), number=1000)

print("NumPy Array to Tuple:", time_array_to_tuple)
print("List to Tuple:", time_list_to_tuple)
