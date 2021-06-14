import derivative
import parser

if __name__ == "__main__":
    # samples:
    # x^2+(x^2-1)^5
    # 2*x^5-3*x^6
    # x-(1+x^5-6*x^10)^5
    # (8*(x^2-2)^7)*2x
    # (x^2-3)^8
    d = derivative.differential()
    result = d.derive()
    d.print_tree()
    print("\nNodes: {}".format(d.tree))
    print("\nDerivative: {}".format(result))
