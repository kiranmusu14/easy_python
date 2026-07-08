"""
Basic Plots with Matplotlib
---------------------------
The pyplot interface as the way to build a figure step by step: creating a
figure and its axes, adding one or more data series with ax.plot(), and
customizing marker, linestyle, color, axis labels and title. Finishes with
small multiples via plt.subplots(nrows, ncols) as the alternative to
cramming too many lines onto a single axes.

Table of Contents
1. The pyplot interface: fig, ax, and plt.show()
2. Adding data to the axes with ax.plot()
3. Plotting two lines on the same axes
4. Customizing data appearance
5. Adding markers
6. Choosing a different marker
7. Setting the linestyle
8. Eliminating lines with linestyle="None"
9. Choosing a line color
10. Customizing the axis labels
11. Adding a title
12. Small multiples: too much data on one axes
13. Creating small multiples with plt.subplots()
14. Adding data to individual subplots
15. Subplots with more than one line each
16. Sharing the y-axis range across subplots
"""

# NOTE: seattle_weather and austin_weather are pandas DataFrames of monthly
# climate normals, assumed already loaded (as in the DataCamp workspace),
# with columns including "MONTH", "MLY-TAVG-NORMAL", "MLY-PRCP-NORMAL",
# "MLY-PRCP-25PCTL" and "MLY-PRCP-75PCTL".

# =====================================================================
# 1. The pyplot interface: fig, ax, and plt.show()
# =====================================================================

# fig is the whole figure/canvas, ax is a single set of axes to plot on.
# plt.show() displays whatever has been drawn onto ax so far.
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
plt.show()


# =====================================================================
# 2. Adding data to the axes with ax.plot()
# =====================================================================

# seattle_weather["MONTH"] holds the month abbreviations, and
# seattle_weather["MLY-TAVG-NORMAL"] holds the matching average
# temperatures — both indexed 1 through 12.
print(seattle_weather["MONTH"])
# 1     Jan
# 2     Feb
# 3     Mar
# 4     Apr
# 5     May
# 6     Jun
# 7     Jul
# 8     Aug
# 9     Sep
# 10    Oct
# 11    Nov
# 12    Dec
# Name: MONTH, dtype: object

print(seattle_weather["MLY-TAVG-NORMAL"])
# 1     42.1
# 2     43.4
# 3     46.6
# 4     50.5
# 5     56.0
# 6     61.0
# 7     65.9
# 8     66.5
# 9     61.6
# 10    53.3
# 11    46.2
# 12    41.1
# Name: MLY-TAVG-NORMAL, dtype: float64

# ax.plot(x, y) draws x against y as a line on the axes.
fig, ax = plt.subplots()
ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-TAVG-NORMAL"])
plt.show()


# =====================================================================
# 3. Plotting two lines on the same axes
# =====================================================================

# Calling ax.plot() a second time on the same ax adds a second line to
# the same axes rather than replacing the first one.
fig, ax = plt.subplots()
ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-TAVG-NORMAL"])
ax.plot(austin_weather["MONTH"], austin_weather["MLY-TAVG-NORMAL"])
plt.show()


# =====================================================================
# 4. Customizing data appearance
# =====================================================================

# Switch to plotting the precipitation normals instead of temperature —
# same pyplot interface, different column.
fig, ax = plt.subplots()
ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-PRCP-NORMAL"])
plt.show()


# =====================================================================
# 5. Adding markers
# =====================================================================

# marker="o" draws a small circle at every data point in addition to
# the connecting line.
fig, ax = plt.subplots()
ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-PRCP-NORMAL"],
        marker="o")
plt.show()


# =====================================================================
# 6. Choosing a different marker
# =====================================================================

# Matplotlib supports many marker shapes; see the marker reference at
# https://matplotlib.org/api/markers_api.html
fig, ax = plt.subplots()
ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-PRCP-NORMAL"],
        marker="v")
plt.show()


# =====================================================================
# 7. Setting the linestyle
# =====================================================================

# linestyle="--" switches the connecting line to dashed.
fig, ax = plt.subplots()
ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-TAVG-NORMAL"],
        marker="v", linestyle="--")
plt.show()


# =====================================================================
# 8. Eliminating lines with linestyle="None"
# =====================================================================

