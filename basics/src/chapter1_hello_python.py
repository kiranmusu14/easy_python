"""
Hello Python! — Getting Started
--------------------------------
First contact with Python as a language and as a tool: what the IPython
Shell is for, how a .py script differs from typing in the shell, and the
basics of naming a variable and asking Python what type it holds.

Table of Contents
1. The IPython Shell vs. a Python script
2. Variables: naming and assigning a value
3. Worked example: calculating BMI
4. Reproducibility: why scripts beat one-off shell commands
5. Python types: float, int, str, bool
6. Types change behavior: + means different things for different types
"""

# =====================================================================
# 1. The IPython Shell vs. a Python script
# =====================================================================

# The IPython Shell executes one Python command at a time and shows the
# result immediately — good for quick experiments, not for saved work.
#   In [1]: 2 + 3
#   Out[1]: 5

# A Python script is a text file (.py) holding a list of Python commands,
# run top to bottom, similar to typing the same lines into the shell.
# Because the shell doesn't echo values in a script, use print() to see
# output when running a .py file.
print(2 + 3)


# =====================================================================
# 2. Variables: naming and assigning a value
# =====================================================================

# A variable is a specific, case-sensitive name you can use later to call
# up the value it was assigned.
height = 1.79
weight = 68.7

# Typing the variable name (in the shell) or printing it recalls the value.
print(height)


# =====================================================================
# 3. Worked example: calculating BMI
# =====================================================================

# BMI = weight / height**2 — build the formula up from the variables
# above instead of retyping the raw numbers.
bmi = weight / height ** 2
print(bmi)  # 21.4413


# =====================================================================
# 4. Reproducibility: why scripts beat one-off shell commands
# =====================================================================

# Re-running the script after changing one variable reproduces the whole
# calculation with no manual re-typing — the point of writing a script
# instead of working line-by-line in the shell.
height = 1.79
weight = 74.2  # <- updated input
bmi = weight / height ** 2
print(bmi)  # 23.1578


# =====================================================================
# 5. Python types: float, int, str, bool
# =====================================================================

# type() reports what kind of value a variable holds.
print(type(bmi))  # <class 'float'>

day_of_week = 5
print(type(day_of_week))  # <class 'int'>

# Strings can use single or double quotes interchangeably.
x = "body mass index"
y = 'this works too'
print(type(y))  # <class 'str'>

z = True
print(type(z))  # <class 'bool'>


# =====================================================================
# 6. Types change behavior: + means different things for different types
# =====================================================================

# The same operator behaves differently depending on the operand types:
# numeric + is arithmetic addition, string + is concatenation.
print(2 + 3)        # 5
print('ab' + 'cd')  # 'abcd'
