"""
Hand-authored multiple-choice questions, keyed by topic id (chapter file
stem). 1-3 per topic where a good conceptual question exists; every topic
additionally receives auto-generated snippet questions in build.py, so
each topic ends up with a full quiz even if it has no hand-authored entry.

Each question is {question, options[4], answer (0-based index), explanation},
focused on WHY the language / library behaves a certain way — the mechanic
or gotcha, not rote recall.
"""

HAND_AUTHORED = {
    # ---- Introduction to Python ----
    "chapter1_hello_python": [
        {
            "question": "Why does `type(day_of_week)` report `int` for `5` but `float` for `weight / height ** 2`?",
            "options": [
                "`/` always produces a float in Python 3, even when both inputs are ints",
                "Exponentiation converts everything to float",
                "Any variable named with an underscore defaults to int",
                "Division rounds, and rounded numbers are always floats",
            ],
            "answer": 0,
            "explanation": "In Python 3 the `/` operator is true division and always yields a float, regardless of operand types. Use `//` for integer (floor) division.",
        },
        {
            "question": "Why does `'ab' + 'cd'` give `'abcd'` while `2 + 3` gives `5`?",
            "options": [
                "Python guesses intent from the variable names",
                "`+` is overloaded: concatenation for str, addition for numbers",
                "Strings are secretly numbers under the hood",
                "`+` always concatenates; `2 + 3` is a special case",
            ],
            "answer": 1,
            "explanation": "The operator dispatches on operand type — `+` calls each type's own implementation. That's why `2 + '3'` raises TypeError rather than guessing.",
        },
    ],
    "chapter2_python_lists": [
        {
            "question": "After `x = [\"a\",\"b\",\"c\"]; y = x; y[1] = \"z\"`, why does `x` also become `['a','z','c']`?",
            "options": [
                "`y = x` copies the list, but index assignment writes through to the original",
                "`y = x` binds y to the *same* list object, so both names see the one mutation",
                "Lists are immutable, so Python silently rebuilt both",
                "Strings inside lists are shared, so only the string changed",
            ],
            "answer": 1,
            "explanation": "`y = x` copies the reference, not the list — both names point at one object. Use `list(x)` or `x[:]` for an independent copy.",
        },
    ],
    # ---- Exploratory Data Analysis ----
    "chapter1_initial_exploration": [
        {
            "question": "A column's `.mean()` returns a number even though the column has missing values. Why no error or NaN?",
            "options": [
                "pandas fills missing values with 0 before averaging",
                "pandas aggregations skip NaN by default (skipna=True)",
                "The missing values were dropped on import",
                "mean() only reads the first non-null value",
            ],
            "answer": 1,
            "explanation": "Most pandas reductions default to skipna=True, quietly ignoring NaN. Convenient, but it can hide data-quality issues — check `.isna().sum()` first.",
        },
    ],
    "chapter2_missing_categorical_numeric_outliers": [
        {
            "question": "Why must `df['col'].str.replace('a','')` be assigned back to the column?",
            "options": [
                "str methods are slow, so caching speeds them up",
                "String operations return a NEW Series; without reassignment the change is discarded",
                "replace() mutates in place; the assignment is only for clarity",
                "The assignment triggers a dtype recompute",
            ],
            "answer": 1,
            "explanation": "Strings (and the Series wrapping them) are immutable — `.str.replace` returns a new Series. Not assigning it back leaves the original unchanged.",
        },
    ],
    # ---- Data Visualization (Matplotlib) ----
    "chapter1_basic_plots": [
        {
            "question": "Why is `fig, ax = plt.subplots()` written as a two-name assignment?",
            "options": [
                "subplots() returns a tuple (Figure, Axes) that gets unpacked into two names",
                "It creates two independent figures at once",
                "fig and ax are keyword arguments set to defaults",
                "The comma makes matplotlib render faster",
            ],
            "answer": 0,
            "explanation": "`plt.subplots()` returns a `(Figure, Axes)` tuple; the comma unpacks it. The Figure is the canvas, the Axes is the plot you draw on.",
        },
        {
            "question": "Several `ax.plot(...)` calls precede a single `plt.show()`. Why do they share one figure?",
            "options": [
                "show() merges the most recent plots automatically",
                "Each plot() draws onto the same Axes; show() just renders the current state",
                "matplotlib caches and deduplicates plots",
                "Only the last plot() actually runs",
            ],
            "answer": 1,
            "explanation": "Plotting calls mutate the Axes; nothing displays until `plt.show()` renders the accumulated state — so you build a figure with several calls, then show once.",
        },
    ],
    # ---- Data Manipulation (pandas) ----
    "chapter1_dataframes_sorting_subsetting": [
        {
            "question": "Why does `df['a']` return a Series but `df[['a','b']]` return a DataFrame?",
            "options": [
                "Double brackets are a tolerated syntax error",
                "The inner list requests multiple columns, so the result stays 2-D (a DataFrame)",
                "Single brackets always return the first column only",
                "It depends on the column dtypes, not the brackets",
            ],
            "answer": 1,
            "explanation": "`df['a']` selects one column → 1-D Series. `df[['a','b']]` passes a list of columns, keeping two dimensions → DataFrame. The extra brackets preserve 2-D shape.",
        },
    ],
    "chapter3_slicing_and_indexing": [
        {
            "question": "Why can `.loc['A':'C']` include row 'C' while `.iloc[0:3]` excludes position 3?",
            "options": [
                ".loc is label-based and inclusive of the end; .iloc is position-based and exclusive",
                "It's a compatibility bug pandas keeps",
                ".loc counts from 1, .iloc from 0",
                "Both are exclusive; the example is wrong",
            ],
            "answer": 0,
            "explanation": "Label slicing (`.loc`) includes the stop label — you named it, so you want it. Positional slicing (`.iloc`) follows Python's half-open ranges and excludes the stop.",
        },
    ],
    "chapter4_visualizing_and_creating_data": [
        {
            "question": "Why is a vectorized column operation preferred over looping rows with `.iterrows()`?",
            "options": [
                "iterrows() can only read, never compute",
                "iterrows() rebuilds a Series per row and drops dtypes — slow and lossy",
                "apply() runs on the GPU",
                "There's no real difference; it's style",
            ],
            "answer": 1,
            "explanation": "`.iterrows()` yields a fresh Series each iteration and coerces mixed dtypes to object — slow and type-lossy. Vectorized operations run in C over the whole column at once.",
        },
    ],
    # ---- Statistics in Python ----
    "chapter1_summary_statistics": [
        {
            "question": "Why is `sample_means = []` created before the `for` loop that appends to it?",
            "options": [
                "Python requires variables to be declared with a type first",
                "The list must exist before the loop can append to it each iteration",
                "Empty brackets reserve memory for speed",
                "It resets any global list of the same name",
            ],
            "answer": 1,
            "explanation": "You accumulate one result per iteration, so the container must exist beforehand — each pass calls `.append()` on it. This underlies building a sampling distribution.",
        },
    ],
    "chapter3_more_distributions": [
        {
            "question": "Why does averaging many samples produce a normal-looking distribution even from skewed data?",
            "options": [
                "The Central Limit Theorem: means of many samples tend toward normal",
                "np.random gradually switches to a normal generator",
                "Larger samples delete outliers automatically",
                "It's a histogram-binning artifact",
            ],
            "answer": 0,
            "explanation": "The CLT says the distribution of sample means approaches normal as the number of samples grows, even for skewed populations — which is why the mean is so well-behaved.",
        },
    ],
}
