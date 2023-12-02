from collections import defaultdict
from itertools import combinations
from multiprocessing import Pool
import time

CPU_COUNT = 24
PATTERN_LEN = 10     #最多一次看5個item   
MIN_SUPPORT = 813    #最少出現次數
MIN_CONFIDENCE = 0.8 #confidence最低門檻

def LoadData():
    with open("date/mushroom.dat", 'r') as f:
        return [[int(x) for x in line.split()] for line in f]

def data2frozenset(dataset):
    frozenSet = {}
    for data in dataset:
        frozenSet[frozenset(data)] = 1
    return frozenSet
    
class Node:
    def __init__(self, name, count, parent):
        self.name = name
        self.count = count
        self.parent = parent
        self.child = {}
        self.nextSimilarItem = None
        
    #計算出現次數    
    def inc(self, num):
        self.count += num
        
    #印出樹的路徑       
    # def display(self, ind=1):
    #     print ('  '*ind, self.name, ' ', self.count)
    #     for child in self.child.values():
    #         child.display(ind+1)
              
        
def createFPtree(dataset):
    headPointTable = {}
    
    #計算出現次數
    for data in dataset:
        for item in data:
            headPointTable[item] = headPointTable.get(item, 0) + dataset[data]  
    
    #只留下>=MIN_SUPPORT的item
    headPointTable = {name:cnt for name, cnt in headPointTable.items() if cnt >= MIN_SUPPORT}
    freq_items = set(headPointTable.keys())

    #沒有任何元素
    if len(freq_items)==0: return None, None
    
    for k in headPointTable:
        headPointTable[k] = [headPointTable[k], None]  #指到下一個similiar Item
        
    #建立fp tree
    fp_tree = Node('null set', 1, None) 
    
    #把資料看過第二遍
    for items, cnt in dataset.items():
        keep_freq_items = {}
        
        #只留下出現在freq_items的item
        for item in items:
            if item in freq_items:
                keep_freq_items[item] = headPointTable[item][0]
            
        if len(keep_freq_items) > 0:
            #用item出現次數，由大到小排序
            orderedFrequentItems = [v[0] for v in sorted(keep_freq_items.items(),key = lambda v: (v[1], v[0]),reverse = True)]
            #更新FP tree
            updateFPtree(orderedFrequentItems, fp_tree, headPointTable, cnt)
        
    return fp_tree, headPointTable
    
def updateFPtree(items, fp_tree, headPointTable, cnt):
    if items[0] in fp_tree.child:
        fp_tree.child[items[0]].inc(cnt)
    else:
        #如不存在子節點，新增一個新的子節點
        fp_tree.child[items[0]] = Node(items[0], cnt, fp_tree)
        #指到下一個
        if headPointTable[items[0]][1] == None:  
            headPointTable[items[0]][1] = fp_tree.child[items[0]]
        else:
            updateHeadPointTable(headPointTable[items[0]][1], fp_tree.child[items[0]])
    
    #遞迴往下找
    if len(items) > 1:
        updateFPtree(items[1::], fp_tree.child[items[0]], headPointTable, cnt)
        
#找到最後一個，再把targetNode放入
def updateHeadPointTable(headPointBeginNode, targetNode):
    while (headPointBeginNode.nextSimilarItem != None):    
        headPointBeginNode = headPointBeginNode.nextSimilarItem
    headPointBeginNode.nextSimilarItem = targetNode
        
#------------------挖掘頻繁項集------------------------------------------   
   
def mineFPTree(header:dict, prefix:set, frequent_set:set):
    if len(prefix) >= PATTERN_LEN:
        return
    # val[0] for item name, val[1][0] for item count
    header_items = [val[0] for val in sorted(header.items(), key=lambda val: val[1][0])] 
    if len(header_items) == 0:
        return
    
    for item in header_items:
        new_prefix = prefix.copy()
        new_prefix.add(item)
        support = header[item][0]
        frequent_set[frozenset(new_prefix)] = support
        prefix_path = findPrefixPath(header, item)
        if len(prefix_path) != 0:
            conditional_tree, conditional_header = createFPtree(prefix_path)
            if conditional_header is not None:
                mineFPTree(conditional_header, new_prefix, frequent_set)

#--------------------產生關連規則----------------------------------------

def rule_generator(frequent_item, frequent_item_count, subset_counts):
    counter = 0
    subsets = [subset for i in range(1, len(frequent_item)) for subset in combinations(frequent_item, i)]
    for s in subsets:
        subset_key = frozenset(s)
        # 確保子集的鍵存在於 subset_counts 中
        if subset_key in subset_counts:
            confidence = frequent_item_count *10
            if confidence >= subset_counts[subset_key]*8:
                counter += 1
    return counter

def generateRulesParallel(frequent_set):
    tasks = []
    for item in frequent_set:
        item_count = frequent_set[frozenset(item)]
        # 只包括那些存在於 frequent_set 中的子集
        subset_counts = {frozenset(s): frequent_set[frozenset(s)] for s in combinations(item, len(item) - 1) if frozenset(s) in frequent_set}
        tasks.append((item, item_count, subset_counts))
    
    with Pool(CPU_COUNT) as p:
        results = p.starmap(rule_generator, tasks)

    total_counter = sum(results)
    print(total_counter)

#---------------------計算每個長度的frequent_set-------------------------

def cnt_each_len_freq_item(freq_set:set):
    cnt = [0,0,0,0,0,0,0,0,0,0,0]
    # cnt = [0,0,0,0,0,0]
    for item in freq_set:
        cnt[len(item)] += 1
    for idx in range(1,len(cnt)):
        print('|L^{}|={}'.format(idx,cnt[idx]))
        
#---------------------印出路徑-------------------------------------------

#每個nextSimilarItem，都呼叫ascendTree往上找路徑
def findPrefixPath(headPointTable, node): 
    condPaths = {}
    treenode = headPointTable[node][1]
    prefixPath = ascendTree(treenode)
    if(len(prefixPath)):
        condPaths[frozenset(prefixPath)] = treenode.count

    while treenode.nextSimilarItem != None:
        treenode = treenode.nextSimilarItem     #往下一個similarItem找
        prefixPath = ascendTree(treenode)
        if len(prefixPath): 
            condPaths[frozenset(prefixPath)] = treenode.count
        
    return condPaths 


#把到root經過的點都加入prefixs
def ascendTree(node): 
    prefixs = []
    while (node.parent != None) and (node.parent.name != 'null set'):
        node = node.parent
        prefixs.append(node.name)
    return  prefixs   

if __name__=='__main__':
    begin_time = time.time()
    data = LoadData()
         
    fp_tree, headpointList = createFPtree(data2frozenset(data))
    frequent_set = {}
    prefix = set([])
    mineFPTree(headpointList, prefix, frequent_set)
    generateRulesParallel(frequent_set)
    
    cnt_each_len_freq_item(frequent_set)
    print(time.time() - begin_time)