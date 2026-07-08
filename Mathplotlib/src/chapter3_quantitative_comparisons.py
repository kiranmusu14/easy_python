"""
Quantitative Comparisons and Statistical Visualizations
--------------------------------------------------------
Four ways to compare quantities with Matplotlib: bar charts (including
stacked bars with a legend), histograms (with custom bins and an outline
style for overlapping groups), statistical summaries via error bars and
boxplots, and scatter plots (including encoding a third variable with
color).

Table of Contents
1. Olympic medals data
2. A simple bar chart
3. Rotating the tick labels
4. Stacking a second bar series
5. Stacking all three medal types
6. Adding a legend to a stacked bar chart
7. Comparing two groups with a bar chart of means
8. Introducing histograms
9. Adding labels and a legend to histograms
10. Setting the number of bins
11. Setting custom bin boundaries
12. Using histtype="step" for overlapping histograms
13. Adding error bars to a bar chart
14. Adding error bars to a line plot
15. Adding boxplots
16. Introducing scatter plots
17. Customizing scatter plots by group color
18. Encoding a third variable by color
"""

# =====================================================================
# 1. Olympic medals data
# =====================================================================

# medals_by_country_2016.csv has one row per country and Gold/Silver/
# Bronze medal counts as columns:
#   ,Gold, Silver, Bronze
#   United States, 137, 52, 67
#   Germany, 47, 43, 67
#   Great Britain, 64, 55, 26
#   Russia, 50, 28, 35
#   China, 44, 30, 35
#   France, 20, 55, 21
#   Australia, 23, 34, 25
#   Italy, 8, 38, 24
#   Canada, 4, 4, 61
#   Japan, 17, 13, 34
import pandas as pd
import matplotlib.pyplot as plt

medals = pd.read_csv('medals_by_country_2016.csv', index_col=0)


# =====================================================================
# 2. A simple bar chart
# =====================================================================

# ax.bar(x, height) draws one bar per country, using the row labels
# (country names) as the index.
fig, ax = plt.subplots()
ax.bar(medals.index, medals["Gold"])
plt.show()


# =====================================================================
# 3. Rotating the tick labels
# =====================================================================

# Long country names overlap on the x-axis unless rotated.
fig, ax = plt.subplots()
ax.bar(medals.index, medals["Gold"])
ax.set_xticklabels(medals.index, rotation=90)
ax.set_ylabel("Number of medals")
plt.show()


# =====================================================================
# 4. Stacking a second bar series
# =====================================================================

# bottom= stacks a second bar series on top of the first instead of
# overlapping it.
fig, ax = plt.subplots()
ax.bar(medals.index, medals["Gold"])
ax.bar(medals.index, medals["Silver"], bottom=medals["Gold"])
ax.set_xticklabels(medals.index, rotation=90)
ax.set_ylabel("Number of medals")
plt.show()


# =====================================================================
# 5. Stacking all three medal types
# =====================================================================

# Bronze stacks on top of Gold + Silver combined.
fig, ax = plt.subplots()
ax.bar(medals.index, medals["Gold"])
ax.bar(medals.index, medals["Silver"], bottom=medals["Gold"])
ax.bar(medals.index, medals["Bronze"],
       bottom=medals["Gold"] + medals["Silver"])
ax.set_xticklabels(medals.index, rotation=90)
ax.set_ylabel("Number of medals")
plt.show()


# =====================================================================
# 6. Adding a legend to a stacked bar chart
# =====================================================================

# label= on each bar series, plus ax.legend(), identifies which stacked
# segment is which medal type.
fig, ax = plt.subplots()
ax.bar(medals.index, medals["Gold"], label="Gold")
ax.bar(medals.index, medals["Silver"], bottom=medals["Gold"],
       label="Silver")
ax.bar(medals.index, medals["Bronze"],
       bottom=medals["Gold"] + medals["Silver"],
       label="Bronze")

ax.set_xticklabels(medals.index, rotation=90)
ax.set_ylabel("Number of medals")

ax.legend()
plt.show()


# =====================================================================
# 7. Comparing two groups with a bar chart of means
# =====================================================================

# NOTE: mens_rowing and mens_gymnastics are pandas DataFrames assumed
# already loaded, each with a "Height" column of athlete heights (cm).

# A bar chart can also compare a single summary statistic (here, the
# mean height) between two groups.
fig, ax = plt.subplots()
ax.bar("Rowing", mens_rowing["Height"].mean())
ax.bar("Gymnastics", mens_gymnastics["Height"].mean())
ax.set_ylabel("Height (cm)")
plt.show()


# =====================================================================
# 8. Introducing histograms
# =====================================================================

# ax.hist() shows the full distribution of a variable, not just its
# mean — here the two groups' height distributions overlap on one axes.
fig, ax = plt.subplots()
ax.hist(mens_rowing["Height"])
ax.hist(mens_gymnastics["Height"])
ax.set_xlabel("Height (cm)")
ax.set_ylabel("# of observations")
plt.show()


# =====================================================================
# 9. Adding labels and a legend to histograms
# =====================================================================

# Without label= + legend(), it's impossible to tell which histogram
# belongs to which group.
fig, ax = plt.subplots()
ax.hist(mens_rowing["Height"], label="Rowing")
ax.hist(mens_gymnastics["Height"], label="Gymnastics")
ax.set_xlabel("Height (cm)")
ax.set_ylabel("# of observations")

