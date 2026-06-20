# ==========================================
# CHAPTER 1: LOAD AND PROFILE DATA
# ==========================================

import pandas as pd

print("--- 1. OVERVIEW PROFILE ---")
nf_movies = pd.read_csv('netflix_analysis.csv')
print(nf_movies.shape)
print(nf_movies.head())

# Step 2 — Deep inspection
print("\n--- 2. STRUCTURE & MISSING DATA ---")
print(nf_movies.info())
print("\nMissing Cells Per Column:")
print(nf_movies.duplicated().sum())
print(nf_movies.isnull().sum())
print(nf_movies.dtypes)

print("\n--- 3. NUMERIC RANGE INSPECTION (Business Logic Check) ---")
print(nf_movies.describe())       #This catches impossible years or weird numbers in numeric columns

print("\n--- 4. TEXT COLUMNS DETAIL LOOP ---")
text_columns = nf_movies.select_dtypes(include=['object', 'str']).columns
for column in text_columns:
    print(f"\n{column}:")
    print(f"\n==================== Column: {column} ====================")
    print(nf_movies[column].value_counts())

    # 1. CALCULATE: Tell Python what number to count first (empty cells)
    empty_counts = nf_movies[column].isnull().sum()      # Calculate and display empty cells for this specific column

    # 2. DISPLAY: Print the summary sentence using that calculated number
    print(f"Total empty cells: {empty_counts}, out of {len(nf_movies[column])}")

   # Business Check: Do we have hidden spaces or mixed casing inflating our piles?
    print("\n--- text formatting inconsistencies (spaces of casing)------")
    raw_unique = nf_movies[column].nunique()
    clean_unique = nf_movies[column].astype(str).str.lower().str.strip().nunique()
    if raw_unique != clean_unique:
        print(f"Warning: {column} has text formatting inconsistencies (spaces of casing)")
    else:
        print(f"{column}: No Errors found")

print("\n--- 5. FINAL REDUNDANCY CHECK ---")
# Check for useless columns
# Make sure this is  moved outside the loop so it only runs once at the very end
useless_columns = [column for column in nf_movies.columns
                    if nf_movies[column].nunique() == 1]
print(f"Useless columns found: {useless_columns}")

# ==========================================
# CHAPTER 2: DATA CLEANING STAGE
# ==========================================
#----------------SOLUTIONS-------------------------
# --- STEP 0: PRE-CLEANING RESCUE (Place it right here!) ---
# 1. Identify rows where the duration leaked into the rating column
leaked_rows = nf_movies['rating'].str.contains('min', na=False)
# 2. Rescue: Copy the minute strings into the empty duration column for those rows
nf_movies.loc[leaked_rows, 'duration'] = nf_movies.loc[leaked_rows, 'rating']
# 3. Cleanup: Overwrite those leaked rows in the rating column with 'NR'
nf_movies.loc[leaked_rows, 'rating'] = 'NR'
# print("\n------6. Data Cleaning Stage------------")
# 1. Fill personnel and origin gaps with 'Not Disclosed'
nf_movies['director'] = nf_movies['director'].fillna('Not Disclosed')
nf_movies['cast'] = nf_movies['cast'].fillna('Not Disclosed')
nf_movies['country'] = nf_movies['country'].fillna('Not Disclosed')

# ----------------CHECK--------------------------
print(f"Empty cells in director: {nf_movies['director'].isnull().sum()}")
print(f"Empty cells in cast: {nf_movies['cast'].isnull().sum()}")
print(f"Empty cells in country: {nf_movies['country'].isnull().sum()}")

# 2. Fill minor metadata gaps with standard placeholders
nf_movies['date_added'] = nf_movies['date_added'].fillna('Unknown Date')
nf_movies['rating'] = nf_movies['rating'].fillna('NR')  # NR stands for 'Not Rated'
nf_movies['duration'] = nf_movies['duration'].fillna('Unknown Duration')

# ----------------CHECK--------------------------
print(f"Empty cells in date: {nf_movies['date_added'].isnull().sum()}")
print(f"Empty cells in rating: {nf_movies['rating'].isnull().sum()}")
print(f"Empty cells in duration: {nf_movies['duration'].isnull().sum()}")

# Converting date_added to real date
nf_movies['date_added'] = pd.to_datetime(nf_movies['date_added'], errors='coerce')
# Confirm it
print(f"The new data type added for the date_added column is: {nf_movies['date_added'].dtype}")
nf_movies['year_added'] = nf_movies['date_added'].dt.year
print(f"\n---------------Summary of Uploads per year---------------")
print(nf_movies['year_added'].value_counts())

# WORKING ON DURATION
cleaned_text = nf_movies['duration'].str.replace(' min', '', case=False).str.strip()
# 2. Extract only Movie minutes safely using a numeric translator
nf_movies.loc[nf_movies['type'] == 'Movie', 'movie_min'] = pd.to_numeric(cleaned_text, errors='coerce')
print(f"The average runtime for Netflix movie is: {nf_movies['movie_min'].mean():.1f}minutes")

