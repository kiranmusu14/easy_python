"""
Sharing Your Visualizations With Others
-----------------------------------------
Preparing a Matplotlib figure to hand off to someone else: switching the
overall visual style with plt.style.use(), saving a figure to disk in
different formats/resolutions/sizes, and automating figure creation by
looping over the unique values in a column instead of hardcoding each
group. Ends with pointers to where to explore Matplotlib further.

Table of Contents
1. Changing plot style with plt.style.use()
2. The "ggplot" style
3. Returning to the default style
4. The "bmh" style
5. Seaborn styles: "seaborn-colorblind"
6. Guidelines for choosing a plotting style
7. A figure to share
8. Saving the figure to file
9. Different file formats
10. Setting the resolution (dpi)
11. Setting the figure size
12. A different aspect ratio
13. Why automate figures from data?
14. How many different kinds of data are there?
15. Getting unique values of a column
16. Automatically building a bar chart with a loop
17. Where to go next
"""

# NOTE: seattle_weather and austin_weather are the monthly climate
# DataFrames used in the earlier chapters.

# =====================================================================
# 1. Changing plot style with plt.style.use()
# =====================================================================

# This is the default look, before any style has been chosen.
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-TAVG-NORMAL"])
ax.plot(austin_weather["MONTH"], austin_weather["MLY-TAVG-NORMAL"])
ax.set_xlabel("Time (months)")
ax.set_ylabel("Average temperature (Fahrenheit degrees)")
plt.show()


# =====================================================================
# 2. The "ggplot" style
# =====================================================================

# plt.style.use(name) changes fonts, colors, gridlines, etc. for every
# figure created afterward, in this case mimicking R's ggplot2 look.
plt.style.use("ggplot")
fig, ax = plt.subplots()
ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-TAVG-NORMAL"])
ax.plot(austin_weather["MONTH"], austin_weather["MLY-TAVG-NORMAL"])
ax.set_xlabel("Time (months)")
ax.set_ylabel("Average temperature (Fahrenheit degrees)")
plt.show()


# =====================================================================
# 3. Returning to the default style
# =====================================================================

# Gotcha: plt.style.use() is global and persists for the rest of the
# script/session — reset explicitly with "default" to get back to the
# original look.
plt.style.use("default")


# =====================================================================
# 4. The "bmh" style
# =====================================================================

# Full gallery of available styles:
# https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
plt.style.use("bmh")
fig, ax = plt.subplots()
ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-TAVG-NORMAL"])
ax.plot(austin_weather["MONTH"], austin_weather["MLY-TAVG-NORMAL"])
ax.set_xlabel("Time (months)")
ax.set_ylabel("Average temperature (Fahrenheit degrees)")
plt.show()


# =====================================================================
# 5. Seaborn styles: "seaborn-colorblind"
# =====================================================================

# Seaborn-derived styles are a good choice when color needs to be
# distinguishable by colorblind readers.
plt.style.use("seaborn-colorblind")
fig, ax = plt.subplots()
ax.plot(seattle_weather["MONTH"], seattle_weather["MLY-TAVG-NORMAL"])
ax.plot(austin_weather["MONTH"], austin_weather["MLY-TAVG-NORMAL"])
ax.set_xlabel("Time (months)")
ax.set_ylabel("Average temperature (Fahrenheit degrees)")
plt.show()


# =====================================================================
# 6. Guidelines for choosing a plotting style
# =====================================================================

# - Dark backgrounds are usually less visible (e.g. when projected).
# - If color matters, prefer colorblind-friendly styles such as
#   "seaborn-colorblind" or "tableau-colorblind10".
# - If the figure may be printed, prefer a style that uses less ink.
# - If it will be printed in black-and-white, use the "grayscale" style.


# =====================================================================
# 7. A figure to share
# =====================================================================

# NOTE: medals is the same Olympic-medals DataFrame used in the
# quantitative-comparisons chapter.
fig, ax = plt.subplots()

ax.bar(medals.index, medals["Gold"])
ax.set_xticklabels(medals.index, rotation=90)
ax.set_ylabel("Number of medals")

