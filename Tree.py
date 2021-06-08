operators = ["+", "-", "*", "/"]
class Tree:
    def __init__(self):
        self.Tree = list()
        # a node in a tree should be able to point to two other nodes
        # which then can points to two other 
        self.equation = ""
        self.current_node = None
    
    def check_operator(self, t):
        if t in operators:
            return 1
        else:
            return 0
    
    def check_para(self, t):
        # if a parameter is opened, 
        if t == "(":
            return 1
        elif t == ")":
            return 0
        else:
            return -1

    def create_node(self):
        # create a new empty node, then set the current node as the left child
        # condition: paranthethis is detected, or a search show an operator is going to occur
        pass

    def parse_equation(self, equation):
        # every child node will have a parent node, except for the first node
        for i in equation:
            if self.check_operator(i) == 1:
                pass
            elif self.check_para(i) == 1:
                pass
            
