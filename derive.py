import tree
op = ['+','-','*','/','^']
class differential:
    # care that ^ is right associative, read first operand as base
    def __init__(self, equation):
        self.equation = equation
        self.new = ''
        self.place = 0
    
    def derive(self, equation):
        # recursively pair all terms
        try:
            for i, item in enumerate (equation):
                if len(equation) == 1:
                    break
                if item in op:
                    target = i-2
                    v1 = self.equation.pop(i-1)
                    v2 = self.equation.pop(target)
                    self.equation.pop(target)
                    if item == '^':
                        self.new = v2 + item + v1
                    else:
                        self.new = v1 + item + v2
                    self.equation.insert(target, self.new)
                    print(self.equation)
                    self.derive(self.equation)
        except IndexError:
            pass



    def map(self):
        dict = {
            "*": self.product(),
            "/": self.quotient(),
            "^": self.power()
        }
    
    def product(self):
        pass

    def power(self):
        pass

    def quotient(self):
        pass

q = 'x ^ 2+(x ^ 2-1) ^ 5'
tree = tree.tree(q)
q = tree.parse_fuc(q)
print(q)
d = differential(q)
d.derive(q)
