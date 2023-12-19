import PyNewtFrac
from sympy import symbols, diff

'''
    When the program is "waiting for input", you can either:
        - press W to zoom in
        - press S to zoom out
        - press C to change the colours, in case you don't like them
        - press I to re-render, in case you want to change some params
'''

symbol = symbols('x')

input_data = input("Enter a polynomial: ")

f = lambda x: eval(input_data)
f1 = diff(f, symbol)

x0 = - 3 + 2j

resolution = 600

# f = lambda x: x ** 4 + 5
# f1 = lambda x: 4 * x ** 3

# x0 = input("Enter the lambda value to start (for example '-3+2j'): ")
# resolution = int(input("Enter the resolution value to start (for example '600'): "))

PyNewtFrac.newton_roots_coloring(f, f1, x0, resolution)
