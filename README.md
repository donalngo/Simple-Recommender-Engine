# Recommendation_System
Standalone Recommendation System for Future use

# Integration Methods
To use Recommendation Engine, Import Recommendation Library and call Match Function.
1. Hard_Rules Variable and Soft_Rule Variable Variable is a list of string. 
2. To be match with strings in Hard and Soft Rules folder files.

## Installation
```
pip install glob itertools numpy
```

## Using the code
```
from Recommendation import Match

Match.ToRecommendationEngine(Hard_Rules,Soft_Rules)
```

# Output
List of Strings and values 
eg.    [(['Product A', 'Product B'], 0.5)]
First value states Software with assigned scores based on matches from recommendation

Sorted in Accordance to :
1. No. of software
2. Score


# Logs
Logs are created in Recommendation\Log folder, consisting of the following files:
1. Dropped Requirements
2. System Error Logs
3. Input/Output


# Managing Soft and Hard Rules
CSV Files located in these 2 locations:
1. Soft Rules - ./Recommendation/Soft Rules
2. Hard Rules - ./Recommendation/Hard Rules


Hard and Soft rules works in 2 axis:
1. X axis - Software Type/Details/Features
2. Y axis - Software Name

## Hard Rules
In the above mentioned assignments, Assign '1' (True) or '0' (False) to each software per category.
- ** All criteria must be completely assigned and order of software must match Soft Rules files to work. **
- ** All criteria must be unique to avoid conflicts **

## Soft Rules

Soft Rules include a group score in each CSV file as a weight multiplier for each CSV file.
This multiplier is located at the (1,1) position of the CSV file.
- ** All criteria must be completely assigned and order of software must match Hard Rules files to work. **
- ** All criteria must be unique to avoid conflicts **

 
# Files (Not to be touched unless necessary)
1. init - Library Initialization
2. Match - Main Function for matching
3. Utils - Utilities used for matching between soft and hard rules
4. SoftRules - Abstract of Soft Rules
5. HardRules - Abstract of Hard Rules