# 1. Strip out 'season' or 'seasons' text cleanly by removing common characters
cleaned_seasons = nf_movies['duration'].str.replace(' Seasons', '', case=False).str.replace(' Season', '', case=False).str.strip()
# 2. Extract only TV Show seasons safely and save them using our GPS locator
nf_movies.loc[nf_movies['type'] == 'TV Show', 'tv_seasons'] = pd.to_numeric(cleaned_seasons, errors='coerce')
print(f"The average average number of seasons for a Netflix TV show! is: {nf_movies['tv_seasons'].mean():.1f} Seasons")

# 1. Chop the text by commas and multiply into separate rows
exploded_countries = nf_movies.assign(country=nf_movies['country'].str.split(', ')).explode('country')
# 2. Print our new top 5 country leaderboard
print('\n---------Top 5 Countries (Cleaned and Unbundled-----------')
print(exploded_countries['country'].value_counts().head())

# 1. Chop the genres by commas and multiply into separate rows
exploded_genres = nf_movies.assign(listed_in=nf_movies['listed_in'].str.split(', ')).explode('listed_in')
# 2. Print the true top genres leaderboard
print("\n-------Top Genre leader board--------")
print(exploded_genres['listed_in'].value_counts().head())

# Save your final cleaned data:
nf_movies.to_csv('Netflix movies and TV Shows Cleaned Data.csv', index=False)
print("Cleaned Data Saved Successfully")


# ==========================================
# CHAPTER 3: DATA VISUALIZATION STAGE
# ==========================================
import matplotlib.pyplot as plt
# 1. Grab the top 5 genres from your clean, unbundled table
top_genres = exploded_genres['listed_in'].value_counts().head()
# 2. Build a horizontal bar chart canvas with Netflix crimson bars
# Create a standard-sized blank canvas for our chart (10 inches wide, 5 inches tall)
plt.figure(figsize=(10, 5))
# Draw the horizontal bar chart using our top genres data and color the bars Netflix crimson red
plt.barh(top_genres.index, top_genres.values, color='crimson')

# Add a bold main title to the top of our chart for business presentations
plt.title('Top 5 Genres on Netflix', fontsize=14, fontweight='bold')

# Label the bottom axis so people know the bars represent the movie show count
plt.xlabel('Total Movie & TV Show Count', fontsize=12)

# Flip the chart upside down so our #1 most popular genre is displayed at the very top
plt.gca().invert_yaxis()
# Automatically adjust the margins so none of our text labels get cut off at the edges
plt.tight_layout()
plt.savefig('Top 5 Genres on Netflix.png', dpi=300)

# Master layout and launch triggers
plt.show(block=True)


# Question 1 ("What type of content dominates — Movies or TV Shows?")
# Group our dataset by content type and count the total number of Movies vs TV Shows
content_counts = nf_movies['type'].value_counts()
plt.figure(figsize=(6, 6))
# Draw the pie chart using our content counts, add percentage labels, and apply custom colors
plt.pie(content_counts.values, labels = content_counts.index, autopct='%1.1f%%',
        startangle=90, colors=['crimson', 'black'], textprops={'color': 'white', 'weight': 'bold'})
plt.legend(labels=content_counts.index, loc='upper left', frameon=False)
plt.title('Netflix Catalog Breakdown: Movies vs. TV Shows', fontsize=14, fontweight='bold')
plt.tight_layout()
# Save the chart dashboard as a professional high-resolution PNG image
plt.savefig('Netflix Catalog Breakdown: Movies vs. TV Shows.png', dpi=300)

# Master layout and launch triggers
plt.show(block=True)


# Question 2: Which country produces the most content?
# building the Top 5 Countries chart leaderboard
top_countries = exploded_countries['country'].value_counts().head()
plt.figure(figsize=(10, 5))
plt.barh(top_countries.index, top_countries.values, color='crimson')

# Add our business presentation titles and labels
plt.title('Top Countries on Netflix', fontsize=14, fontweight='bold')
plt.xlabel('Country Count', fontsize=12)
plt.gca().invert_yaxis()
plt.tight_layout()
# Save the chart dashboard as a professional high-resolution PNG image
plt.savefig('Top Countries on Netflix.png', dpi=300)

# Master layout and launch triggers
plt.show(block=True)

# Question 3: What is the most common rating?
# Count the age ratings and grab the top 5 most common ones
top_ratings = nf_movies['rating'].value_counts().head()
plt.figure(figsize=(10, 5))
# Draw vertical skyscraper bars and save them into a variable name
rating_bars = plt.bar(top_ratings.index, top_ratings.values, color='crimson')
# Automatically stamp the exact volumes directly on top of each skyscraper head
plt.bar_label(rating_bars, padding=3, fontweight='bold')

