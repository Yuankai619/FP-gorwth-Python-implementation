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

    def insert(self, items):
        node = self.root
        for element in items:
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
    def remove_leaf(self, leaf):
        if leaf is None or leaf.parent is None:
            return

        if leaf in self.leaves:
            self.leaves.remove(leaf)

        parent = leaf.parent
        del parent.children[leaf.value]
        if parent.children is None:
            self.leaves.append(parent)

        # while parent.parent is not None and not parent.children:
        #     grandparent = parent.parent
        #     del grandparent.children[parent.value]
        #     parent = grandparent
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
for i in trie.leaves:
    print(i.value,end="")
print("")
for leaf in trie.leaves:
    print(f"Leaf value: {leaf.value}, Path to root: {trie.traverse_to_root(leaf)}")

print_trie(trie.root)

print("delete leave 2")
trie.remove_leaf(trie.leaves[0])
print_trie(trie.root)
for leaf in trie.leaves:
    print(f"Leaf value: {leaf.value}, Path to root: {trie.traverse_to_root(leaf)}")