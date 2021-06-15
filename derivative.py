# updated derivative class
# provides better reliablity
# try to allow fraction
from parser import parser
from node import node
from fractions import Fraction
from decimal import Decimal

op = ['+', '-', '*', '/', '^']
trig = ['sin', 'cos', 'tan', 'csc', 'sec', 'cot']


class Differential:
    def __init__(self, equation):
        p = parser(equation)
        self.equation = p.parse_fuc()
        self.node_tree = []

    def derive(self):
        self.tree_constructor()
        self.print_tree()
        return self.node_tree[-1].fp

    def tree_constructor(self):
        """
        construct a tree from nodes
        """
        try:
            for i, item in enumerate(self.equation):
                if item in op or item in trig:
                    if item in op:
                        target, node = self.node_constructor(i, item)
                    elif item in trig:
                        target, node = self.node_constructor(
                            i, op=item, is_trig=True)
                    self.equation.insert(target, node)
                    self.node_tree.append(node)
                    self.tree_constructor()
        except IndexError:
            pass

    def node_constructor(self, i, op=None, is_trig=False):
        """Constructs a node and returns it

        Args:
            i (int): [current index of the item]
            op ([string], optional): [an operator]. Defaults to None.
            is_trig (bool, optional): [detects whether it is a trignometric equation]. Defaults to False.

        Returns a node
        """

        if is_trig:
            # trig removes current index and index-1 from equation list

            target = i-1
            inner = self.equation.pop(target)
            op = self.equation.pop(target)
            if self.is_node(inner):
                fx = '({}({}))'.format(op, inner.fx)
            else:
                fx = '({}({}))'.format(op, inner)
            
            fp = self.trig_mapping(inner, op)
            new_node = node(fx=fx, fp=fp, l=inner, op=op)
            if self.is_node(inner):
                inner.parent = new_node

        else:

            target = i-2
            v1 = self.equation.pop(target)
            v2 = self.equation.pop(target)
            op = self.equation.pop(target)

            if self.is_node(v1) and self.is_node(v2):
                fx = '({}{}{})'.format(v1.fx, op, v2.fx)
            elif self.is_node(v1):
                fx = '({}{}{})'.format(v1.fx, op, v2)
            elif self.is_node(v2):
                fx = '({}{}{})'.format(v1, op, v2.fx)
            else:
                fx = '({}{}{})'.format(v1, op, v2)
                # construct the derivative
            fp = self.rule_mapping(v1, v2, op)

            new_node = node(fx, fp, v1, v2, op)

            if self.is_node(v1):
                v1.parent = new_node
            if self.is_node(v2):
                v2.parent = new_node

        return target, new_node

    def is_node(self, function):
        return isinstance(function, node)

    def rule_mapping(self, v1, v2, op):
        """map a function to its derivative and return the derivative
        Args:
            v1 ([function or node]): [first value]
            v2 ([function or node]): [second value]
            op ([an operator]): [operator]
        """
        m = {
            "*": self.product(v1, v2),
            "/": self.quotient(v1, v2),
            "^": self.power(v1, v2),
            "-": self.subtract(v1, v2),
            "+": self.add(v1, v2)
        }
        return m.get(op)

    def product(self, v1, v2):
        if self.is_node(v1) and self.is_node(v2):
            return '({}*{}+{}*{})'.format(v1.fp, v2.fx, v2.fp, v1.fx)
        elif self.is_node(v1):
            if v2.isdigit():
                return '({}*{})'.format(v2, v1.fp)
            else:
                return '({}*{}+{})'.format(v1.fp, v2, v1.fx)
        elif self.is_node(v2):
            if v1.isdigit():
                return '({}*{})'.format(v1, v2.fp)
            else:
                return '({}*{}+{})'.format(v2.fp, v1, v2.fx)
        else:
            if v1.isdigit() and v2.isdigit():
                return None
            elif v1.isdigit():
                return '({})'.format(v1)
            elif v2.isdigit():
                return '({})'.format(v2)

    def quotient(self, v1, v2):
        # when creating nodes, account for fraction
        if self.is_node(v1) and self.is_node(v2):
            return '(({}*{}-{}*{})/(({})^2))'.format(v1.fp, v2.fx, v2.fp, v1.fx, v2.fx)

        elif self.is_node(v1):
            if v2.isdigit():
                return '(({}*{}))/(({})^2))'.format(v1.fp, v2, v2)
            else:
                return '(({}*{}-{}))/(({})^2))'.format(v1.fp, v2, v1.fx, v2)
        elif self.is_node(v2):
            if v1.isdigit():
                return '((-{}*{})/(({})^2))'.format(v1, v2.fp, v2.fx)
            else:
                return '(({}-{}*{})/(({})^2))'.format(v2.fx, v1, v2.fp, v2.fx)
        else:
            if v1.isdigit() and v2.isdigit():
                return None
            elif v1.isdigit() and not v2.isdigit():
                return '(-{})/(({})^2)'.format(v1, v2)
            elif v2.isdigit() and not v1.isdigit():
                return '({})/(({})^2)'.format(v2, v2)

    def power(self, v1, v2):
        # v1 raised to the poewr of v2
        # if one of the values is a node in the power rule, then it needs to be mutiplied
        # this eliminates the need of a derivative constructor
        # and the nodes will only need to be search once
        if self.is_node(v2):
            # the program does not support non-numerical powers
            # remove brackets, and check if it is a fraction
            if '(' in v2.fx:
                new = v2.fx[1:-1]
                if '(' in new:
                    # make sure that there is no double brackets in the exponent
                    return None
                else:
                    b = Fraction(new)
                    n_p = Fraction(float(b-1))
                    # follow a similar process 
                    if self.is_node(v1):
                        if v1.fp != None:
                            return '(({})*{}^({}))({})'.format(b, v1.fx, n_p, v1.fp)
                        else:
                            return '(({})*{}^({}))'.format(b, v1.fx, n_p)
                    elif not v1.isdigit():
                        return '(({})*{}^({})'.format(b, v1, n_p)
                    else:
                        return None
            if not v2.fx.isdigit() or v1.isdigit():
                return None
        elif self.is_node(v1):
            # if v1 is a node, then it probably has a derivative
            # if not, then don't mutiply it by anything
            # if it's a fraction, convert to decimal, do subtraction, and convert back to fraction form
            if v1.fp != None:
                return '({}*{}^{})({})'.format(v2, v1.fx, str(int(v2)-1), v1.fp)
            else:
                return '({}*{}^{})'.format(v2, v1.fx, str(int(v2)-1))
        else:
            # this is when v2 is a number, but v1 is a varaible
            # this means that it has no derivative
            try:
                return '({}*{}^{})'.format(v2, v1, str(int(v2)-1))
            except ValueError:
                pass

    def subtract(self, v1, v2):
        if self.is_node(v1) and self.is_node(v2):
            return '({}-{})'.format(v1.fp, v2.fp)
        elif self.is_node(v1):
            if v2.isdigit():
                return '({})'.format(v1.fp)
            else:
                return '({}-1)'.format(v1.fp)
        elif self.is_node(v2):
            if v1.isdigit():
                return '(-({}))'.format(v2.fp)
            else:
                return '(1-{})'.format(v2.fp)
        else:
            if v1.isdigit() and v2.isdigit() or v2.isdigit() and not v1.isdigit():
                return None
            elif v1.isdigit() and not v2.isdigit():
                return '(-)'

    def add(self, v1, v2):
        if self.is_node(v1) and self.is_node(v2):
            return '({}+{})'.format(v1.fp, v2.fp)
        elif self.is_node(v1):
            if v2.isdigit():
                return '({})'.format(v1.fp)
            else:
                return '({}+1)'.format(v1.fp)
        elif self.is_node(v2):
            if v1.isdigit():
                return '({})'.format(v2.fp)
            else:
                return '(1+{})'.format(v2.fp)
        else:
            if v1 == 'x' and v2 == 'x':
                return '(2)'
            else:
                return None

    def trig_mapping(self, v1, trig):
        # similar to rule_mapping
        trig_derivative = {
            'cos': '(-sin({}))'.format(v1),
            'sin': '(cos({}))'.format(v1),
            'tan': '(sec({}))^2'.format(v1),
            'csc': '(-csc({})cot({}))'.format(v1, v1),
            'sec': '(sec({})tan({}))'.format(v1, v1),
            'cot': '(-(csc({}))^2)'.format(v1)
        }
        if self.is_node(v1):
            trig_derivative = {
                'cos': '(-sin({}))({})'.format(v1.fx, v1.fp),
                'sin': '(cos({}))({})'.format(v1.fx, v1.fp),
                'tan': '(sec({}))^2)({})'.format(v1.fx, v1.fp),
                'csc': '(-csc({})cot({}))({})'.format(v1.fx, v1.fx, v1.fp),
                'sec': '(sec({})tan({}))({})'.format(v1.fx, v1.fx, v1.fp),
                'cot': '(-(csc({}))^2)({})'.format(v1.fx, v1.fp)
            }
        return trig_derivative.get(trig)

    def print_tree(self):
        # prints tree from the lowest to the highest
        print('\n')
        for i, item in enumerate(self.node_tree):
            print("fuction:{} derivative:{} left:{} right:{} operator:{} parent:{}".format(
                item.fx, item.fp, item.left, item.right, item.op, item.parent
            ))
