"""
What is Statistics? — Summary Statistics
-----------------------------------------
An introduction to what the field of statistics can (and can't) answer, the
distinction between descriptive and inferential statistics, the main types
of data, and how to summarize a dataset's center (mean, median, mode) and
spread (variance, standard deviation, quantiles, IQR, outliers) using NumPy,
pandas, and SciPy on the `msleep` mammal-sleep dataset (83 mammals' sleep
statistics, assumed already loaded as a pandas DataFrame).

Table of Contents
1. What is statistics?
2. Types of statistics: descriptive vs. inferential
3. Types of data: numeric vs. categorical
4. Why data type matters: summary statistics differ by type
5. The msleep dataset
6. Measures of center: mean
7. Measures of center: median
8. Measures of center: mode
9. How outliers affect mean vs. median
10. Choosing mean vs. median: skew
11. Measures of spread: variance
12. Measures of spread: standard deviation
13. Mean absolute deviation
14. Quantiles and quartiles
15. Quantiles with np.linspace()
16. Interquartile range (IQR)
17. Using the IQR to find outliers
18. All summary statistics at once: describe()
"""

import numpy as np
import pandas as pd
import statistics
import matplotlib.pyplot as plt
from scipy.stats import iqr

# =====================================================================
# 1. What is statistics?
# =====================================================================

# The field of statistics is the practice and study of collecting and
# analyzing data. A summary statistic is a single fact/number that
# summarizes a larger set of data.

# Statistics can help answer questions such as:
# - How likely is someone to purchase a product?
# - How many occupants will a hotel have, and how can occupancy be optimized?
# - What sizes of jeans need to be manufactured to fit 95% of the population?
# - Which of two ads is more effective (A/B testing)?

# What statistics can't do: it can't answer "why" questions directly.
# e.g. "Why is Game of Thrones so popular?" can't be answered by statistics,
# but a related, measurable question can be: "Are series with more violent
# scenes viewed by more people?" Even then, correlation between violence and
# views can't tell us that violent scenes *cause* more views.


# =====================================================================
# 2. Types of statistics: descriptive vs. inferential
# =====================================================================

# Descriptive statistics: describe and summarize the data you have.
#   e.g. 50% of friends drive to work, 25% take the bus, 25% bike.

# Inferential statistics: use a sample of data to make inferences about a
# larger population.
#   e.g. What percent of *all* people drive to work, based on a sample?


# =====================================================================
# 3. Types of data: numeric vs. categorical
# =====================================================================

# Numeric (quantitative) data:
#   Continuous (measured) - e.g. airplane speed, time spent waiting in line
#   Discrete (counted)    - e.g. number of pets, number of packages shipped

# Categorical (qualitative) data:
#   Nominal (unordered)   - e.g. married/unmarried, country of residence
#   Ordinal (ordered)     - e.g. strongly disagree ... strongly agree

# Categorical data can be represented as numbers, e.g.:
#   Nominal:  married/unmarried -> (1 / 0), country of residence -> (1, 2, ...)
#   Ordinal:  strongly disagree (1), somewhat disagree (2),
#             neither agree nor disagree (3), somewhat agree (4),
#             strongly agree (5)
# Even when represented as numbers, these are still categorical: they can't
# be meaningfully added, averaged, etc.


# =====================================================================
# 4. Why data type matters: summary statistics differ by type
# =====================================================================

# Numeric data: a summary statistic like the mean makes sense.
print(np.mean(car_speeds['speed_mph']))  # 40.09062

# Categorical data: counting the occurrences of each category makes sense
# instead of averaging them.
print(demographics['marriage_status'].value_counts())
# single      188
# married     143
# divorced    124
# dtype: int64


# =====================================================================
# 5. The msleep dataset
# =====================================================================

# msleep holds sleep statistics for 83 mammals: name, genus, diet (vore),
# order, sleep_total, sleep cycle, awake time, brain weight, body weight...
print(msleep)
#                  name       genus   vore         order  ... sleep_cycle  awake  brainwt   bodywt
# 1             Cheetah    Acinonyx  carni     Carnivora  ...         NaN   11.9      NaN   50.000
# 2          Owl monkey       Aotus   omni      Primates  ...         NaN    7.0  0.01550    0.480
# 3     Mountain beaver  Aplodontia  herbi      Rodentia  ...         NaN    9.6      NaN    1.350
# ...
# 83            Red fox      Vulpes  carni     Carnivora  ...    0.350000   14.2  0.05040    4.230

