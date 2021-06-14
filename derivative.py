import parser
import node
op = ['+', '-', '*', '/', '^']

# create a derivative tree
# need to fix the order of which two terms are passed into the mapping and later the construction


class differential:
    # care that ^ is right associative, read first operand as base
    def __init__(self, p=None):
        print("---------------------------------!!Klassen You Are The Best!!---------------------------------")
        if p == None:
            p = parser.parser(input(
                "Enter Input (remember to have * if a variable is multiplied by a constant): "))
        else:
            p = parser.parser(p)
        self.equation = p.parse_fuc()
        print("\nParsed Equation {}".format(self.equation))
        self.new = ''
        self.tree = []
        self.derived = ''

    def derive(self):
        self.tree_constructor()
        return self.derivative_constructor()

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
        v2 = self.equation.pop(index-1)
        v1 = self.equation.pop(target)
        self.equation.pop(target)

        # construct the original equation
        # derivatives will be constructed inside
        # if v1 and v2 are both nodes
        if isinstance(v1, node.node) and isinstance(v2, node.node):
            fx = '({}{}{})'.format(v1.fx, op, v2.fx)
            # construct the derivative
            fp = self.mapping(v1.fx, v2.fx, op)

        # if only v1 is a node
        elif isinstance(v1, node.node):
            fx = '({}{}{})'.format(v1.fx, op, v2)
            # construct the derivative
            fp = self.mapping(v1.fx, v2, op)

        # if only v2 is a node
        elif isinstance(v2, node.node):
            fx = '({}{}{})'.format(v1, op, v2.fx)
            # construct the derivative
            fp = self.mapping(v1, v2.fx, op)

        # if none are nodes
        else:
            fx = '({}{}{})'.format(v1, op, v2)
            # construct the derivative
            fp = self.mapping(v1, v2, op)

        # construct a new node
        new_node = node.node(fx, fp, v1, v2, op)

        # if v1 or v2 are nodes, set their parent class to current
        if isinstance(v1, node.node):
            v1.parent = new_node
        if isinstance(v2, node.node):
            v2.parent = new_node

        return target, new_node

    def mapping(self, v1, v2, op):
        # pass in nodes
        # v1 = first term, v2
        m = {
            "*": self.product(v1, v2),
            "/": self.quotient(v1, v2),
            "^": self.power(v1, v2),
            "-": self.subtract(v1, v2),
            "+": self.add(v1, v2)
        }
        return m.get(op)

    def subtract(self, v1, v2):
        # similar pattern to the product rule
        # need to check whether a child is a variable or a constant
        if isinstance(v1, node.node) and isinstance(v2, node.node):
            return '({}-{})'.format(v1.fp, v2.fp)
        elif isinstance(v1, node.node) and not isinstance(v2, node.node):
            if v2.isdigit():
                return '({})'.format(v1.fp)
            else:
                return '({}-1)'.format(v1.fp)
        elif isinstance(v2, node.node) and not isinstance(v1, node.node):
            if v1.isdigit():
                return '(-({}))'.format(v2.fp)
            else:
                return '(1-{})'.format(v2.fp)
        elif not isinstance(v1, node.node) and not isinstance(v2, node.node):
            if v1.isdigit() and v2.isdigit():
                return None
            elif v1.isdigit() and not v2.isdigit():
                return '(-)'
            elif v2.isdigit() and not v1.isdigit():
                return None

    def add(self, v1, v2):
        if isinstance(v1, node.node) and isinstance(v2, node.node):
            return '({}+{})'.format(v1.fp, v2.fp)
        elif isinstance(v1, node.node) and not isinstance(v2, node.node):
            if v2.isdigit():
                return '({})'.format(v1.fp)
            else:
                # else it would be a single variable, which means the derivative is always 1
                return '({}+1)'.format(v1.fp)
        elif isinstance(v2, node.node) and not isinstance(v1, node.node):
            if v1.isdigit():
                return '({})'.format(v2.fp)
            else:
                return '(1+{})'.format(v2.fp)
        elif not isinstance(v1, node.node) and not isinstance(v2, node.node):
            # if neither are nodes
            if v1 == 'x' and v2 == 'x':
                return '(2)'
            else:
                return None

    def product(self, v1, v2):
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
        if isinstance(v2, node.node):
            return None
        elif v2.isdigit():
            return '({}*{}^{})'.format(v2, v1, str(int(v2)-1))

    def quotient(self, v1, v2):
        # quotient rule
        # v1 is the dividend, v2 is the
        # f(x) = (h'(x)g(x)-g'(x)h(x))/((g(x))^2)
        if isinstance(v1, node.node) and isinstance(v2, node.node):
            return '(({}*{}-{}*{})/(({})^2))'.format(v1.fp, v2.fx, v2.fp, v1.fx, v2.fx)
        elif isinstance(v1, node.node) and not isinstance(v2, node.node):
            if v2.isdigit():
                return '(({}*{}))/(({})^2))'.format(v1.fp, v2, v2)
            else:
                return '(({}*{}-{}))/(({})^2))'.format(v1.fp, v2, v1.fx, v2)
        elif isinstance(v2, node.node) and not isinstance(v1, node.node):
            if v1.isdigit():
                return '((-{}*{})/(({})^2))'.format(v1, v2.fp, v2.fx)
            else:
                return '(({}-{}*{})/(({})^2))'.format(v2.fx, v1, v2.fp, v2.fx)
        elif not isinstance(v1, node.node) and not isinstance(v2, node.node):
            if v1.isdigit() and v2.isdigit():
                return None
            elif v1.isdigit() and not v2.isdigit():
                return '(-{})/(({})^2)'.format(v1, v2)
            elif v2.isdigit() and not v1.isdigit():
                return '({})/(({})^2)'.format(v2, v2)

    def derivative_constructor(self):
        for i, item in enumerate(self.tree):
            # recusively add children's derivative to the parent, stop when there is no parent
            # then the parent will apply derivative rules
            # the node of which that has no parent should be the last node
            # check the position of child 
            if item.parent and item.parent.fp != None:
                item.parent.fp += '*({})'.format(item.fp)
            elif item.parent and item.parent.fp == None:
                item.parent.fp = '({})'.format(item.fp)
            if not item.parent:
                # if the node has no parent, then it is the highest level
                if item.op == '^':
                    return item.fp
                else:
                    return self.mapping(item.left, item.right, item.op)

    def print_tree(self):
        # prints tree from the lowest to the highest
        for i, item in enumerate(self.tree):
            print("fuction:{} derivative:{} left:{} right:{} operator:{} parent:{}".format(
                item.fx, item.fp, item.left, item.right, item.op, item.parent
            ))
