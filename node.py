class node:
    def __init__(self, fx=None, fp=None, l=None, r=None, op=None, parent=None):
        self.fx = fx
        self.fp = fp
        # to store derivatives from children
        self.left = l
        self.right = r
        self.op  = op
        self.parent = parent