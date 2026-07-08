"""
Concept dictionary: a flat, ordered list of Python syntax/idiom detectors.

Each entry is {label, detectionRegex, explanation}. For a given topic we
scan its full source against every entry and keep the matches, in this
dictionary's order — that becomes the topic's "Syntax Pointers" panel.

Explanations are about the mechanic or the gotcha, not textbook prose.
Regexes are deliberately narrow to avoid false positives; every one is
tested against every topic by build.py before the output is trusted.

Regex flags: all patterns are matched with re.MULTILINE. Use raw strings.
"""

# Order matters: entries are emitted in this list's order.
CONCEPTS = [
    # ---- Literals & basic values -------------------------------------
    {
        "label": "f-string",
        "regex": r'''(?<![A-Za-z0-9_])[fF](['"]).*?\{.*?\}.*?\1''',
        "explanation": "The f prefix interpolates expressions inside {} at runtime. Without the f, the braces are literal characters and no substitution happens.",
    },
    {
        "label": "Raw string (r-prefix)",
        "regex": r'''(?<![A-Za-z0-9_])[rR](['"]).*?\1''',
        "explanation": "r'...' turns off backslash escaping, so \\n stays two characters. Essential for regex patterns and Windows paths.",
    },
    {
        "label": "Triple-quoted string / docstring",
        "regex": r'"""|\'\'\'',
        "explanation": "Triple quotes span multiple lines verbatim. As the first statement of a module/function/class they become its __doc__ that help() reads.",
    },
    {
        "label": "Byte / unicode string prefix",
        "regex": r'''(?<![A-Za-z0-9_'"])[bB](['"])(?!\1)''',
        "explanation": "b'...' is a bytes literal (raw 8-bit data), not text. You must .decode() bytes to get a str, and can't mix the two with +.",
    },
    {
        "label": "Numeric underscore separator",
        "regex": r"\b\d{1,3}(?:_\d{3})+\b",
        "explanation": "Underscores in numeric literals (1_000_000) are ignored by Python and only aid readability; the value is unchanged.",
    },
    {
        "label": "Complex / scientific notation",
        "regex": r"\b\d+\.?\d*[eE][-+]?\d+\b",
        "explanation": "1e-3 is a float in exponential form. Even 1e0 is a float, not an int — the e forces float type.",
    },

    # ---- Collections & literals --------------------------------------
    {
        "label": "List literal",
        "regex": r"=\s*\[[^\]]*\]",
        "explanation": "Square brackets build a mutable list. Assigning a list to a new name shares the same object — mutating one view mutates both.",
    },
    {
        "label": "Dict literal",
        "regex": r"\{\s*['\"A-Za-z0-9_]+\s*:\s*",
        "explanation": "Braces with key: value pairs build a dict. Since 3.7 insertion order is preserved; duplicate keys keep only the last value.",
    },
    {
        "label": "Set literal",
        "regex": r"=\s*\{[^:{}]+\}",
        "explanation": "Braces with no colons build a set — unordered, de-duplicated. Note {} is an empty dict, not an empty set; use set() for that.",
    },
    {
        "label": "Tuple packing / unpacking",
        "regex": r"^\s*[A-Za-z_]\w*\s*,\s*[A-Za-z_]\w*\s*=",
        "explanation": "a, b = ... unpacks an iterable into multiple names by position. The right side must have exactly as many items as names.",
    },
    {
        "label": "Nested list / 2D structure",
        "regex": r"(?:=|\(|return)\s*\[\s*\[",
        "explanation": "A list of lists is Python's basic 2D structure. Indexing is [row][col]; the inner lists are independent objects.",
    },

    # ---- Indexing & slicing ------------------------------------------
    {
        "label": "Negative indexing",
        "regex": r"\[\s*-\d+\s*\]",
        "explanation": "[-1] counts from the end, so -1 is the last element. Going past the start (too-negative) raises IndexError, unlike slicing.",
    },
    {
        "label": "Slicing [start:stop]",
        "regex": r"\[\s*-?\w*\s*:\s*-?\w*\s*\]",
        "explanation": "start is inclusive, stop is exclusive. Omitting either end defaults to the beginning/end; slicing never raises for out-of-range bounds.",
    },
    {
        "label": "Strided slice [::step]",
        "regex": r"\[\s*-?\w*\s*:\s*-?\w*\s*:\s*-?\w+\s*\]",
        "explanation": "The third value is the step. [::-1] reverses a sequence; [::2] takes every other element.",
    },
    {
        "label": "Full-copy slice [:]",
        "regex": r"=\s*\w+\[\s*:\s*\]",
        "explanation": "x[:] makes a shallow copy of a sequence, so mutating the copy leaves the original alone — unlike a plain y = x reference.",
    },

    # ---- Operators ---------------------------------------------------
    {
        "label": "Exponentiation (**)",
        "regex": r"\*\*\s*\d",
        "explanation": "** is power, not ^ (which is bitwise XOR in Python). It binds tighter than unary minus: -2**2 is -4.",
    },
    {
        "label": "Floor division (//)",
        "regex": r"(?<![/*])//(?![/*])",
        "explanation": "// divides and rounds toward negative infinity, so -7 // 2 is -4, not -3. Returns int only if both operands are ints.",
    },
    {
        "label": "Augmented assignment (+=, *=)",
        "regex": r"[-+*/%]=\s",
        "explanation": "x += y is in-place for mutable objects (list.extend) but rebinds for immutables (int). This distinction bites with shared lists.",
    },
    {
        "label": "Chained comparison",
        "regex": r"\b\w+\s*[<>]=?\s*\w+\s*[<>]=?\s*\w+",
        "explanation": "1 < x < 10 is real chaining — x is evaluated once and both comparisons must hold, unlike most languages where it would parse as booleans.",
    },
    {
        "label": "Identity test (is / is not)",
        "regex": r"\bis(\s+not)?\b",
        "explanation": "is compares identity (same object), not equality. Use it only for None; using it for numbers/strings works by accident via caching.",
    },
    {
        "label": "Membership test (in)",
        "regex": r"(?<!\bfor )(?<!\w)\bin\b(?! .*:)",
        "explanation": "x in coll checks membership — O(1) for sets/dicts, O(n) for lists. For dicts it tests keys, not values.",
    },
    {
        "label": "Boolean operators (and / or / not)",
        "regex": r"\b(and|or|not)\b",
        "explanation": "and/or short-circuit and return an operand, not a bool: 'a' or 'b' is 'a'. Handy for defaults but surprising when you expected True/False.",
    },
    {
        "label": "Ternary conditional expression",
        "regex": r"\S+\s+if\s+.+\s+else\s+\S+",
        "explanation": "value_if_true if cond else value_if_false is an expression, so it can sit inside a list comprehension or a return.",
    },
    {
        "label": "Walrus operator (:=)",
        "regex": r":=",
        "explanation": "The walrus assigns and returns in one expression, letting you capture a value inside a while/if condition without a separate line.",
    },

    # ---- Comprehensions ----------------------------------------------
    {
        "label": "List comprehension",
        "regex": r"\[[^\[\]]*\bfor\b[^\[\]]*\]",
        "explanation": "[expr for x in it] builds a list in one pass. Faster than an append loop and creates no leftover loop variable in 3.x.",
    },
    {
        "label": "Comprehension with filter (if)",
        "regex": r"\[[^\[\]]*\bfor\b[^\[\]]*\bif\b[^\[\]]*\]",
        "explanation": "A trailing if filters items (keep-or-drop). This differs from a leading if/else, which transforms every item.",
    },
    {
        "label": "Dict comprehension",
        "regex": r"\{[^{}]*:[^{}]*\bfor\b[^{}]*\}",
        "explanation": "{k: v for ...} builds a dict directly. Later duplicate keys overwrite earlier ones silently.",
    },
    {
        "label": "Set comprehension",
        "regex": r"\{[^{}:]*\bfor\b[^{}:]*\}",
        "explanation": "{expr for ...} builds a set — de-duplicates as it goes. Same syntax as a dict comprehension but with no colon.",
    },
    {
        "label": "Generator expression",
        "regex": r"\((?:[^()]*?)\bfor\b(?:[^()]*?)\)",
        "explanation": "Parentheses instead of brackets make a lazy generator — items are produced on demand, so it's memory-cheap for large or infinite streams.",
    },

    # ---- Control flow -------------------------------------------------
    {
        "label": "if / elif / else",
        "regex": r"^\s*(if|elif|else)\b.*:",
        "explanation": "Only the first truthy branch runs. elif avoids nesting; the colon and indentation (not braces) define the block.",
    },
    {
        "label": "for loop",
        "regex": r"^\s*for\s+.+\s+in\s+.+:",
        "explanation": "Python's for iterates over items directly, not indices. To get indices too, wrap the iterable in enumerate().",
    },
    {
        "label": "while loop",
        "regex": r"^\s*while\s+.+:",
        "explanation": "Repeats while the condition stays truthy. Forgetting to change the condition inside gives an infinite loop (Ctrl+C to break).",
    },
    {
        "label": "enumerate()",
        "regex": r"\benumerate\s*\(",
        "explanation": "enumerate(seq) yields (index, item) pairs so you get the counter without a manual i += 1. Pass start= to begin at 1.",
    },
    {
        "label": "zip()",
        "regex": r"\bzip\s*\(",
        "explanation": "zip pairs items from several iterables and stops at the shortest one. It returns a one-shot iterator, exhausted after one pass.",
    },
    {
        "label": "range()",
        "regex": r"\brange\s*\(",
        "explanation": "range is a lazy sequence, not a list — it computes values on demand. range(stop) excludes stop, matching zero-based indexing.",
    },
    {
        "label": "break / continue",
        "regex": r"^\s*(break|continue)\b",
        "explanation": "break exits the whole loop; continue skips to the next iteration. Both affect only the innermost enclosing loop.",
    },
    {
        "label": "pass statement",
        "regex": r"^\s*pass\s*$",
        "explanation": "pass is a no-op placeholder where syntax requires a statement but you have nothing to do yet.",
    },
    {
        "label": "match / case (structural pattern)",
        "regex": r"^\s*(match|case)\b.*:",
        "explanation": "match/case (3.10+) destructures by shape, not just value equality — it can bind sub-parts of tuples/objects in each case.",
    },

    # ---- Functions ----------------------------------------------------
    {
        "label": "Function definition (def)",
        "regex": r"^\s*def\s+\w+\s*\(",
        "explanation": "def creates a function object at runtime. Default argument values are evaluated once at definition — mutable defaults are a classic trap.",
    },
    {
        "label": "return statement",
        "regex": r"^\s*return\b",
        "explanation": "A function with no return (or a bare return) yields None. Returning multiple comma-separated values actually returns one tuple.",
    },
    {
        "label": "Default argument value",
        "regex": r"def\s+\w+\s*\([^)]*\w+\s*=",
        "explanation": "Defaults let callers omit arguments. A mutable default like []= is shared across all calls — use None as the sentinel instead.",
    },
    {
        "label": "*args (variadic positional)",
        "regex": r"def\s+\w+\s*\([^)]*\*\w+",
        "explanation": "*args collects extra positional arguments into a tuple, so the function accepts any number of them.",
    },
    {
        "label": "**kwargs (variadic keyword)",
        "regex": r"def\s+\w+\s*\([^)]*\*\*\w+",
        "explanation": "**kwargs collects extra keyword arguments into a dict. Combined with *args it forwards arbitrary call signatures.",
    },
    {
        "label": "Keyword argument at call site",
        "regex": r"\w+\s*\(\s*[^)]*\b\w+\s*=\s*[^=]",
        "explanation": "name=value at a call passes by name, so order doesn't matter and intent is explicit. Keyword args must follow positional ones.",
    },
    {
        "label": "Lambda expression",
        "regex": r"\blambda\b[^:]*:",
        "explanation": "lambda is a one-expression anonymous function. It can't contain statements — use a def when you need more than a single expression.",
    },
    {
        "label": "Type hint / annotation",
        "regex": r"def\s+\w+\s*\([^)]*:\s*\w+|->\s*\w+\s*:",
        "explanation": "Annotations document expected types and power tools like mypy, but Python does not enforce them at runtime.",
    },
    {
        "label": "Decorator (@)",
        "regex": r"^\s*@\w[\w.]*",
        "explanation": "@deco above a def replaces the function with deco(function). It's syntactic sugar for wrapping behavior (caching, timing, routing).",
    },
    {
        "label": "Nested / higher-order function",
        "regex": r"def\s+\w+.*\n(?:.*\n)*?\s+def\s+\w+",
        "explanation": "A function defined inside another closes over the enclosing locals (a closure), remembering them after the outer call returns.",
    },

    # ---- Iterators & generators --------------------------------------
    {
        "label": "yield (generator function)",
        "regex": r"^\s*yield\b",
        "explanation": "yield turns a function into a generator: each call resumes after the last yield, keeping local state, producing values lazily.",
    },
    {
        "label": "iter() / next()",
        "regex": r"\b(iter|next)\s*\(",
        "explanation": "next() pulls one value from an iterator and raises StopIteration when exhausted. Pass a default to next() to avoid the exception.",
    },

    # ---- Classes & objects -------------------------------------------
    {
        "label": "Class definition",
        "regex": r"^\s*class\s+\w+",
        "explanation": "class defines a new type. Methods take self explicitly as the first parameter — it's the instance, passed automatically on call.",
    },
    {
        "label": "__init__ / dunder method",
        "regex": r"def\s+__\w+__\s*\(",
        "explanation": "Dunder methods hook into syntax: __init__ runs on construction, __len__ powers len(), __eq__ powers ==. Python calls them for you.",
    },
    {
        "label": "self parameter",
        "regex": r"def\s+\w+\s*\(\s*self\b",
        "explanation": "self is the instance the method was called on. It's a naming convention, not a keyword, but the first arg always receives the instance.",
    },
    {
        "label": "@dataclass",
        "regex": r"@dataclass",
        "explanation": "@dataclass auto-generates __init__, __repr__ and __eq__ from annotated fields, cutting boilerplate for record-like classes.",
    },
    {
        "label": "@property",
        "regex": r"@property",
        "explanation": "@property exposes a method as an attribute, so obj.x runs code without parentheses — useful for computed or validated values.",
    },
    {
        "label": "@staticmethod / @classmethod",
        "regex": r"@(staticmethod|classmethod)",
        "explanation": "@staticmethod takes no implicit first arg; @classmethod receives the class (cls) instead of an instance, handy for alternate constructors.",
    },
    {
        "label": "isinstance() / type()",
        "regex": r"\b(isinstance|type)\s*\(",
        "explanation": "isinstance() respects inheritance (subclasses count); type() checks the exact class. Prefer isinstance for behavior checks.",
    },
    {
        "label": "super()",
        "regex": r"\bsuper\s*\(\s*\)",
        "explanation": "super() calls the parent implementation following the method-resolution order, so cooperative multiple inheritance works correctly.",
    },

    # ---- Context managers & exceptions -------------------------------
    {
        "label": "with statement (context manager)",
        "regex": r"^\s*with\s+.+:",
        "explanation": "with guarantees cleanup (closing files, releasing locks) via __enter__/__exit__ even if the block raises — no manual finally needed.",
    },
    {
        "label": "try / except",
        "regex": r"^\s*(try|except)\b.*:",
        "explanation": "Catch the narrowest exception you can. A bare except: also swallows KeyboardInterrupt and SystemExit — almost always a mistake.",
    },
    {
        "label": "finally / else on try",
        "regex": r"^\s*finally\s*:",
        "explanation": "finally always runs (cleanup), even on return or re-raise. The try/else block runs only if no exception occurred.",
    },
    {
        "label": "raise statement",
        "regex": r"^\s*raise\b",
        "explanation": "raise throws an exception. A bare raise inside except re-raises the current one, preserving the original traceback.",
    },
    {
        "label": "assert statement",
        "regex": r"^\s*assert\b",
        "explanation": "assert checks an invariant and raises AssertionError if false. It's stripped when Python runs with -O, so never use it for real validation.",
    },

    # ---- Async --------------------------------------------------------
    {
        "label": "async def",
        "regex": r"^\s*async\s+def\b",
        "explanation": "async def defines a coroutine that returns immediately as an awaitable; its body runs only when awaited or scheduled on an event loop.",
    },
    {
        "label": "await expression",
        "regex": r"\bawait\b",
        "explanation": "await suspends the coroutine until the awaited task finishes, yielding control to the event loop meanwhile. Only valid inside async def.",
    },

    # ---- Imports & modules -------------------------------------------
    {
        "label": "import module",
        "regex": r"^\s*import\s+\w+",
        "explanation": "import binds the module object; you reach its contents via the dotted prefix, keeping the origin of every name explicit.",
    },
    {
        "label": "import ... as (alias)",
        "regex": r"^\s*import\s+[\w.]+\s+as\s+\w+",
        "explanation": "Aliasing (import numpy as np) shortens a long name while keeping the prefix, so calls still read as clearly coming from that package.",
    },
    {
        "label": "from ... import",
        "regex": r"^\s*from\s+[\w.]+\s+import\b",
        "explanation": "from x import y pulls a name into the local namespace, so no prefix is needed — but it obscures which module y actually came from.",
    },
    {
        "label": "__name__ == '__main__' guard",
        "regex": r"__name__\s*==\s*['\"]__main__['\"]",
        "explanation": "This guard runs code only when the file is executed directly, not when imported — letting a module double as a script and a library.",
    },

    # ---- Built-ins & string ops --------------------------------------
    {
        "label": "print()",
        "regex": r"\bprint\s*\(",
        "explanation": "print() writes to stdout with a trailing newline. Control it with sep=, end=, and file= — e.g. end='' to suppress the newline.",
    },
    {
        "label": "len()",
        "regex": r"\blen\s*\(",
        "explanation": "len() is O(1) — containers store their size. It calls the object's __len__; objects without one raise TypeError.",
    },
    {
        "label": "String .format()",
        "regex": r"\.\s*format\s*\(",
        "explanation": ".format() substitutes {} placeholders positionally or by name. f-strings are the newer, faster equivalent for literals.",
    },
    {
        "label": "String join()",
        "regex": r"['\"].*['\"]\s*\.\s*join\s*\(",
        "explanation": "sep.join(items) is the efficient way to concatenate many strings — repeated + builds throwaway intermediates. Items must all be str.",
    },
    {
        "label": "String split()",
        "regex": r"\.\s*split\s*\(",
        "explanation": "split() with no arg splits on any run of whitespace and drops empties; split(',') keeps empty fields between delimiters.",
    },
    {
        "label": "String strip/replace",
        "regex": r"\.\s*(strip|lstrip|rstrip|replace)\s*\(",
        "explanation": "Strings are immutable, so these return a new string — the original is unchanged. Assign the result or it's lost.",
    },
    {
        "label": "String case methods",
        "regex": r"\.\s*(upper|lower|capitalize|title)\s*\(",
        "explanation": "Case methods return a new string. capitalize() lowercases everything after the first letter; title() capitalizes each word.",
    },
    {
        "label": "sorted() / sort()",
        "regex": r"\b(sorted\s*\(|\.\s*sort\s*\()",
        "explanation": "sorted() returns a new list; list.sort() sorts in place and returns None. Use key= for custom order, reverse=True to flip.",
    },
    {
        "label": "map() / filter()",
        "regex": r"\b(map|filter)\s*\(",
        "explanation": "Both return lazy iterators, not lists — wrap in list() to materialize. A comprehension is usually clearer for the same job.",
    },
    {
        "label": "sum() / min() / max()",
        "regex": r"\b(sum|min|max)\s*\(",
        "explanation": "These consume any iterable. min/max accept a key= like sorted; on an empty iterable they raise unless you pass default=.",
    },
    {
        "label": "any() / all()",
        "regex": r"\b(any|all)\s*\(",
        "explanation": "any()/all() short-circuit on the first decisive item. all() on an empty iterable is True; any() on empty is False.",
    },
    {
        "label": "help() / dir()",
        "regex": r"\b(help|dir)\s*\(",
        "explanation": "help() prints an object's docstring-based manual; dir() lists its attributes/methods. Both work live without leaving the shell.",
    },

    # ---- Dict & list methods -----------------------------------------
    {
        "label": "dict .items() / .keys() / .values()",
        "regex": r"\.\s*(items|keys|values)\s*\(\s*\)",
        "explanation": "These return live views that track later dict changes. Iterating a bare dict yields keys; use .items() to get key and value together.",
    },
    {
        "label": "dict .get() with default",
        "regex": r"\.\s*get\s*\(",
        "explanation": ".get(key, default) returns default instead of raising KeyError when the key is absent — safer than dict[key] for optional keys.",
    },
    {
        "label": "list .append() / .extend()",
        "regex": r"\.\s*(append|extend)\s*\(",
        "explanation": "append adds one item; extend adds each item of an iterable. append(list) nests a whole list as a single element — a common mix-up.",
    },
    {
        "label": "list .index() / .count()",
        "regex": r"\.\s*(index|count)\s*\(",
        "explanation": ".index() returns the first match's position and raises ValueError if absent; .count() returns how many times a value appears.",
    },
    {
        "label": "del statement",
        "regex": r"^\s*del\s+\w+",
        "explanation": "del removes a name binding or a container element in place. Deleting from a list shifts later indices down by one.",
    },

    # ---- NumPy / pandas idioms (data-science topics) -----------------
    {
        "label": "Boolean mask indexing",
        "regex": r"\w+\s*\[\s*\w+\s*[<>=!]=?\s*",
        "explanation": "arr[arr > x] selects elements where the boolean array is True. It's vectorized — no Python loop — and returns a filtered copy.",
    },
    {
        "label": "Vectorized array arithmetic",
        "regex": r"\bnp_\w+\s*[-+*/]\s*np_\w+|\barray\([^)]*\)\s*[-+*/]",
        "explanation": "NumPy applies +, -, * element-wise across whole arrays at C speed, so you never write an explicit element loop.",
    },
    {
        "label": "np.array()",
        "regex": r"\bnp\.\s*array\s*\(",
        "explanation": "np.array coerces to one dtype for the whole array — mixing int and float upcasts everything to float. That homogeneity is what makes it fast.",
    },
    {
        "label": "Double-bracket column selection",
        "regex": r"[\w\)\]]\s*\[\s*\[",
        "explanation": "df[['a','b']] returns a DataFrame of several columns; the inner list is the column names. Single brackets df['a'] give a 1-D Series instead — the extra brackets are what keep it 2-D.",
    },
    {
        "label": "DataFrame .loc / .iloc",
        "regex": r"\.\s*(loc|iloc)\s*\[",
        "explanation": ".loc selects by label (end-inclusive!), .iloc by integer position (end-exclusive). Mixing them up is the classic pandas indexing bug.",
    },
    {
        "label": "pd.read_csv()",
        "regex": r"\bread_csv\s*\(",
        "explanation": "read_csv infers dtypes column by column. Pass index_col= to promote a column to the index and parse_dates= to get real datetimes.",
    },
    {
        "label": "DataFrame .groupby()",
        "regex": r"\.\s*groupby\s*\(",
        "explanation": "groupby splits rows by key, then you apply an aggregation — nothing is computed until that aggregation runs (split-apply-combine).",
    },
    {
        "label": "DataFrame .apply()",
        "regex": r"\.\s*apply\s*\(",
        "explanation": ".apply(func) runs a Python function per row/column — flexible but far slower than a vectorized column operation; prefer the latter when possible.",
    },
    {
        "label": "DataFrame .iterrows()",
        "regex": r"\.\s*iterrows\s*\(",
        "explanation": "iterrows() yields (label, Series) pairs but rebuilds a Series each iteration and loses dtypes — treat it as a last resort, not a default.",
    },
    {
        "label": "DataFrame aggregation (.mean/.sum/.agg)",
        "regex": r"\.\s*(mean|sum|median|std|agg|describe)\s*\(",
        "explanation": "These skip NaN by default, so a column's mean ignores missing values silently — check .isna().sum() if that matters.",
    },
    {
        "label": "Method chaining",
        "regex": r"\)\s*\.\s*\w+\s*\(",
        "explanation": "Chaining a.b().c() reads left-to-right as a pipeline. Each call returns an object the next call operates on; a broken link mid-chain is harder to debug.",
    },
]
