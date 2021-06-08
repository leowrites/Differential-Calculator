class Node:
    # a node will hold an operator, it will have a parent, left and right child
    # a node can be marked to indicate that if it is a (), this will help with child nodes returning to parent nodes
    def __init__(self):
        self.DataValue = ""
        self.Parent = None
        self.LeftChild = None
        self.RightChild = None
