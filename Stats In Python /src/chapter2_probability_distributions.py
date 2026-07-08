"""
Random Numbers and Probability
-------------------------------
How to measure the chance of an event, how sampling with vs. without
replacement changes independence between picks, and how to describe,
visualize, and sample from discrete (uniform, binomial) and continuous
(uniform) probability distributions using pandas, NumPy, and SciPy.

Table of Contents
1. Measuring chance: P(event)
2. Sampling from a DataFrame
3. Setting a random seed for reproducibility
4. Sampling twice: without replacement
5. Sampling with replacement
6. Independent vs. dependent events
7. Probability distributions and expected value
8. Probability as area under the distribution
9. Discrete uniform distribution: sampling and visualizing
10. Sample distribution vs. theoretical distribution
11. Law of large numbers
12. Continuous uniform distribution
13. Uniform distribution in Python: cdf()
14. Generating random numbers from a uniform distribution
15. The binomial distribution: single/many flips
16. Binomial distribution: parameters n and p
17. Binomial distribution: pmf() and cdf()
18. Expected value and independence
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================================
# 1. Measuring chance: P(event)
# =====================================================================

# P(event) = (# ways event can happen) / (total # of possible outcomes)

# Example: a coin flip. P(heads) = 1 / 2 = 50%.

# Example: assigning one of 4 salespeople (Amir, Brian, Claire, Damian) to
# a meeting at random. P(Brian) = 1 / 4 = 25%.


# =====================================================================
# 2. Sampling from a DataFrame
# =====================================================================

print(sales_counts)
#      name  n_sales
# 0    Amir      178
# 1   Brian      128
# 2  Claire       75
# 3  Damian       69

# .sample() picks one row at random each time it's called.
print(sales_counts.sample())
#     name  n_sales
# 1  Brian      128

print(sales_counts.sample())
#     name  n_sales
# 2  Claire      75


# =====================================================================
# 3. Setting a random seed for reproducibility
# =====================================================================

# np.random.seed() fixes the random number generator's starting point, so
# the "random" pick becomes reproducible: calling sample() again after
# re-seeding with the same value reproduces the same result.
np.random.seed(10)
print(sales_counts.sample())
#     name  n_sales
# 1  Brian      128

np.random.seed(10)
print(sales_counts.sample())
#     name  n_sales
# 1  Brian      128

np.random.seed(10)
print(sales_counts.sample())
#     name  n_sales
# 1  Brian      128


# =====================================================================
# 4. Sampling twice: without replacement
# =====================================================================

# By default, sample() samples without replacement: once a row is picked,
# it can't be picked again in the same call.
# "A second meeting": P(Claire) = 1 / 3 = 33% (Brian already picked).
print(sales_counts.sample(2))
#      name  n_sales
# 1   Brian      128
# 2  Claire       75


# =====================================================================
# 5. Sampling with replacement
# =====================================================================

# With replace=True, each pick is put back before the next pick, so the
# same row can be picked more than once.
# "Sampling with replacement": P(Claire) = 1 / 4 = 25% every time.
print(sales_counts.sample(5, replace=True))
#      name  n_sales
# 1   Brian      128
# 2  Claire       75
# 1   Brian      128
# 3  Damian       69
# 0    Amir      178


# =====================================================================
# 6. Independent vs. dependent events
# =====================================================================

# Two events are independent if the probability of the second event isn't
# affected by the outcome of the first event.
# Sampling with replacement -> each pick is independent.

# Two events are dependent if the probability of the second event IS
# affected by the outcome of the first event.
# Sampling without replacement -> picks become dependent.


# =====================================================================
# 7. Probability distributions and expected value
# =====================================================================

# A probability distribution describes the probability of each possible
# outcome in a scenario.
# The expected value is the mean of a probability distribution.

# Expected value of a fair die roll:
# (1 * 1/6) + (2 * 1/6) + (3 * 1/6) + (4 * 1/6) + (5 * 1/6) + (6 * 1/6) = 3.5

# Expected value of an uneven die roll (where rolling a 2 is impossible):
# (1 * 1/6) + (2 * 0) + (3 * 1/3) + (4 * 1/6) + (5 * 1/6) + (6 * 1/6) = 3.67


# =====================================================================
# 8. Probability as area under the distribution
# =====================================================================

# For a fair die, P(die roll <= 2) = 1/3 (2 of 6 equally likely outcomes).
# For the uneven die above, P(uneven die roll <= 2) = 1/6 (rolling a 2 is
# impossible, so only the "1" outcome, with probability 1/6, counts).


# =====================================================================
# 9. Discrete uniform distribution: sampling and visualizing
# =====================================================================

# Discrete probability distributions describe probabilities for discrete
# outcomes. A fair die is a discrete UNIFORM distribution (every outcome
# equally likely); an uneven die is not.
print(die)
#   number      prob
# 0      1  0.166667
# 1      2  0.166667
# 2      3  0.166667
# 3      4  0.166667
# 4      5  0.166667
# 5      6  0.166667

print(np.mean(die['number']))  # 3.5

# Sample 10 rolls from the die, with replacement (a die roll is always
# "with replacement" — every roll has the same possible outcomes).
rolls_10 = die.sample(10, replace=True)
print(rolls_10)
#   number      prob
# 0      1  0.166667
# 0      1  0.166667
# 4      5  0.166667
# 1      2  0.166667
# 0      1  0.166667
# 0      1  0.166667
# 5      6  0.166667
# 5      6  0.166667
# ...

# Visualize the sample as a histogram, with one bin per possible outcome.
rolls_10['number'].hist(bins=np.linspace(1, 7, 7))
plt.show()


# =====================================================================
# 10. Sample distribution vs. theoretical distribution
# =====================================================================

# A sample's mean approximates, but doesn't exactly match, the theoretical
# distribution's expected value — and the approximation improves with a
# bigger sample.

# Sample of 10 rolls:
print(np.mean(rolls_10['number']))  # 3.0
# Theoretical probability distribution mean:
print(np.mean(die['number']))  # 3.5

# Sample of 100 rolls:
rolls_100 = die.sample(100, replace=True)
print(np.mean(rolls_100['number']))  # 3.4

# Sample of 1000 rolls:
rolls_1000 = die.sample(1000, replace=True)
print(np.mean(rolls_1000['number']))  # 3.48


# =====================================================================
# 11. Law of large numbers
# =====================================================================

# As the size of a sample increases, the sample mean approaches the
# expected value:
#   Sample size    Mean
#          10      3.00
#         100      3.40
#        1000      3.48


# =====================================================================
# 12. Continuous uniform distribution
# =====================================================================

# Continuous distributions describe probabilities over a continuous range
# rather than discrete outcomes.
# Example: waiting for a bus that arrives uniformly at random somewhere
# between 0 and 12 minutes -> a continuous uniform distribution.

# Probability is still represented as area under the distribution.
# P(4 <= wait time <= 7) = 3 * 1/12 = 3/12


# =====================================================================
# 13. Uniform distribution in Python: cdf()
# =====================================================================

from scipy.stats import uniform

# P(wait time <= 7), for a uniform distribution from 0 to 12.
print(uniform.cdf(7, 0, 12))  # 0.5833333

# "Greater than" probabilities: P(wait time >= 7) = 1 - P(wait time <= 7).
print(1 - uniform.cdf(7, 0, 12))  # 0.4166667

# P(4 <= wait time <= 7) = P(wait time <= 7) - P(wait time <= 4).
print(uniform.cdf(7, 0, 12) - uniform.cdf(4, 0, 12))  # 0.25

# Total area under any probability distribution always sums to 1.
# P(0 <= wait time <= 12) = 12 * 1/12 = 1


# =====================================================================
# 14. Generating random numbers from a uniform distribution
# =====================================================================

# uniform.rvs(low, high, size) generates random numbers following a
# uniform distribution between low and high.
print(uniform.rvs(0, 5, size=10))
# array([1.89740094, 4.70673196, 0.33224683, 1.0137103 , 2.31641255,
#        3.49969897, 0.29688598, 0.92057234, 4.71086658, 1.56815855])

# Other continuous distributions have other characteristic shapes, e.g.
# the normal distribution and the exponential distribution (covered later).


# =====================================================================
# 15. The binomial distribution: single/many flips
# =====================================================================

from scipy.stats import binom

# binom.rvs(# of coins, probability of heads/success, size=# of trials)
# 1 = head/success, 0 = tails/failure.

# A single flip of a fair coin.
print(binom.rvs(1, 0.5, size=1))  # array([1])

# One flip, repeated many times.
print(binom.rvs(1, 0.5, size=8))  # array([0, 1, 1, 0, 1, 0, 1, 1])

# Many flips (of the same coin), one trial: total number of heads.
print(binom.rvs(8, 0.5, size=1))  # array([5])

# Many flips, many trials.
print(binom.rvs(3, 0.5, size=10))  # array([0, 3, 2, 1, 3, 0, 2, 2, 0, 0])

# A different (unfair) probability of success.
print(binom.rvs(3, 0.25, size=10))  # array([1, 1, 1, 1, 0, 0, 2, 0, 1, 0])


# =====================================================================
# 16. Binomial distribution: parameters n and p
# =====================================================================

# The binomial distribution describes the probability of some number of
# successes in a sequence of independent trials, e.g. the number of heads
# in a sequence of coin flips. It's described by:
#   n: total number of trials
#   p: probability of success
print(binom.rvs(n=10, p=0.5, size=20))


# =====================================================================
# 17. Binomial distribution: pmf() and cdf()
# =====================================================================

# What's the probability of exactly 7 heads out of 10 flips?
# binom.pmf(num heads, num trials, prob of heads)
print(binom.pmf(7, 10, 0.5))  # 0.1171875

# What's the probability of 7 or fewer heads?
print(binom.cdf(7, 10, 0.5))  # 0.9453125

# What's the probability of more than 7 heads?
print(1 - binom.cdf(7, 10, 0.5))  # 0.0546875


# =====================================================================
# 18. Expected value and independence
# =====================================================================

# Expected value of a binomial distribution = n * p.
# Expected number of heads out of 10 flips = 10 * 0.5 = 5

# The binomial distribution describes a sequence of INDEPENDENT trials —
# if the probability of the second trial is altered by the outcome of the
# first (e.g. sampling without replacement), the binomial distribution
# does not apply.
