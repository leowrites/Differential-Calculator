import parser
import node
op = ['+', '-', '*', '/', '^']

# create a derivative tree
# user inorder traverse to construct the final derivative


class differential:
    # care that ^ is right associative, read first operand as base
    def __init__(self, equation):
        self.equation = equation
        self.new = ''
        self.tree = []
        self.derived = ''

    def tree_constructor(self):
        # recursively pair all terms
        try:
            for i, item in enumerate(self.equation):
                if item in op:
                    target, node = self.node_constructor(i, item)
                    self.equation.insert(target, node)
                    self.tree.append(node)
                    self.tree_constructor()
        except IndexError:
            pass

    def node_constructor(self, index, op):
        target = index-2
        v1 = self.equation.pop(index-1)
        v2 = self.equation.pop(target)
        self.equation.pop(target)

        # construct the original equation
        # derivatives will be constructed inside
        # if v1 and v2 are both nodes
        if isinstance(v2, node.node) and isinstance(v1, node.node):
            fx = '({}{}{})'.format(v2.fx, op, v1.fx)
            # construct the derivative
            fp = self.mapping(v1.fx, v2.fx, op)

        # if only v1 is a node
        elif isinstance(v1, node.node):
            fx = '({}{}{})'.format(v2, op, v1.fx)
            # construct the derivative
            fp = self.mapping(v1.fx, v2, op)

        # if only v2 is a node
        elif isinstance(v2, node.node):
            fx = '({}{}{})'.format(v2.fx, op, v1)
            # construct the derivative
            fp = self.mapping(v1, v2.fx, op)

        # if none are nodes
        else:
            fx = '({}{}{})'.format(v2, op, v1)
            # construct the derivative
            fp = self.mapping(v1, v2, op)

        # construct a new node
        new_node = node.node(fx, fp, v2, v1, op)

        # if v1 or v2 are nodes, set their parent class to current
        if isinstance(v1, node.node):
            v1.parent = new_node
        if isinstance(v2, node.node):
            v2.parent = new_node

        return target, new_node

    def mapping(self, v1, v2, op):
        m = {
            "*": self.product(v1, v2),
            "/": self.quotient(v1, v2),
            "^": self.power(v1, v2),
            "+": None,
            "-": None
        }
        return m.get(op)

    def product(self, v1, v2):
        # disable product rule if necessary
        # if v1 is a node then it has attributes
        # if neither are nodes, then they are either a number or a variable
        if isinstance(v1, node.node) and isinstance(v2, node.node):
            return '({}*{}+{}*{})'.format(v1.fp, v2.fx, v1.fx, v2.fp)
        elif isinstance(v1, node.node) and not isinstance(v2, node.node):
            if v2.isdigit():
                return '({}*{})'.format(v2, v1.fp)
            else:
                # else it would be a single variable, which means the derivative is always 1
                return '({}*{}+{})'.format(v1.fp, v2, v1.fx)
        elif isinstance(v2, node.node) and not isinstance(v1, node.node):
            if v1.isdigit():
                return '({}*{})'.format(v1, v2.fp)
            else:
                # else it would be a single variable, which means the derivative is always 1
                return '({}*{}+{})'.format(v2.fp, v1, v2.fx)
        elif not isinstance(v1, node.node) and not isinstance(v2, node.node):
            # if neither are nodes
            if v1.isdigit() and v2.isdigit():
                return None
            elif v1.isdigit() and not v2.isdigit():
                return '({})'.format(v1)
            elif v2.isdigit() and not v1.isdigit():
                return '({})'.format(v2)

    def power(self, v1, v2):
        if isinstance(v1, node.node):
            return None
        elif v1.isdigit():
            return '({}*{}^{})'.format(v1, v2, str(int(v1)-1))

    def quotient(self, v1, v2):
        # quotient rule
        pass

    def derivative_constructor(self):
        for i, item in enumerate(self.tree):
            # recusively add children's derivative to the parent, stop when there is no parent
            # then the parent will apply derivative rules
            # the node of which that has no parent should be the last node
            # check the position of child 
            if item.parent and item.parent.fp != None:
                item.parent.fp += '({})'.format(item.fp)
            elif item.parent and item.parent.fp == None:
                item.parent.fp = '({})'.format(item.fp)
            if not item.parent:
                # if the node has no parent, then it is the highest level
                return self.parent_process(item)
    
    def parent_process(self, parent):
        # process parent nodes
        if parent.op == '+' or parent.op == '-':
            parent.fp = '[{}]{}[{}]'.format(parent.left.fp, parent.op, parent.right.fp)
        return parent.fp

    def print_tree(self):
        # prints tree from the lowest to the highest
        for i, item in enumerate(self.tree):
            print("fuction:{} derivative:{} left:{} right:{} operator:{} parent:{}".format(
                item.fx, item.fp, item.left, item.right, item.op, item.parent
            ))
