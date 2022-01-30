import sys

digit_string = int(sys.argv[1])

for i in range(digit_string):
    x = i + 1
    tree = ' ' * (digit_string-x) + '#' * x
    print(tree)
