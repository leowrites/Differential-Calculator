# variables multiplied by a constant must be connected with the multiply sign *
# implement trig?

op = {
    '+': 0,
    '-': 0,
    '*': 1,
    '/': 1,
    '^': 2
}
trig = ['sin', 'cos', 'tan', 'csc', 'sec', 'cot']

class parser:
    def __init__(self, user_in):
        self.user_in = user_in
        self.output = []
        self.stack = []

    def parse_fuc(self):
        # combine the digits into one number by appending number to a single temporary holder
        # the number will then be appended later when a () is reached or an operator
        # this would mean that numbers are only pushed when an operator is reached

        # trig implementation
        # first detect if a trig occurs at all, and how many trigs there should be. 
        # then decide how to parse the equation
        temp_num = ''
        x = self.find_trig()
        for i, item in enumerate(self.user_in):
            if x and i in x:
                # trig append
                # need a trig push function
                self.stack.append(self.user_in[i:i+3])
            if i+1 != len(self.user_in) and item.isdigit():
                temp_num += item
            elif i+1 == len(self.user_in) and item.isdigit():
                temp_num += item
                self.output.append(temp_num)
                self.end_fuc()
            elif i+1 == len(self.user_in) and item == ")":
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
    
    def find_trig(self):
        """Finds the amount of trigs in the equation
            Once a trig is found, search again but start after the previous trig

        Args:
            equation (string): equation to be searched

        Returns:
            b(list) : a list of arrays of the first index of a trig
        """
        b = []
        for i in trig:
            t = self.user_in.count(i)
            if t > 0:
                # if a particular trig exists in the trig, find all indexes
                # and append to list
                for x in range(t):
                    b.append(self.user_in.find(i))
        # sort the array from first to last
        if not b:
            return None
        b.sort()
        return b

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
                    # what to do with sec
                    a = self.stack[index]
                    z = op.get(a)
                    if a in trig:
                        self.output.append(self.stack.pop(index))
                    elif a == "(":
                        break
                    elif a != "(" and z > v or z == v:
                        self.output.append(self.stack.pop(index))
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