# linestyle="None" removes the connecting line entirely, leaving only
# the markers — useful when only individual data points matter.
fig, ax = plt.subplots()
ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-TAVG-NORMAL"],
        marker="v", linestyle="None")
plt.show()


# =====================================================================
# 9. Choosing a line color
# =====================================================================

# color= controls the color of the marker and the line together.
fig, ax = plt.subplots()
ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-TAVG-NORMAL"],
        marker="v", linestyle="--", color="r")
plt.show()


# =====================================================================
# 10. Customizing the axis labels
# =====================================================================

# set_xlabel()/set_ylabel() label what each axis represents.
ax.set_xlabel("Time (months)")
ax.set_ylabel("Average temperature (Fahrenheit degrees)")
plt.show()


# =====================================================================
# 11. Adding a title
# =====================================================================

# set_title() labels the whole axes.
ax.set_title("Weather in Seattle")
plt.show()


# =====================================================================
# 12. Small multiples: too much data on one axes
# =====================================================================

# Plotting Seattle's precipitation normal together with its 25th/75th
# percentile bands, in blue.
fig, ax = plt.subplots()
ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-PRCP-NORMAL"],
        color='b')
ax.set_xlabel("Time (months)")
ax.set_ylabel("Precipitation (inches)")
plt.show()

ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-PRCP-25PCTL"],
        linestyle='--', color='b')
ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-PRCP-75PCTL"],
        linestyle='--', color='b')
plt.show()

# Adding Austin's precipitation normal and percentile bands on top, in
# red, makes the same axes hold six lines at once — hard to read.
ax.plot(austin_weather["MONTH"], austin_weather["MLY-PRCP-NORMAL"],
        color='r')
ax.plot(austin_weather["MONTH"], austin_weather["MLY-PRCP-25PCTL"],
        linestyle='--', color='r')
ax.plot(austin_weather["MONTH"], austin_weather["MLY-PRCP-75PCTL"],
        linestyle='--', color='r')
plt.show()
# Too much data on one axes! -> use small multiples (separate axes per
# city) instead of continuing to overload a single axes.


# =====================================================================
# 13. Creating small multiples with plt.subplots()
# =====================================================================

# plt.subplots(nrows, ncols) creates a grid of Axes objects on one figure.
fig, ax = plt.subplots(3, 2)
plt.show()

# ax is now a 2D NumPy array of Axes, with one entry per grid cell.
print(ax.shape)  # (3, 2)


# =====================================================================
# 14. Adding data to individual subplots
# =====================================================================

# Index into the ax array to plot on one specific subplot.
fig, ax = plt.subplots(3, 2)
ax[0, 0].plot(seattle_weather["MONTH"], seattle_weather["MLY-PRCP-NORMAL"],
              color='b')
plt.show()


# =====================================================================
# 15. Subplots with more than one line each
# =====================================================================

# A 2x1 grid: Seattle's precipitation (+ bands) on top, Austin's on the
# bottom, each subplot getting its own three ax[...].plot() calls.
fig, ax = plt.subplots(2, 1)
ax[0].plot(seattle_weather["MONTH"], seattle_weather["MLY-PRCP-NORMAL"],
           color='b')
ax[0].plot(seattle_weather["MONTH"], seattle_weather["MLY-PRCP-25PCTL"],
           linestyle='--', color='b')
ax[0].plot(seattle_weather["MONTH"], seattle_weather["MLY-PRCP-75PCTL"],
           linestyle='--', color='b')

ax[1].plot(austin_weather["MONTH"], austin_weather["MLY-PRCP-NORMAL"],
           color='r')
ax[1].plot(austin_weather["MONTH"], austin_weather["MLY-PRCP-25PCTL"],
           linestyle='--', color='r')
ax[1].plot(austin_weather["MONTH"], austin_weather["MLY-PRCP-75PCTL"],
           linestyle='--', color='r')

ax[0].set_ylabel("Precipitation (inches)")
ax[1].set_ylabel("Precipitation (inches)")
ax[1].set_xlabel("Time (months)")
plt.show()


# =====================================================================
# 16. Sharing the y-axis range across subplots
# =====================================================================

# sharey=True forces every subplot to use the same y-axis range, which
# makes magnitudes directly comparable between them.
fig, ax = plt.subplots(2, 1, sharey=True)
