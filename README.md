# Credits

*This algorithm is discovered by Javier Cilleruelo, Florian Luca, and Lewis Baxter in 2016*  
I am merely implementing this algorithm; I play absolutely no parts in its discovery.
Check out their full paper here: https://arxiv.org/abs/1602.06208.

# Introduction

Palindrome is a special type of number that looks exactly the same when reading from left to right or from right to left. 131, 1551, 729838927 are examples of palindromes.  
Although most integers are not palindromes, all can be written as the sum of surprisingly few palindromes. For example, 37 = 33 + 4, 10420248 = 10133101 + 235532 + 51615, and  
```
  98765432102358234659182  
= 91110000001110000001119  
+  7004962955005592694007  
+   650469146242641964056  
```

In 2016, Javier Cilleruelo et. al. discovered that all positive integers can be expressed as the sum of three palindromes for all bases greater than 4 (0 is counted as a palindrom as well, so it is equivalent as the sum of at most three positive palindromes). Moreover, they discovered an algorithm that construct the summands.

# Python-Palindrome (rc_palindrome)
This script implemented the algorithm mentioned above.  
It provides the following functions:
```
is_palindrome(num, base: int = 10) -> bool
sum_of_palindromes(num, base: int = 10) -> list
```

1. is_palindrome
  + Parameter 'num' takes in a number. It supports three types: int, str and list.  
    + **If the num is an int, the function will interpret this as a number under the given base (which is 10 by default). Note that this can only represent numbers consist of the first ten digits.**  
    + For example, you cannot express 11<sub>10</sub> in base 16 with this method, since this digit is usually reprenseted by 'b' or "B", which is not an integral digit.  
    + **If the num is a str, then the function will try to parse it under the given base.**
    + For example, "AB" under base 16 is 171<sub>10</sub>.  
    + Supported characters include 0-9 and a-z (does not differentiate lowercase with capital letters).  
    + Can represent the first 36 digits.  
    + **If the num is a list of ints, the function will treat each entry as a separate digit.**  
    + For example, [10, 11] is AB<sub>16</sub>.  
    + Note that this method can represent numbers under arbitrary bases.  
  + Parameter 'base' takes in a base (int). Defaults to 10.  
  + Returns True if the number given is a palindrome, and False if not.  
2. sum_of_palindromes  
  + Parameter 'num' takes in a number, parsed in the say way above.  
  + Parameter 'base' takes in a base (int). Defaults to 10.  
    + If the base is less than 5, the algorithm will not work.  
  + Parameter show takes a bool. If True, the result will be automatically printed out; defaults to False  
  + Parameter check; for debug purposes; defaults to False  
  + Returns a list of palindromes that sum to the given number.  
    + If the base is ten, the palindromes will be represented by ints.  
    + If the base is below 37 but not ten, the palindromes will be represented by strings consist of 0-9 and A-Z.  
    + If the base is above 36, the palindromes will be represented as lists of ints  

I just finished basic testing today; if there is any issue with the program, please contact me on git or via email: yc4120@ic.ac.uk  

Sorrowful T-Rex  
2020 Dec 19  

# Python-Functools (rc_func)  

Contains some helper functions used in the implementation of the algorithm. 
They are maining functional tools, and I used them to enable a combination of imperative and functional programming in Python.  
I have another repo specifically for this; here it only promises to contain the functional tools used in rc_palindromes and may not be updated.  
