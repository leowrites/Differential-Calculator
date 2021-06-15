from gui import app


# Derivative Calculator for Calculus 12 Final Project
# 06/07/2021 - 06/13/2021
# By Leo Liu
# Note - Supports chain rule, product rule, quotient rule, addition and subtraction
# IMPORTANT - you must have * between a constant and a variable to show multiplication

if __name__ == "__main__":
    # try these samples to get started
    # samples:
    # x^2+(x^2-1)^5
    # 2*x^5-3*x^6
    # x-(1+x^5-6*x^10)^5
    # (8*(x^2-2)^7)*2x
    # (x^2-3)^8
    # 4/(9-x^2)
    # ((2*x+3)^3)/(4*x-7)
    # (sin(x))+(cos(x))
    # 1/((sec(2*x)-1)^3)^(1/2)
    app = app()
    app.main()