# A histogram of sleep_total shows the overall shape of the distribution.
msleep['sleep_total'].hist()
plt.show()

# How long do mammals in this dataset typically sleep? What's a typical
# value? Where is the center of the data? -> mean, median, mode


# =====================================================================
# 6. Measures of center: mean
# =====================================================================

# The mean is the sum of all the data points divided by the total number
# of data points.
print(np.mean(msleep['sleep_total']))  # 10.43373


# =====================================================================
# 7. Measures of center: median
# =====================================================================

# The median is the value in the middle of the sorted data.
print(msleep['sleep_total'].sort_values().iloc[41])  # 10.1

# np.median() computes the same thing directly.
print(np.median(msleep['sleep_total']))  # 10.1


# =====================================================================
# 8. Measures of center: mode
# =====================================================================

# The mode is the most frequent value(s) in the data.
print(msleep['sleep_total'].value_counts())
# 12.5    4
# 10.1    3
# 14.9    2
# ...
# Name: sleep_total, Length: 65, dtype: int64

# The mode is especially useful for categorical data.
print(msleep['vore'].value_counts())
# herbi      32
# omni       20
# carni      19
# insecti     5
# Name: vore, dtype: int64

print(statistics.mode(msleep['vore']))  # 'herbi'


# =====================================================================
# 9. How outliers affect mean vs. median
# =====================================================================

# Subset msleep to select rows where 'vore' equals 'insecti'.
print(msleep[msleep['vore'] == 'insecti'])
#                      name         genus     vore         order  sleep_total
# 22          Big brown bat     Eptesicus  insecti    Chiroptera         19.7
# 43       Little brown bat        Myotis  insecti    Chiroptera         19.9
# 62        Giant armadillo    Priodontes  insecti     Cingulata         18.1
# 67  Eastern american mole      Scalopus  insecti  Soricomorpha          8.4

# Aggregate mean and median of sleep_total for this subset.
print(msleep[msleep['vore'] == "insecti"]['sleep_total'].agg([np.mean, np.median]))
# mean      16.53
# median    18.9
# Name: sleep_total, dtype: float64

# Now add an outlier row: a "Mystery insectivore" with sleep_total = 0.0.
print(msleep[msleep['vore'] == 'insecti'])
#                      name         genus     vore         order  sleep_total
# 22          Big brown bat     Eptesicus  insecti    Chiroptera         19.7
# 43       Little brown bat        Myotis  insecti    Chiroptera         19.9
# 62        Giant armadillo    Priodontes  insecti     Cingulata         18.1
# 67  Eastern american mole      Scalopus  insecti  Soricomorpha          8.4
# 84    Mystery insectivore            ... insecti           ...          0.0

# Re-aggregating shows the outlier pulls the mean much further than the
# median: Mean: 16.5 -> 13.2, Median: 18.9 -> 18.1.
print(msleep[msleep['vore'] == "insecti"]['sleep_total'].agg([np.mean, np.median]))
# mean      13.22
# median    18.1
# Name: sleep_total, dtype: float64


# =====================================================================
# 10. Choosing mean vs. median: skew
# =====================================================================

# A histogram of the values reveals the shape (and skew) of the data.
data['values'].hist()
plt.show()

# Left-skewed data has a tail stretching to the left; right-skewed data has
# a tail stretching to the right. The mean is pulled toward the tail more
# than the median is, so:
# - Symmetrical data: mean and median are close, either works.
# - Skewed data: median is a more robust measure of center than the mean.


# =====================================================================
# 11. Measures of spread: variance
# =====================================================================

# Variance is roughly the average (squared) distance from each data point
# to the data's mean. Calculating it by hand, step by step:

# 1. Subtract the mean from each data point.
dists = msleep['sleep_total'] - np.mean(msleep['sleep_total'])
print(dists)
# 0     1.666265
# 1     6.566265
# 2     3.966265
# 3     4.466265
# 4    -6.433735
# ...

# 2. Square each distance.
sq_dists = dists ** 2
print(sq_dists)
# 0      2.776439
# 1     43.115837
# 2     15.731259
# 3     19.947524
# 4     41.392945
# ...

# 3. Sum the squared distances.
sum_sq_dists = np.sum(sq_dists)
print(sum_sq_dists)  # 1624.065542

# 4. Divide by the number of data points minus 1.
variance = sum_sq_dists / (83 - 1)
print(variance)  # 19.805677

