import time
start_time = time.time()
file_path = 'date\mushroom.dat'

data_list = []
with open(file_path, 'r') as file:
    for line in file:
        row = [int(x) for x in line.strip().split()]
        data_list.append(row)


p1= [0 for _ in range(121)]
for i in data_list:
    for j in i:
        p1[j]+=1
cnt2=0
for i in range(1,120):
    if p1[i]>=813:
        cnt2+=1
print(cnt2)


p2=[[0 for _ in range(121)] for _ in range(121)]

for i in data_list:
    for j in i:
        for k in i:
            p2[j][k]+=1

# data[]
# for(int j=1;j<data[i].size();j++){
#     for(int k=j+1;k<=data[i].size();k++){
#         p2[j][k];
#     }
# }
        
cnt = 0
for i in range(1,120):
    for j in range(1,120):
        if i == j:
            continue
        elif p2[i][j]>=813:
            cnt+=1


print(cnt/2)


end_time=time.time()
print(f'All processes have completed. cost {end_time-start_time} s')
