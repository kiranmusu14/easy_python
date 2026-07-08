"""
Plotting Time-Series Data
-------------------------
Time-series data as a DataFrame indexed by a DatetimeIndex: reading it in
with pd.read_csv(parse_dates=..., index_col=...), slicing it by date
range, plotting it, and layering a second variable on a shared or twinned
axes. Ends with annotating a specific point on the plot with text and an
arrow.

Table of Contents
1. Climate change time-series data
2. Working with a DatetimeIndex
3. Plotting time-series data
4. Zooming in with slicing on a DatetimeIndex
5. Reading the CSV with parse_dates and index_col
6. Plotting two time-series on the same axes
7. Using twin axes for a second scale
8. Separating variables by color
9. Coloring the ticks to match
10. A reusable function for plotting a time series
11. Using the plotting function with twin axes
12. Annotating a point on the plot
13. Positioning the annotation text
14. Adding an arrow to an annotation
15. Customizing arrow properties
"""

# =====================================================================
# 1. Climate change time-series data
# =====================================================================

# climate_change.csv holds one row per month, with columns date, co2 and
# relative_temp:
#   date,co2,relative_temp
#   1958-03-06,315.71,0.1
#   1958-04-06,317.45,0.01
#   1958-05-06,317.5,0.08
#   1958-06-06,-99.99,-0.05
#   1958-07-06,315.86,0.06
#   1958-08-06,314.93,-0.06
#   ...
#   2016-11-06,403.55,0.93
#   2016-12-06,404.45,0.81


# =====================================================================
# 2. Working with a DatetimeIndex
# =====================================================================

# NOTE: climate_change is a pandas DataFrame assumed already loaded, with
# its "date" column set as a DatetimeIndex.

# The index is a DatetimeIndex, not plain integers or strings.
print(climate_change.index)
# DatetimeIndex(['1958-03-06', '1958-04-06', '1958-05-06', '1958-06-06',
#                '1958-07-06', '1958-08-06', '1958-09-06', '1958-10-06',
#                '1958-11-06', '1958-12-06',
#                ...
#                '2016-03-06', '2016-04-06', '2016-05-06', '2016-06-06',
#                '2016-07-06', '2016-08-06', '2016-09-06', '2016-10-06',
#                '2016-11-06', '2016-12-06'],
#               dtype='datetime64[ns]', name='date', length=706, freq=None)

print(climate_change['relative_temp'])
# 0      0.10
# 1      0.01
# 2      0.08
# 3     -0.05
# 4      0.06
# 5     -0.06
# 6     -0.03
# 7      0.04
#       ...
# 701    0.98
# 702    0.87
# 703    0.89
# 704    0.93
# 705    0.81
# Name: co2, Length: 706, dtype: float64

print(climate_change['co2'])
# 0      315.71
# 1      317.45
# 2      317.50
# 3         NaN
# 4      315.86
# 5      314.93
# 6      313.20
# 7         NaN
#       ...
# 701    402.27
# 702    401.05
# 703    401.59
# 704    403.55
# 705    404.45
# Name: co2, Length: 706, dtype: float64


# =====================================================================
# 3. Plotting time-series data
# =====================================================================

# ax.plot(index, column) plots the DatetimeIndex on the x-axis.
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(climate_change.index, climate_change['co2'])
ax.set_xlabel('Time')
ax.set_ylabel('CO2 (ppm)')
plt.show()


# =====================================================================
# 4. Zooming in with slicing on a DatetimeIndex
# =====================================================================

# A DatetimeIndex can be sliced with "start":"end" date strings, just
# like a regular list slice, to zoom in on a range of time.
sixties = climate_change["1960-01-01":"1969-12-31"]
fig, ax = plt.subplots()
ax.plot(sixties.index, sixties['co2'])
ax.set_xlabel('Time')
ax.set_ylabel('CO2 (ppm)')
plt.show()

# Slicing down to a single year zooms in further still.
sixty_nine = climate_change["1969-01-01":"1969-12-31"]
fig, ax = plt.subplots()
ax.plot(sixty_nine.index, sixty_nine['co2'])
ax.set_xlabel('Time')
ax.set_ylabel('CO2 (ppm)')
plt.show()


# =====================================================================
# 5. Reading the CSV with parse_dates and index_col
# =====================================================================

# parse_dates converts the "date" column to datetime objects, and
# index_col sets it as the DataFrame's index in one step.
import pandas as pd

climate_change = pd.read_csv('climate_change.csv',
                              parse_dates=["date"],
                              index_col="date")
print(climate_change)
#               co2  relative_temp
# date
# 1958-03-06  315.71           0.10
# 1958-04-06  317.45           0.01
# 1958-07-06  315.86           0.06
# ...            ...            ...
# 2016-11-06  403.55           0.93
# 2016-12-06  404.45           0.81
#
# [706 rows x 2 columns]


# =====================================================================
# 6. Plotting two time-series on the same axes
# =====================================================================