# Add our business presentation titles and labels
plt.title('Top 5 Content Ratings on Netflix', fontsize=14, fontweight='bold')
plt.xlabel('Age Rating Category', fontsize=12)
plt.ylabel('Total Movies and TV Shows', fontsize=12)
plt.tight_layout()
# Save the chart dashboard as a professional high-resolution PNG image
plt.savefig('Top 5 Content Ratings on Netflix.png', dpi=300)

# Master layout and launch triggers
plt.show(block=True)

# Question 4: How has content addition grown over the years?
# Group our data by year, count the total uploads, and sort them chronologically by year number
yearly_trend = nf_movies['year_added'].value_counts().sort_index()

# Draw a smooth timeline trend line using our sorted data, make it crimson, and add dot markers
plt.figure(figsize=(10, 5))
plt.plot(yearly_trend.index, yearly_trend.values, color='crimson', marker='o', linewidth=2)

# On a line chart, we must label both axes because the numbers run in two different directions
# (years running horizontally, and upload counts running vertically).
plt.title('Netflix Content Upload Velocity Over Time', fontsize=14, fontweight='bold')
plt.xlabel('Year Content Was Added', fontsize=12)
plt.ylabel('Total Movies and TV Shows Uploaded', fontsize=12)
plt.xticks(yearly_trend.index, rotation=45)

# Add a faint grid background so it is easy to trace the exact coordinate values
plt.grid(axis='both', linestyle='--', alpha=0.5)
plt.tight_layout()
# Save the chart dashboard as a professional high-resolution PNG image
plt.savefig('Netflix Content Upload Velocity Over Time.png', dpi=300)

# Master layout and launch triggers
plt.show(block=True)


# FOR ALL DISPLAY IN GRID

# Roll out one massive master canvas and split it into a 2-row, 2-column grid frame
fig, axes = plt.subplots(2, 2, figsize=(15, 10), constrained_layout=True)

# Question 1 ("What type of content dominates — Movies or TV Shows?")
# 1. Count the data for Box 1
content_counts = nf_movies['type'].value_counts()
# 2. Paint directly inside the top-left box coordinate slot (Row 0, Column 0)
axes[0, 0].pie(content_counts.values, labels = content_counts.index, autopct='%1.1f%%',
        startangle=90, colors=['crimson', 'black'], textprops={'color': 'white', 'weight': 'bold'})
axes[0, 0].legend(labels=content_counts.index, bbox_to_anchor=(1, 1), frameon=False)
# 3. Set the bold title specifically inside the frame of the top-left box
axes[0, 0].set_title('Netflix Catalog Breakdown: Movies vs. TV Shows', fontsize=14, fontweight='bold')

# Question 2: Which country produces the most content?
top_countries = exploded_countries['country'].value_counts().head()
axes[0, 1].barh(top_countries.index, top_countries.values, color='crimson')

# Add our business presentation titles and labels
axes[0, 1].set_title('Top Countries on Netflix', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Country Count', fontsize=12)
axes[0, 1].invert_yaxis()

# Question 3: What is the most common rating?
# Count the age ratings and grab the top 5 most common ones
top_ratings = nf_movies['rating'].value_counts().head()
# Draw vertical skyscraper bars and save them into a variable name
rating_bars = axes[1, 0].bar(top_ratings.index, top_ratings.values, color='crimson')
# Automatically stamp the exact volumes directly on top of each skyscraper head
axes[1, 0].bar_label(rating_bars, padding=3, fontweight='bold')

# Add our business presentation titles and labels
axes[1, 0].set_title('Top 5 Content Ratings on Netflix', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Age Rating Category', fontsize=12)
axes[1, 0].set_ylabel('Total Movies and TV Shows', fontsize=12)


# Question 4: How has content addition grown over the years?
# Group our data by year, count the total uploads, and sort them chronologically by year number
yearly_trend = nf_movies['year_added'].value_counts().sort_index()

# Draw a smooth timeline trend line using our sorted data, make it crimson, and add dot markers
axes[1, 1].plot(yearly_trend.index, yearly_trend.values, color='crimson', marker='o', linewidth=2)

# On a line chart, we must label both axes because the numbers run in two different directions
# (years running horizontally, and upload counts running vertically).
axes[1, 1].set_title('Netflix Content Upload Velocity Over Time', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Year Content Was Added', fontsize=12)
axes[1, 1].set_ylabel('Total Movies and TV Shows Uploaded', fontsize=12)

# Fix: Split the year marker setup and the rotation switch into their proper tools
axes[1, 1].set_xticks(yearly_trend.index)
axes[1, 1].tick_params(axis='x', rotation=45)

# Add your faint grid background
axes[1, 1].grid(axis='both', linestyle='--', alpha=0.5)

# Save the entire 4-chart dashboard as a professional high-resolution PNG image
plt.savefig('Netflix_Business_Dashboard.png', dpi=300)

# Master layout and launch triggers
plt.show(block=True)