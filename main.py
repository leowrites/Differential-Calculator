import tree
import derive

# x^2+(x^2-1)^5
if __name__ == "__main__":
    q = 'x^2+(x ^ 2-1)^5'
    tree = tree.tree(q)
    q = tree.parse_fuc(q)
    print(q)
    d = derive.differential(q)
    d.derive(q)
