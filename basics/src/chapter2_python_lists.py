"""
Python Lists
------------
Why a single variable per value doesn't scale once you have many related
data points, how a list groups them under one name, and the mechanics of
reading, slicing, mutating, and copying a list.

Table of Contents
1. The problem: one variable per value doesn't scale
2. Python lists: grouping values under one name
3. Lists can mix types, and can nest
4. type() on a list
5. Subsetting lists by index
6. List slicing
7. Changing list elements
8. Adding and removing elements
9. Behind the scenes: lists are references, not copies
10. Making an actual copy of a list
"""

# =====================================================================
# 1. The problem: one variable per value doesn't scale
# =====================================================================

# Each of these variables holds a single float, int, str, or bool value.
height = 1.73
tall = True

# Data science deals with many data points at once — one variable per
# height in a family is inconvenient and doesn't scale.
height1 = 1.73
height2 = 1.68
height3 = 1.71
height4 = 1.89


# =====================================================================
# 2. Python lists: grouping values under one name
# =====================================================================

# A list groups a collection of values under one name: [a, b, c].
fam = [1.73, 1.68, 1.71, 1.89]
print(fam)


# =====================================================================
# 3. Lists can mix types, and can nest
# =====================================================================

# A list can contain any type, and different types within the same list.
fam = ["liz", 1.73, "emma", 1.68, "mom", 1.71, "dad", 1.89]
print(fam)

# Lists can also contain other lists (nesting).
fam2 = [["liz", 1.73],
        ["emma", 1.68],
        ["mom", 1.71],
        ["dad", 1.89]]
print(fam2)


# =====================================================================
# 4. type() on a list
# =====================================================================

# Both a flat list and a nested list report the same type: list. What
# varies is the specific functionality/behavior of what's inside.
print(type(fam))   # <class 'list'>
print(type(fam2))  # <class 'list'>


# =====================================================================
# 5. Subsetting lists by index
# =====================================================================

fam = ["liz", 1.73, "emma", 1.68, "mom", 1.71, "dad", 1.89]
print(fam[3])   # 1.68 — zero-based indexing

# Negative indices count from the end of the list.
print(fam[6])   # 'dad'
print(fam[-1])  # 1.89 — same element as fam[7]
print(fam[7])   # 1.89


# =====================================================================
# 6. List slicing
# =====================================================================

# fam[start:end] — start is inclusive, end is exclusive.
fam = ["liz", 1.73, "emma", 1.68, "mom", 1.71, "dad", 1.89]
print(fam[3:5])  # [1.68, 'mom']
print(fam[1:4])  # [1.73, 'emma', 1.68]

# Omitting start or end slices from the beginning or to the end.
print(fam[:4])  # ['liz', 1.73, 'emma', 1.68]
print(fam[5:])  # [1.71, 'dad', 1.89]


# =====================================================================
# 7. Changing list elements
# =====================================================================

fam = ["liz", 1.73, "emma", 1.68, "mom", 1.71, "dad", 1.89]

# Assign to a single index to change one element in place.
fam[7] = 1.86
print(fam)  # [..., 'dad', 1.86]

# Assign to a slice to change a whole range at once.
fam[0:2] = ["lisa", 1.74]
print(fam)  # ['lisa', 1.74, 'emma', 1.68, 'mom', 1.71, 'dad', 1.86]


# =====================================================================
# 8. Adding and removing elements
# =====================================================================

# + concatenates and returns a new list; it doesn't mutate the original.
fam_ext = fam + ["me", 1.79]
print(fam_ext)

# del removes an element from the list in place, by index.
del fam[2]
print(fam)


# =====================================================================
# 9. Behind the scenes: lists are references, not copies
# =====================================================================

# y = x does NOT create a new list — both names point at the same list
# object, so mutating y through an index also changes what x sees.
x = ["a", "b", "c"]
y = x
y[1] = "z"
print(y)  # ['a', 'z', 'c']
print(x)  # ['a', 'z', 'c'] — x changed too, even though only y was assigned to


# =====================================================================
# 10. Making an actual copy of a list
# =====================================================================

# list(x) or x[:] builds a genuinely separate list, so mutating the copy
# leaves the original untouched.
x = ["a", "b", "c"]
y = list(x)   # or: y = x[:]

y[1] = "z"
print(x)  # ['a', 'b', 'c'] — unchanged, unlike the y = x case above
