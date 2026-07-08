"""
More Distributions and the Central Limit Theorem
--------------------------------------------------
The normal distribution and its "68-95-99.7" rule, using scipy.stats.norm
to answer percentage/percentile questions, the central limit theorem
(sampling distributions approach normal as sample size grows), the Poisson
distribution for counts of events over fixed time, and a quick tour of the
exponential, t, and log-normal distributions.

Table of Contents
1. What is the normal distribution?
2. Areas under the normal distribution: the 68-95-99.7 rule
3. Approximating real data with the normal distribution
4. norm.cdf(): percentages below/above/between values
5. norm.ppf(): finding a value from a percentage
6. Generating random numbers from a normal distribution
7. Sampling distributions: rolling dice and taking the mean
8. Sampling distributions of the mean, over more repeats
9. The central limit theorem
10. Standard deviation and the CLT
11. Proportions and the CLT
12. Mean of a sampling distribution
13. The Poisson distribution: lambda and pmf/cdf
14. Sampling from a Poisson distribution; the CLT still applies
15. The exponential distribution
16. The (Student's) t-distribution
17. The log-normal distribution
"""

import numpy as np
import pandas as pd

# =====================================================================
# 1. What is the normal distribution?
# =====================================================================

# The normal distribution is:
# - Symmetrical (left and right halves are mirror images)
# - Has a total area under the curve of 1 (like all probability
#   distributions)
# - The curve never actually touches 0 (its tails extend infinitely)
# - Described by its mean and standard deviation.
#   e.g. mean 20, standard deviation 3.
# - The STANDARD normal distribution has mean 0 and standard deviation 1.


# =====================================================================
# 2. Areas under the normal distribution: the 68-95-99.7 rule
# =====================================================================

# 68% of the area falls within 1 standard deviation of the mean.
# 95% of the area falls within 2 standard deviations of the mean.
# 99.7% of the area falls within 3 standard deviations of the mean.


# =====================================================================
# 3. Approximating real data with the normal distribution
# =====================================================================

# Many real-world histograms look approximately normal, e.g. women's
# heights from the NHANES survey: mean 161 cm, standard deviation 7 cm.


# =====================================================================
# 4. norm.cdf(): percentages below/above/between values
# =====================================================================

from scipy.stats import norm

# What percent of women are shorter than 154 cm?
# (16% of women in the survey are shorter than 154 cm.)
print(norm.cdf(154, 161, 7))  # 0.158655

# What percent of women are taller than 154 cm?
print(1 - norm.cdf(154, 161, 7))  # 0.841345

# What percent of women are between 154 and 157 cm?
print(norm.cdf(157, 161, 7) - norm.cdf(154, 161, 7))  # 0.1252


# =====================================================================
# 5. norm.ppf(): finding a value from a percentage
# =====================================================================

# norm.ppf() is the inverse of norm.cdf(): given a probability, it returns
# the value at that percentile.

# What height are 90% of women shorter than?
print(norm.ppf(0.9, 161, 7))  # 169.97086

# What height are 90% of women taller than?
print(norm.ppf((1 - 0.9), 161, 7))  # 152.029


# =====================================================================
# 6. Generating random numbers from a normal distribution
# =====================================================================

# Generate 10 random heights following this normal distribution.
print(norm.rvs(161, 7, size=10))
# array([155.5758223 , 155.13133235, 160.06377097, 168.33345778,
#        165.92273375, 163.32677057, 165.13280753, 146.36133538,
#        149.07845021, 160.5790856 ])


# =====================================================================
# 7. Sampling distributions: rolling dice and taking the mean
# =====================================================================

die = pd.Series([1, 2, 3, 4, 5, 6])

# Roll the die 5 times and look at the individual rolls.
samp_5 = die.sample(5, replace=True)
print(samp_5)  # array([3, 1, 4, 1, 1])
print(np.mean(samp_5))  # 2.0

# Roll 5 times and take the mean — repeating the experiment gives a
# different mean each time.
samp_5 = die.sample(5, replace=True)
print(np.mean(samp_5))  # 4.4

samp_5 = die.sample(5, replace=True)
print(np.mean(samp_5))  # 3.8


# =====================================================================
# 8. Sampling distributions of the mean, over more repeats
# =====================================================================

# Repeat 10 times: roll 5 times, take the mean, and collect the means.
sample_means = []
for i in range(10):
    samp_5 = die.sample(5, replace=True)
    sample_means.append(np.mean(samp_5))
print(sample_means)
# [3.8, 4.0, 3.8, 3.6, 3.2, 4.8, 2.6, 3.0, 2.6, 2.0]

# This collection of sample means is a "sampling distribution of the
# sample mean." Repeating with 100 and then 1000 replicates shows the
# distribution take shape more clearly as more means are collected.
sample_means = []
for i in range(100):
    sample_means.append(np.mean(die.sample(5, replace=True)))

sample_means = []
for i in range(1000):
    sample_means.append(np.mean(die.sample(5, replace=True)))


# =====================================================================
# 9. The central limit theorem
# =====================================================================