# np.var() with ddof=1 computes the sample variance directly, matching the
# manual calculation above.
print(np.var(msleep['sleep_total'], ddof=1))  # 19.805677

# Without ddof=1, np.var() calculates the population variance instead of
# the sample variance, giving a (slightly) different result.
print(np.var(msleep['sleep_total']))  # 19.567055


# =====================================================================
# 12. Measures of spread: standard deviation
# =====================================================================

# Standard deviation is the square root of the variance.
print(np.sqrt(np.var(msleep['sleep_total'], ddof=1)))  # 4.450357

# np.std() with ddof=1 computes the same sample standard deviation directly.
print(np.std(msleep['sleep_total'], ddof=1))  # 4.450357


# =====================================================================
# 13. Mean absolute deviation
# =====================================================================

# Mean absolute deviation takes the absolute value of each distance from
# the mean, instead of squaring it.
dists = msleep['sleep_total'] - np.mean(msleep['sleep_total'])
print(np.mean(np.abs(dists)))  # 3.566701

# Standard deviation vs. mean absolute deviation:
# - Standard deviation squares distances, penalizing longer distances more
#   than shorter ones.
# - Mean absolute deviation penalizes each distance equally.
# Neither is "better" than the other, but standard deviation is more common.


# =====================================================================
# 14. Quantiles and quartiles
# =====================================================================

# A quantile splits the (sorted) data into equal-size chunks; the 0.5
# quantile is the median.
print(np.quantile(msleep['sleep_total'], 0.5))  # 10.1

# Quartiles split the data into quarters: 0, 0.25, 0.5, 0.75, 1.
print(np.quantile(msleep['sleep_total'], [0, 0.25, 0.5, 0.75, 1]))
# array([ 1.9 ,  7.85, 10.1 , 13.75, 19.9 ])

# Boxplots visualize quartiles directly: the box spans the 25th to 75th
# percentile, with a line at the median.
plt.boxplot(msleep['sleep_total'])
plt.show()


# =====================================================================
# 15. Quantiles with np.linspace()
# =====================================================================

# Quantiles don't have to be quarters — any evenly spaced set works.
print(np.quantile(msleep['sleep_total'], [0, 0.2, 0.4, 0.6, 0.8, 1]))
# array([ 1.9 ,  6.24,  9.48, 11.14, 14.4 , 19.9 ])

# np.linspace(start, stop, num) generates evenly spaced boundaries, so it
# can generate the quantile cut points instead of typing them by hand.
print(np.quantile(msleep['sleep_total'], np.linspace(0, 1, 5)))
# array([ 1.9 ,  7.85, 10.1 , 13.75, 19.9 ])


# =====================================================================
# 16. Interquartile range (IQR)
# =====================================================================

# The IQR is the distance between the 25th and 75th percentiles — it's
# the height of the box in a boxplot.
print(np.quantile(msleep['sleep_total'], 0.75) - np.quantile(msleep['sleep_total'], 0.25))  # 5.9

# scipy.stats.iqr() computes the same value directly.
print(iqr(msleep['sleep_total']))  # 5.9


# =====================================================================
# 17. Using the IQR to find outliers
# =====================================================================

# An outlier is a data point substantially different from the others. One
# common rule: a data point is an outlier if
#   data < Q1 - 1.5 * IQR   or   data > Q3 + 1.5 * IQR

# Apply the rule to bodywt.
bodywt_iqr = iqr(msleep['bodywt'])
lower_threshold = np.quantile(msleep['bodywt'], 0.25) - 1.5 * bodywt_iqr
upper_threshold = np.quantile(msleep['bodywt'], 0.75) + 1.5 * bodywt_iqr
print(msleep[(msleep['bodywt'] < lower_threshold) | (msleep['bodywt'] > upper_threshold)])
#                     name   vore  sleep_total    bodywt
# 4                    Cow  herbi          4.0   600.000
# 20        Asian elephant  herbi          3.9  2547.000
# 22                 Horse  herbi          2.9   521.000
# ...


# =====================================================================
# 18. All summary statistics at once: describe()
# =====================================================================

# describe() reports count, mean, std, min, quartiles, and max all in one
# call — a quick way to get most of the summary statistics above at once.
print(msleep['bodywt'].describe())
# count      83.000000
# mean      166.136349
# std       786.839732
# min         0.005000
# 25%         0.174000
# 50%         1.670000
# 75%        41.750000
# max      6654.000000
# Name: bodywt, dtype: float64