ax.legend()
plt.show()


# =====================================================================
# 10. Setting the number of bins
# =====================================================================

# bins= controls how many bars the range is divided into.
fig, ax = plt.subplots()
ax.hist(mens_rowing["Height"], label="Rowing", bins=5)
ax.hist(mens_gymnastics["Height"], label="Gymnastics", bins=5)
ax.set_xlabel("Height (cm)")
ax.set_ylabel("# of observations")
ax.legend()
plt.show()


# =====================================================================
# 11. Setting custom bin boundaries
# =====================================================================

# bins= can also take an explicit list of boundary edges instead of a
# count, so both histograms use identical, directly comparable bins.
fig, ax = plt.subplots()
ax.hist(mens_rowing["Height"], label="Rowing",
        bins=[150, 160, 170, 180, 190, 200, 210])

ax.hist(mens_gymnastics["Height"], label="Gymnastics",
        bins=[150, 160, 170, 180, 190, 200, 210])

ax.set_xlabel("Height (cm)")
ax.set_ylabel("# of observations")
ax.legend()
plt.show()


# =====================================================================
# 12. Using histtype="step" for overlapping histograms
# =====================================================================

# histtype="step" draws only the outline of each histogram instead of a
# filled bar, so overlapping distributions stay readable.
fig, ax = plt.subplots()
ax.hist(mens_rowing["Height"], label="Rowing",
        bins=[150, 160, 170, 180, 190, 200, 210],
        histtype="step")

ax.hist(mens_gymnastics["Height"], label="Gymnastics",
        bins=[150, 160, 170, 180, 190, 200, 210],
        histtype="step")

ax.set_xlabel("Height (cm)")
ax.set_ylabel("# of observations")
ax.legend()
plt.show()


# =====================================================================
# 13. Adding error bars to a bar chart
# =====================================================================

# yerr= adds a vertical error bar (here, one standard deviation) on top
# of each bar's mean.
fig, ax = plt.subplots()

ax.bar("Rowing",
       mens_rowing["Height"].mean(),
       yerr=mens_rowing["Height"].std())

ax.bar("Gymnastics",
       mens_gymnastics["Height"].mean(),
       yerr=mens_gymnastics["Height"].std())

ax.set_ylabel("Height (cm)")

plt.show()


# =====================================================================
# 14. Adding error bars to a line plot
# =====================================================================

# NOTE: seattle_weather and austin_weather are the same monthly climate
# DataFrames used in earlier chapters; MLY-TAVG-STDDEV holds the
# standard deviation of the monthly average temperature.

# ax.errorbar() draws a line plot with a shaded/whiskered error region
# at each point, instead of a plain line.
fig, ax = plt.subplots()

ax.errorbar(seattle_weather["MONTH"],
            seattle_weather["MLY-TAVG-NORMAL"],
            yerr=seattle_weather["MLY-TAVG-STDDEV"])

ax.errorbar(austin_weather["MONTH"],
            austin_weather["MLY-TAVG-NORMAL"],
            yerr=austin_weather["MLY-TAVG-STDDEV"])

ax.set_ylabel("Temperature (Fahrenheit)")

plt.show()


# =====================================================================
# 15. Adding boxplots
# =====================================================================

# ax.boxplot() takes a list of Series/arrays, one box per group, and
# summarizes each group's distribution (median, quartiles, outliers) at
# a glance.
fig, ax = plt.subplots()
ax.boxplot([mens_rowing["Height"],
            mens_gymnastics["Height"]])
ax.set_xticklabels(["Rowing", "Gymnastics"])
ax.set_ylabel("Height (cm)")
plt.show()


# =====================================================================
# 16. Introducing scatter plots
# =====================================================================

# NOTE: climate_change is the same DatetimeIndex-ed DataFrame from the
# time-series chapter, with "co2" and "relative_temp" columns.

# ax.scatter(x, y) plots one point per row, useful for spotting a
# relationship between two variables.
fig, ax = plt.subplots()
ax.scatter(climate_change["co2"], climate_change["relative_temp"])
ax.set_xlabel("CO2 (ppm)")
ax.set_ylabel("Relative temperature (Celsius)")
plt.show()


# =====================================================================
# 17. Customizing scatter plots by group color
# =====================================================================

# Slicing by decade and giving each slice its own color + label turns
# the single scatter plot into a group comparison.
eighties = climate_change["1980-01-01":"1989-12-31"]
nineties = climate_change["1990-01-01":"1999-12-31"]
fig, ax = plt.subplots()
ax.scatter(eighties["co2"], eighties["relative_temp"],
           color="red", label="eighties")

ax.scatter(nineties["co2"], nineties["relative_temp"],
           color="blue", label="nineties")

ax.legend()

ax.set_xlabel("CO2 (ppm)")
ax.set_ylabel("Relative temperature (Celsius)")

plt.show()


# =====================================================================
# 18. Encoding a third variable by color
# =====================================================================

# c= colors each point by a third variable's value — here, time itself
# — so the passage of time shows up as a color gradient across points.
fig, ax = plt.subplots()
ax.scatter(climate_change["co2"], climate_change["relative_temp"],
           c=climate_change.index)

ax.set_xlabel("CO2 (ppm)")
ax.set_ylabel("Relative temperature (Celsius)")
plt.show()
