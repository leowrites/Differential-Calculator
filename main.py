import derivative
import parser

# x^2+(x^2-1)^5
if __name__ == "__main__":
    
    print('\n\n--------------------Klassen You Are The Best!!--------------------')
    # replace with input
    # remember to have * between a variable and a constant
    raw = 'x^2+(x^2-1)^5'
    test1 = '2*x^5-3*x^6'
    # uin = input("Input: ")
    print("\nInput: {}".format(raw))
    # parser 
    parser = parser.parser()
    processed = parser.parse_fuc(raw)
    print("\nParsed Equation {}".format(processed))
    # create a derivative object
    d = derivative.differential(processed)
    d.tree_constructor()
    derived = d.derivative_constructor()
    d.print_tree()
    print("\nNodes: {}".format(d.tree))
    print("\nDerivative: {}".format(derived))
