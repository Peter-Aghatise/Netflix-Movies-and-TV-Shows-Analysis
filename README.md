# Netflix Movies and TV Shows Analysis

## Project Overview
Comprehensive analysis of Netflix's global content catalog covering 8,807 movies and TV shows 
to uncover content trends, audience targeting strategies, and growth patterns using Python, 
Pandas and Matplotlib.

## Business Questions Answered
- What type of content dominates — Movies or TV Shows?
- Which country produces the most Netflix content?
- What is the most common content rating?
- How has Netflix content addition grown over the years?
- What are the top genres on Netflix?

## Tools Used
- Python
- Pandas
- Matplotlib

## Data Cleaning Highlights
- Handled 2,634 missing director values filled with 'Not Disclosed'
- Rescued duration data incorrectly stored in rating column (74 min, 84 min, 66 min)
- Converted date_added column from text to proper datetime format
- Extracted year added as separate column for trend analysis
- Split multi-value country and genre columns using explode() for accurate counting
- Separated duration into movie minutes and TV show seasons

## Key Findings
- Movies dominate Netflix catalog at 69.6% vs TV Shows at 30.4%
- United States leads content production with 3,689 titles — over 3x second-place India
- TV-MA is the most common rating with 3,207 titles — Netflix primarily targets mature adults
- Content additions exploded from 2015