# Two calls to ax.plot() draw co2 and relative_temp on the same y-scale
# — but the two variables have very different ranges, so this is hard
# to read.
fig, ax = plt.subplots()
ax.plot(climate_change.index, climate_change["co2"])
ax.plot(climate_change.index, climate_change["relative_temp"])
ax.set_xlabel('Time')
ax.set_ylabel('CO2 (ppm) / Relative temperature')
plt.show()


# =====================================================================
# 7. Using twin axes for a second scale
# =====================================================================

# ax.twinx() creates a second Axes sharing the same x-axis but with its
# own, independent y-axis — one scale per variable.
fig, ax = plt.subplots()
ax.plot(climate_change.index, climate_change["co2"])
ax.set_xlabel('Time')
ax.set_ylabel('CO2 (ppm)')

ax2 = ax.twinx()
ax2.plot(climate_change.index, climate_change["relative_temp"])
ax2.set_ylabel('Relative temperature (Celsius)')
plt.show()


# =====================================================================
# 8. Separating variables by color
# =====================================================================

# Coloring each line and its matching y-axis label makes it clear which
# axis belongs to which variable.
fig, ax = plt.subplots()
ax.plot(climate_change.index, climate_change["co2"], color='blue')
ax.set_xlabel('Time')
ax.set_ylabel('CO2 (ppm)', color='blue')

ax2 = ax.twinx()
ax2.plot(climate_change.index, climate_change["relative_temp"],
         color='red')
ax2.set_ylabel('Relative temperature (Celsius)', color='red')
plt.show()


# =====================================================================
# 9. Coloring the ticks to match
# =====================================================================

# tick_params('y', colors=...) colors the tick marks/labels on one axis
# to match its line, for an even clearer visual link.
fig, ax = plt.subplots()
ax.plot(climate_change.index, climate_change["co2"],
        color='blue')
ax.set_xlabel('Time')
ax.set_ylabel('CO2 (ppm)', color='blue')
ax.tick_params('y', colors='blue')

ax2 = ax.twinx()
ax2.plot(climate_change.index,
         climate_change["relative_temp"],
         color='red')
ax2.set_ylabel('Relative temperature (Celsius)', color='red')
ax2.tick_params('y', colors='red')
plt.show()


# =====================================================================
# 10. A reusable function for plotting a time series
# =====================================================================

# Wrapping the repeated plot/xlabel/ylabel/tick_params calls in a
# function avoids retyping them for every variable.
def plot_timeseries(axes, x, y, color, xlabel, ylabel):
    axes.plot(x, y, color=color)
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel, color=color)
    axes.tick_params('y', colors=color)


# =====================================================================
# 11. Using the plotting function with twin axes
# =====================================================================

fig, ax = plt.subplots()
plot_timeseries(ax, climate_change.index, climate_change['co2'],
                 'blue', 'Time', 'CO2 (ppm)')

ax2 = ax.twinx()
plot_timeseries(ax2, climate_change.index,
                 climate_change['relative_temp'],
                 'red', 'Time', 'Relative temperature (Celsius)')
plt.show()


# =====================================================================
# 12. Annotating a point on the plot
# =====================================================================

# ax.annotate(text, xy=(x, y)) places text at a specific data
# coordinate — here, marking where the relative temperature first
# crosses 1 degree.
fig, ax = plt.subplots()
plot_timeseries(ax, climate_change.index, climate_change['co2'],
                 'blue', 'Time', 'CO2 (ppm)')

ax2 = ax.twinx()
plot_timeseries(ax2, climate_change.index,
                 climate_change['relative_temp'],
                 'red', 'Time', 'Relative temperature (Celsius)')

ax2.annotate(">1 degree", xy=(pd.Timestamp("2015-10-06"), 1))
plt.show()


# =====================================================================
# 13. Positioning the annotation text
# =====================================================================

# xytext=(x, y) places the text label away from xy, so it doesn't
# overlap the data point it's pointing at.
ax2.annotate(">1 degree",
             xy=(pd.Timestamp('2015-10-06'), 1),
             xytext=(pd.Timestamp('2008-10-06'), -0.2))


# =====================================================================
# 14. Adding an arrow to an annotation
# =====================================================================

# Passing arrowprops (even as an empty dict) draws a default arrow from
# the text back to the xy point.
ax2.annotate(">1 degree",
             xy=(pd.Timestamp('2015-10-06'), 1),
             xytext=(pd.Timestamp('2008-10-06'), -0.2),
             arrowprops={})


# =====================================================================
# 15. Customizing arrow properties
# =====================================================================

# arrowprops accepts a dict of keys like "arrowstyle" and "color" to
# control how the arrow looks. Full reference:
# https://matplotlib.org/users/annotations.html
ax2.annotate(">1 degree",
             xy=(pd.Timestamp('2015-10-06'), 1),
             xytext=(pd.Timestamp('2008-10-06'), -0.2),
             arrowprops={"arrowstyle": "->", "color": "gray"})
