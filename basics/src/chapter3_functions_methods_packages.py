"""
Functions, Methods & Packages
-----------------------------
Functions as reusable, pre-written pieces of code you call instead of
re-implementing yourself; methods as functions that belong to a specific
object's type; and packages as the mechanism for sharing and reusing
someone else's functions and methods via import.

Table of Contents
1. Functions: reusable code that solves one task
2. round(): a function that takes more than one argument
3. Finding functions for a standard task
4. Methods: functions that belong to an object
5. list methods: index() and count()
6. str methods: capitalize() and replace()
7. Different types have different methods
8. list methods (2): append()
9. Packages: why not ship everything in core Python
10. Installing and importing a package
"""

# =====================================================================
# 1. Functions: reusable code that solves one task
# =====================================================================

# type() is already a function: a piece of reusable code that solves a
# particular task. Calling a function means you don't have to write the
# code yourself.
fam = [1.73, 1.68, 1.71, 1.89]
print(fam)
print(max(fam))  # 1.89 — max() is a built-in function

# Store a function's return value in a variable to reuse it.
tallest = max(fam)
print(tallest)


# =====================================================================
# 2. round(): a function that takes more than one argument
# =====================================================================

# round(number, ndigits) — ndigits controls precision; omitting it rounds
# to the nearest whole number instead.
print(round(1.68, 1))  # 1.7
print(round(1.68))     # 2

# help() opens a function's documentation without leaving the shell.
help(round)


# =====================================================================
# 3. Finding functions for a standard task
# =====================================================================

# Getting a list's index, or reversing it, are standard tasks — a
# built-in function almost certainly already exists for them. When in
# doubt, the internet (and help()) is the fastest way to check.


# =====================================================================
# 4. Methods: functions that belong to an object
# =====================================================================

# Everything in Python is an object, and every object has methods
# associated with it, depending on its type.
sister = "liz"
height = 1.73
fam = ["liz", 1.73, "emma", 1.68,
       "mom", 1.71, "dad", 1.89]


# =====================================================================
# 5. list methods: index() and count()
# =====================================================================

print(fam)
print(fam.index("mom"))  # 4 — call method index() on fam
print(fam.count(1.73))   # 1 — how many times 1.73 appears


# =====================================================================
# 6. str methods: capitalize() and replace()
# =====================================================================

print(sister)                    # 'liz'
print(sister.capitalize())       # 'Liz'
print(sister.replace("z", "sa"))  # 'lisa'


# =====================================================================
# 7. Different types have different methods
# =====================================================================

# A method that exists on str doesn't exist on list, because the
# methods available depend on the object's type.
print(sister.replace("z", "sa"))  # 'lisa' — fine, sister is a str
# fam.replace("mom", "mommy")     # AttributeError: 'list' object has no attribute 'replace'

print(sister.index("z"))  # 2
print(fam.index("mom"))   # 4


# =====================================================================
# 8. list methods (2): append()
# =====================================================================

# append() mutates the list in place, adding one element at the end.
print(fam)
fam.append("me")
print(fam)
fam.append(1.79)
print(fam)


# =====================================================================
# 9. Packages: why not ship everything in core Python
# =====================================================================

# Putting every possible function/method into the base Python
# distribution would make it a huge, messy, hard-to-maintain codebase
# full of code most people never use. Instead, a package is a directory
# of Python scripts (each script is a module) that specifies functions,
# methods, and types for one purpose — e.g. NumPy, Matplotlib,
# scikit-learn — installed only if you need it.


# =====================================================================
# 10. Installing and importing a package
# =====================================================================

# Installed once from the terminal, e.g.:
#   python3 get-pip.py
#   pip3 install numpy

# import numpy makes its contents available only via the numpy. prefix —
# calling array() directly still fails.
import numpy
# array([1, 2, 3])          # NameError: name 'array' is not defined
print(numpy.array([1, 2, 3]))

# import numpy as np gives it a shorter alias.
import numpy as np
print(np.array([1, 2, 3]))

# from numpy import array pulls one name into the current namespace
# directly, no prefix needed — but it's less clear later in the code
# which package a bare name like array() came from.
from numpy import array
print(array([1, 2, 3]))

# Same script, less clear which package `array` came from:
fam = ["liz", 1.73, "emma", 1.68,
       "mom", 1.71, "dad", 1.89]
fam_ext = fam + ["me", 1.79]
print(str(len(fam_ext)) + " elements in fam_ext")
np_fam = array(fam_ext)

# Same script, using the np. prefix makes the NumPy dependency explicit.
fam_ext = fam + ["me", 1.79]
print(str(len(fam_ext)) + " elements in fam_ext")
np_fam = np.array(fam_ext)  # clearly using NumPy
