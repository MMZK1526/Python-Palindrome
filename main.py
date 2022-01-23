# This main function only supports base-10 numbers simply because I am lazy LOL

import sys
from rc_func import *
from rc_palindrome import *


if len(sys.argv) < 2:
    print("Please provide me a number!")

try:
    print(sys.argv[1] + " = ", end="")
    l_print(sum_of_palindromes(sys.argv[1], 10), separator=" + ", brackets="")
except Exception as e:
    print("Please enter a valid positive integer")
