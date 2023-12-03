from itertools import combinations

def generate_combinations(arr):
    result_set = []
    for r in range(1, len(arr) + 1):
        for combo in combinations(arr, r):
            result_set.append(combo)
    return result_set

# 測試給定的數組 [1, 2, 4, 5]
test_array = [1, 2, 4, 5]
combinations = generate_combinations(test_array)
for i in combinations:
    for j in i:
        print(j,end=" ")
    print("")