# The central limit theorem (CLT): the sampling distribution of a
# statistic becomes closer to the normal distribution as the number of
# trials increases.
# * Samples should be random and independent for the CLT to apply.


# =====================================================================
# 10. Standard deviation and the CLT
# =====================================================================

# The CLT applies to other summary statistics too, not just the mean —
# e.g. collecting the standard deviation of each sample.
sample_sds = []
for i in range(1000):
    sample_sds.append(np.std(die.sample(5, replace=True)))


# =====================================================================
# 11. Proportions and the CLT
# =====================================================================

# The CLT also applies to proportions, e.g. sampling from a categorical
# variable (which of 4 salespeople gets picked).
sales_team = pd.Series(["Amir", "Brian", "Claire", "Damian"])

print(sales_team.sample(10, replace=True))
# array(['Claire', 'Damian', 'Brian', 'Damian', 'Damian', 'Amir', 'Amir',
#        'Amir', 'Amir', 'Damian'], dtype=object)

print(sales_team.sample(10, replace=True))
# array(['Brian', 'Amir', 'Brian', 'Claire', 'Brian', 'Damian', 'Claire',
#        'Brian', 'Claire', 'Claire'], dtype=object)

# Repeatedly sampling and recording the proportion of "Claire"s each time
# builds a sampling distribution of the proportion, which also approaches
# normal as the number of repeats increases.


# =====================================================================
# 12. Mean of a sampling distribution
# =====================================================================

# The mean of a sampling distribution estimates a characteristic of the
# unknown underlying distribution, and can more easily estimate
# characteristics of large populations.

# Estimate the expected value of the die from the sampling distribution
# of sample means.
print(np.mean(sample_means))  # 3.48

# Estimate the true proportion of "Claire"s from repeated samples.
print(np.mean(sample_props))  # 0.26


# =====================================================================
# 13. The Poisson distribution: lambda and pmf/cdf
# =====================================================================

# A Poisson process: events appear to happen at a certain rate, but
# completely at random, e.g. number of animals adopted from a shelter per
# week, number of people arriving at a restaurant per hour, number of
# earthquakes in California per year.
# The time unit is irrelevant, as long as the same unit is used
# consistently for the same situation.

# The Poisson distribution describes the probability of some number of
# events occurring over a fixed period of time, e.g. probability of >= 5
# animals adopted per week, or < 20 earthquakes per year.

# lambda (the distribution's peak) = average number of events per time
# interval, e.g. average number of adoptions per week = 8.

from scipy.stats import poisson

# If the average number of adoptions per week is 8, what is
# P(# adoptions in a week = 5)?
print(poisson.pmf(5, 8))  # 0.09160366

# What is P(# adoptions in a week <= 5)?
print(poisson.cdf(5, 8))  # 0.1912361

# What is P(# adoptions in a week > 5)?
print(1 - poisson.cdf(5, 8))  # 0.8087639

# If the average is instead 10 adoptions per week, what is
# P(# adoptions in a week > 5)?
print(1 - poisson.cdf(5, 10))  # 0.932914


# =====================================================================
# 14. Sampling from a Poisson distribution; the CLT still applies
# =====================================================================

print(poisson.rvs(8, size=10))
# array([ 9,  9,  8,  7, 11,  3, 10,  6,  8, 14])

# As with the mean and proportion earlier, the central limit theorem still
# applies to the Poisson distribution: the sampling distribution of the
# sample mean of Poisson samples approaches normal as sample size grows.


# =====================================================================
# 15. The exponential distribution
# =====================================================================

# The exponential distribution describes the probability of a certain
# amount of time passing BETWEEN Poisson events, e.g. probability of > 1
# day between adoptions, < 10 minutes between restaurant arrivals, or 6-8
# months between earthquakes. It also uses lambda (rate), and is
# continuous (time-based).

# Example: on average, one customer service ticket is created every 2
# minutes -> lambda = 0.5 tickets created each minute.

# Expected value of the exponential distribution = 1 / lambda.
# In terms of rate (Poisson): lambda = 0.5 requests per minute.
# In terms of time between events (exponential): 1 / lambda = 1 / 0.5 = 2,
# i.e. 1 request per 2 minutes.

from scipy.stats import expon

# scale = 1 / lambda = 1 / 0.5 = 2

# P(wait < 1 min)
print(expon.cdf(1, scale=2))  # 0.3934693402873666

# P(wait > 4 min)
print(1 - expon.cdf(4, scale=2))  # 0.1353352832366127

# P(1 min < wait < 4 min)
print(expon.cdf(4, scale=2) - expon.cdf(1, scale=2))  # 0.4711953764760207


# =====================================================================
# 16. The (Student's) t-distribution
# =====================================================================

# The t-distribution has a similar shape to the normal distribution, but
# has an additional parameter: degrees of freedom (df), which affects the
# thickness of the tails.
# Lower df = thicker tails, higher standard deviation.
# Higher df = distribution gets closer to the normal distribution.


# =====================================================================
# 17. The log-normal distribution
# =====================================================================

# A log-normal distributed variable has a logarithm that is normally
# distributed. Examples: length of chess games, adult blood pressure,
# number of hospitalizations in the 2003 SARS outbreak.
