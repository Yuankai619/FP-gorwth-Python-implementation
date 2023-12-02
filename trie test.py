class TreeNode:
    def __init__(self, value=None):
        self.value = value
        self.count = 1
        self.children = {}
        self.parent = None

class Trie:
    def __init__(self):
        self.root = TreeNode()
        self.leaves = []

    def insert(self, array):
        node = self.root
        for element in array:
            if element not in node.children:
                new_node = TreeNode(element)
                new_node.parent = node
                node.children[element] = new_node
            else:
                node.children[element].count += 1
            node = node.children[element]
        self.leaves.append(node)

    def traverse_to_root(self, leaf):
        path = []
        node = leaf
        while node.parent is not None:
            path.append(node.value)
            node = node.parent
        return path[::-1]
    
def print_trie(node, level=0):
    # Base case: if the node is None, return
    if node is None:
        return

    # Print the current node
    indent = " " * (level * 4)
    node_info = f"{indent}Node: {node.value}, Count: {node.count}" if node.value is not None else "Root"
    print(node_info)

    # Recursively print each child
    for child in node.children.values():
        print_trie(child, level + 1)
# Example usage
trie = Trie()
n = 4  # Number of arrays
m = 5  # Size of each array
data = [[1, 2, 3, 4, 5], [1, 2, 6, 7, 8], [1, 3, 6, 9, 10],[1,2,6,7,4]]

# Insert data into the trie
for items in data:
    trie.insert(items)

# Print the leaf nodes and their paths to the root
for leaf in trie.leaves:
    print(f"Leaf value: {leaf.value}, Path to root: {trie.traverse_to_root(leaf)}")