import time
start_time = time.time()
file_path = 'date\mushroom.dat'

data_list = []
with open(file_path, 'r') as file:
    for line in file:
        row = [int(x) for x in line.strip().split()]
        data_list.append(row)


# def findMaxbylist(data):
#     MAX_val=0
#     for i in data:
#         for j in i:
#             MAX_val+=j
#             # MAX_val=max(MAX_val,j)
#     print(MAX_val)

# findMaxbylist(data_list)
# arr= [0 for _ in range(121)]
p1= [0 for _ in range(121)]
for i in data_list:
    for j in i:
        p1[j]+=1
p2=[[0 for _ in range(121)] for _ in range(121)]
# support=[]
# for id,i in enumerate(arr):
#     if i >=813:
#         support.append(id)
for i in data_list:
    for j in range(1,120):
        st=set(i)
        for k in st:
            p2[j][k]+=1
        
cnt = 0
for i in range(1,120):
    for j in range(1,120):
        if i == j:
            continue
        elif p1[i]>=813 and ((p2[i][j])/p1[i])>0.8:
            cnt+=1


print(cnt)


end_time=time.time()
print(f'All processes have completed. cost {end_time-start_time} s')
