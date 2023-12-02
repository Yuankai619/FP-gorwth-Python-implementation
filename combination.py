# from itertools import combinations

# def generate_combinations(arr):
#     result_set = []
#     for r in range(1, len(arr) + 1):
#         for combo in combinations(arr, r):
#             result_set.append(combo)
#     return result_set

# # 測試給定的數組 [1, 2, 4, 5]
# test_array = [1, 2, 4, 5]
# combinations = generate_combinations(test_array)
# for i in combinations:
#     for j in i:
#         print(j,end=" ")
#     print("")
from itertools import combinations
from numba import jit
import numpy as np

@jit(nopython=True)
def generate_combinations_jit(arr):
    result = []
    for r in range(1, len(arr) + 1):
        for combo in combinations(arr, r):
            result.append(combo)
    return result

# 將輸入數組轉換為 Numba 支援的型態，如 numpy 數組
test_array = np.array([1, 2, 4, 5])

# 使用 Numba 優化的函數
combinations_jit = generate_combinations_jit(test_array)