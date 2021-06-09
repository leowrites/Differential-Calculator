import tree
import derive
if __name__ == "__main__":
    q = input("Input Equation: ")
    tree = tree.tree(q)
    q = tree.parse_fuc(q)
    print(q)
    d = derive.differential(q)