plt.show()


# =====================================================================
# 8. Saving the figure to file
# =====================================================================

# fig.savefig(path) writes the figure to disk instead of (or as well
# as) displaying it; the file format is inferred from the extension.
fig, ax = plt.subplots()
ax.bar(medals.index, medals["Gold"])
ax.set_xticklabels(medals.index, rotation=90)
ax.set_ylabel("Number of medals")
fig.savefig("gold_medals.png")
# $ ls
# gold_medals.png


# =====================================================================
# 9. Different file formats
# =====================================================================

# .jpg supports a quality= setting (0-100, trading off file size against
# image quality); .svg is a scalable vector format.
fig.savefig("gold_medals.jpg")
fig.savefig("gold_medals.jpg", quality=50)
fig.savefig("gold_medals.svg")


# =====================================================================
# 10. Setting the resolution (dpi)
# =====================================================================

# dpi= controls the pixel density of a raster (e.g. .png) output.
fig.savefig("gold_medals.png", dpi=300)


# =====================================================================
# 11. Setting the figure size
# =====================================================================

# fig.set_size_inches([width, height]) sets the physical figure size
# before saving.
fig.set_size_inches([5, 3])


# =====================================================================
# 12. A different aspect ratio
# =====================================================================

# Swapping width and height flips a wide figure into a tall one.
fig.set_size_inches([3, 5])


# =====================================================================
# 13. Why automate figures from data?
# =====================================================================

# - Ease and speed
# - Flexibility
# - Robustness
# - Reproducibility


# =====================================================================
# 14. How many different kinds of data are there?
# =====================================================================

# NOTE: summer_2016_medals is a pandas DataFrame assumed already loaded,
# with one row per athlete/medal and a "Sport" column, indexed by ID.
print(summer_2016_medals["Sport"])
# ID
# 62            Rowing
# 65         Taekwondo
# 73          Handball
#              ...
# 134759      Handball
# 135132    Volleyball
# 135205        Boxing
# Name: Sport, Length: 976, dtype: object


# =====================================================================
# 15. Getting unique values of a column
# =====================================================================

# .unique() collapses a column down to its distinct values — the set of
# groups to loop over next.
sports = summer_2016_medals["Sport"].unique()
print(sports)
# ['Rowing' 'Taekwondo' 'Handball' 'Wrestling'
#  'Gymnastics' 'Swimming' 'Basketball' 'Boxing'
#  'Volleyball' 'Athletics']


# =====================================================================
# 16. Automatically building a bar chart with a loop
# =====================================================================

# Looping over sports and filtering the DataFrame each time builds one
# bar (with error bars) per sport, without hardcoding any sport name.
fig, ax = plt.subplots()

for sport in sports:
    sport_df = summer_2016_medals[summer_2016_medals["Sport"] == sport]
    ax.bar(sport, sport_df["Height"].mean(),
           yerr=sport_df["Height"].std())

ax.set_ylabel("Height (cm)")
ax.set_xticklabels(sports, rotation=90)
plt.show()


# =====================================================================
# 17. Where to go next
# =====================================================================

# Further Matplotlib resources:
# - Example gallery: https://matplotlib.org/gallery.html
# - Plotting data in 3D: https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html
# - Visualizing images with pseudo-color: https://matplotlib.org/users/image_tutorial.html
# - Animations: https://matplotlib.org/api/animation_api.html
# - Matplotlib for geospatial data (Cartopy): https://scitools.org.uk/cartopy/docs/latest/

# pandas + Matplotlib = Seaborn: statistical plots built directly from
# a DataFrame, with Matplotlib underneath.
# NOTE: mpg is a pandas DataFrame assumed already loaded (Seaborn's
# built-in "mpg" dataset).
import seaborn

seaborn.relplot(x="horsepower", y="mpg", hue="origin", size="weight",
                 sizes=(40, 400), alpha=.5, palette="muted",
                 height=6, data=mpg)
# Seaborn example gallery: https://seaborn.pydata.org/examples/index.html
