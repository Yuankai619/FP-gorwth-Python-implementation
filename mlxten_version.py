class TreeNode:
    def __init__(self, name, count, parentNode):
        self.name = name
        self.count = count
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def increment(self, count):
        self.count += count

def createTree(transactions, minSup):
    headerTable = {}
    for trans in transactions:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + 1

    headerTable = {k: v for k, v in headerTable.items() if v >= minSup}

    if len(headerTable) == 0:
        return None, None

    for k in headerTable:
        headerTable[k] = [headerTable[k], None]

    retTree = TreeNode('Null Set', 1, None)
    for tranSet, count in transactions.items():
        localD = {}
        for item in tranSet:
            if item in headerTable:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable

def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        inTree.children[items[0]].increment(count)
    else:
        inTree.children[items[0]] = TreeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1:], inTree.children[items[0]], headerTable, count)

def updateHeader(nodeToTest, targetNode):
    while nodeToTest.nodeLink != None:
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSup)

        if myHead != None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def loadDataSet(file_path):
    file_path = 'date\mushroom.dat'
    with open(file_path, 'r') as file:
        return [line.strip().split() for line in file]

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

# 读取数据
dataSet = loadDataSet('file_path')

# 初始化事务数据集
initSet = createInitSet(dataSet)

# 构建 FP-Tree
myFPtree, myHeaderTab = createTree(initSet, 813)

# 提取频繁项集
myFreqList = []
mineTree(myFPtree, myHeaderTab, 813, set([]), myFreqList)

# 输出频繁项集的数量
print(f"Total number of frequent itemsets: {len(myFreqList)}")
