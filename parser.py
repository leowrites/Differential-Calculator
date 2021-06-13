# variables multiplied by a constant must be connected with the multiply sign *
# implement trig?

op = {
    '+': 0,
    '-': 0,
    '*': 1,
    '/': 1,
    '^': 2
}


class parser:
    def __init__(self):
        self.output = []
        self.stack = []

    def parse_fuc(self, sample):
        # combine the digits into one number by appending number to a single temporary holder
        # the number will then be appended later when a () is reached or an operator
        # this would mean that numbers are only pushed when an operator is reached
        # cos implementation
        temp_num = ''
        for i, item in enumerate(sample):
            if i+1 != len(sample) and item.isdigit():
                temp_num += item
            elif i+1 == len(sample) and item.isdigit():
                temp_num += item
                self.output.append(temp_num)
                self.end_fuc()
            elif i+1 == len(sample) and item == ")":
                if temp_num != '':
                    self.output.append(temp_num)
                self.end_para_fuc()
                self.end_fuc()
            else:
                temp_num = self.push_num(temp_num)
                if item in op:
                    self.op_fuc(item)
                elif self.var_fuc(item):
                    self.output.append(item)
                elif self.para_fuc(item) == 0:
                    self.stack.append(item)
                elif self.para_fuc(item) == 1:
                    self.end_para_fuc()
        return self.output

    def push_num(self, num):
        # pushes the number to the output
        if num != '':
            self.output.append(num)
            num = ''
            return num
        else:
            return ''

    def var_fuc(self, item):
        if item == "x":
            return True

    def op_fuc(self, item):
        # if the stack is not empty
        if self.stack:
            # loop through each item from the stack backwards
            x = range(len(self.stack))
            q = len(self.stack)
            for i in x:
                # ignore (
                index = q - i - 1
                v = op.get(item)
                # exception for index error
                try:
                    # if the operator in the stack has a higher
                    # or equal presedence when compare to the current
                    # operator
                    a = self.stack[index]
                    z = op.get(a)
                    if a != "(" and z > v or z == v:
                        self.output.append(self.stack.pop(index))
                    if a == "(":
                        break
                except IndexError:
                    pass

        # for all other conditions, append the operator to the stack
        self.stack.append(item)

    def para_fuc(self, item):
        if item == "(":
            return 0
        elif item == ")":
            return 1

    def end_para_fuc(self):
        x = range(len(self.stack))
        q = len(self.stack)
        for i in x:
            # pop and append all operators
            # stop when ( is detected, and discard (
            index = q - i - 1
            try:
                if self.stack[-1] == "(":
                    self.stack.pop()
                    break
                else:
                    self.output.append(self.stack.pop(index))
            except IndexError:
                pass

    def end_fuc(self):
        # call derivative function
        if self.stack:
            self.output.append(self.stack.pop())
            self.end_fuc()
