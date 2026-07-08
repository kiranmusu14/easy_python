"""
Correlation and Experimental Design
--------------------------------------
How the correlation coefficient quantifies the strength and direction of a
linear relationship between two variables, why it should never be trusted
blindly (non-linear relationships, the need for data transformations, and
the correlation-does-not-imply-causation trap with confounding variables),
and the vocabulary of experimental design: controlled experiments,
randomized controlled trials, placebos, double-blind trials, and
observational (longitudinal vs. cross-sectional) studies.

Table of Contents
1. Relationships between two variables: x and y
2. The correlation coefficient
3. Magnitude: strength of the relationship
4. Sign: direction of the relationship
5. Visualizing relationships: scatterplot and trendline
6. Computing correlation with .corr()
7. The Pearson correlation formula
8. Correlation caveats: non-linear relationships
9. Correlation only accounts for linear relationships
10. Body weight vs. awake time: a skewed relationship
11. Log transformation
12. Other transformations
13. Why use a transformation?
14. Correlation does not imply causation: confounding
15. Vocabulary: treatment and response
16. Controlled experiments
17. Randomized controlled trials and placebos
18. Double-blind trials
19. Observational studies
20. Longitudinal vs. cross-sectional studies
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================================
# 1. Relationships between two variables: x and y
# =====================================================================

# x = the explanatory/independent variable
# y = the response/dependent variable


# =====================================================================
# 2. The correlation coefficient
# =====================================================================

# The correlation coefficient quantifies the linear relationship between
# two variables. It's a number between -1 and 1:
# - Magnitude corresponds to the strength of the relationship.
# - Sign (+ or -) corresponds to the direction of the relationship.


# =====================================================================
# 3. Magnitude: strength of the relationship
# =====================================================================

# 0.99 -> very strong relationship
# 0.75 -> strong relationship
# 0.56 -> moderate relationship
# 0.21 -> weak relationship
# 0.04 -> no relationship (knowing x tells us nothing about y)


# =====================================================================
# 4. Sign: direction of the relationship
# =====================================================================

#  0.75 -> as x increases, y increases
# -0.75 -> as x increases, y decreases


# =====================================================================
# 5. Visualizing relationships: scatterplot and trendline
# =====================================================================

# A scatterplot visualizes the relationship between two numeric variables.
sns.scatterplot(x="sleep_total", y="sleep_rem", data=msleep)
plt.show()

# lmplot() adds a linear trendline to the scatterplot (ci=None hides the
# confidence interval band).
sns.lmplot(x="sleep_total", y="sleep_rem", data=msleep, ci=None)
plt.show()


# =====================================================================
# 6. Computing correlation with .corr()
# =====================================================================

# .corr() is symmetric: the correlation of x with y is the same as y
# with x.
print(msleep['sleep_total'].corr(msleep['sleep_rem']))   # 0.751755
print(msleep['sleep_rem'].corr(msleep['sleep_total']))   # 0.751755


# =====================================================================
# 7. The Pearson correlation formula
# =====================================================================

# There are many ways to calculate correlation; this course uses the
# Pearson product-moment correlation (r), the most common measure:
#
#   r = (1 / (n - 1)) * sum_i[ (x_i - x_bar) * (y_i - y_bar) ] / (sigma_x * sigma_y)
#
# where x_bar is the mean of x and sigma_x is the standard deviation of x
# (similarly for y).
# Variations on this formula include Kendall's tau and Spearman's rho.


# =====================================================================
# 8. Correlation caveats: non-linear relationships
# =====================================================================

# A relationship can look strongly patterned to the eye (e.g. a curve)
# while still having a low correlation coefficient, because correlation
# only measures LINEAR relationships.
# r = 0.18


# =====================================================================
# 9. Correlation only accounts for linear relationships
# =====================================================================

# Correlation shouldn't be used blindly — always visualize the data first,
# since a low correlation can hide a strong non-linear pattern.
print(df['x'].corr(df['y']))  # 0.081094


# =====================================================================
# 10. Body weight vs. awake time: a skewed relationship
# =====================================================================

print(msleep)
#                  name       genus   vore         order  ... sleep_cycle  awake  brainwt   bodywt
# 1             Cheetah    Acinonyx  carni     Carnivora  ...         NaN   11.9      NaN   50.000
# 2          Owl monkey       Aotus   omni      Primates  ...         NaN    7.0  0.01550    0.480
# 3     Mountain beaver  Aplodontia  herbi      Rodentia  ...         NaN    9.6      NaN    1.350
# ...
# 83            Red fox      Vulpes  carni     Carnivora  ...    0.350000   14.2  0.05040    4.230

# bodywt is heavily right-skewed (a few very large mammals), which weakens
# a linear correlation with awake time.
print(msleep['bodywt'].corr(msleep['awake']))  # 0.3119801


# =====================================================================
# 11. Log transformation
# =====================================================================

# Applying a log transformation to the skewed variable can make the
# relationship more linear, increasing the correlation coefficient.
msleep['log_bodywt'] = np.log(msleep['bodywt'])

sns.lmplot(x='log_bodywt',
           y='awake',
           data=msleep,
           ci=None)
plt.show()

print(msleep['log_bodywt'].corr(msleep['awake']))  # 0.5687943


# =====================================================================
# 12. Other transformations
# =====================================================================

# Other common transformations:
# - Log transformation:        log(x)
# - Square root transformation: sqrt(x)
# - Reciprocal transformation:  1 / x
# Transformations can also be combined, e.g. log(x) and log(y), or
# sqrt(x) and 1 / y.


# =====================================================================
# 13. Why use a transformation?
# =====================================================================

# Certain statistical methods rely on variables having a linear
# relationship, including:
# - The correlation coefficient
# - Linear regression (see: Introduction to Linear Modeling in Python)


# =====================================================================
# 14. Correlation does not imply causation: confounding
# =====================================================================

# x being correlated with y does not mean x causes y. A third, unmeasured
# variable — a confounder — can influence both x and y, creating an
# association between them that isn't causal.


# =====================================================================
# 15. Vocabulary: treatment and response
# =====================================================================

# An experiment aims to answer: what is the effect of the treatment on
# the response?
# - Treatment: the explanatory/independent variable
# - Response: the response/dependent variable
# e.g. What is the effect of an advertisement (treatment) on the number of
# products purchased (response)?


# =====================================================================
# 16. Controlled experiments
# =====================================================================

# In a controlled experiment, participants are assigned by researchers to
# either a treatment group (sees the advertisement) or a control group
# (does not).
# The two groups should be comparable so that causation can be inferred.
# If the groups are not comparable, this can lead to confounding (bias),
# e.g.:
#   Treatment group average age: 25
#   Control group average age: 50
#   -> Age is a potential confounder.


# =====================================================================
# 17. Randomized controlled trials and placebos
# =====================================================================

# The gold standard of experiments uses a randomized controlled trial:
# participants are assigned to the treatment/control group randomly, not
# based on any other characteristic. Choosing randomly helps ensure the
# groups are comparable.

# A placebo resembles the treatment but has no effect, so participants
# don't know which group they're in. In clinical trials, a sugar pill
# ensures any observed effect is due to the drug itself, not the idea of
# receiving treatment.


# =====================================================================
# 18. Double-blind trials
# =====================================================================

# In a double-blind trial, the person administering the treatment or
# running the study also doesn't know whether a given participant is
# receiving the real treatment or a placebo.
# This prevents bias in the response and/or analysis of results.
# Fewer opportunities for bias = a more reliable conclusion about
# causation.


# =====================================================================
# 19. Observational studies
# =====================================================================

# In an observational study, participants are NOT assigned randomly to
# groups — they assign themselves, usually based on pre-existing
# characteristics.
# Many research questions aren't conducive to a controlled experiment: you
# can't force someone to smoke, to have a disease, or to have had certain
# past behavior.
# Observational studies can only establish association, not causation:
# effects can be confounded by whatever factors got people into the
# control or treatment group in the first place. There are ways to
# control for confounders to get more reliable conclusions about
# association.


# =====================================================================
# 20. Longitudinal vs. cross-sectional studies
# =====================================================================

# Longitudinal study: participants are followed over a period of time to
# examine the effect of a treatment on a response.
#   e.g. the effect of age on height is not confounded by generation.
#   More expensive, and results take longer.

# Cross-sectional study: data on participants is collected from a single
# snapshot in time.
#   e.g. the effect of age on height IS confounded by generation.
#   Cheaper, faster, and more convenient.
