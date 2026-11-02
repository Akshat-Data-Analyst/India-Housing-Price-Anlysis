import pandas as pd

df = pd.read_csv("data/india_housing_prices.csv")
# first five rows in dataset
print(df.head())
# check total rows and columns in dataset
print("Dataset Shape:", df.shape)
# check coulumns and datatypes in dataset
print(df.info())

# check columns name in dataset
print("\n Columns Names:")
print(df.columns.tolist())

# Check Missing Values in dataset
print("\n Missing Values:")
print(df.isnull().sum())

# Check Duplicate Rows in Dataset
print("\n Duplicate Rows:", df.duplicated().sum())

# Data Cleaning

# Making a copy of the Original Dataset
df_cleaned = df.copy()

# Check Missing values
print("\nMissing Values Before Cleaning:")
print(df_cleaned.isnull().sum().sum())

# Remove Duplicate rows 
df_cleaned = df_cleaned.drop_duplicates()

# Checking the dataset after cleaning
print("\nOriginal Dataset Shape:", df.shape)
print("Cleaned Dataset Shape:", df_cleaned.shape)

# Checking for duplicate rows after cleaning
print("Duplicate Rows After Cleaning:", df_cleaned.duplicated().sum())


# Saving the cleaned dataset to a CSV file
df_cleaned.to_csv("data/india_housing_prices_cleaned.csv", index=False)

print("\nCleaned dataset successfully saved!")


# Data Quality Check

print("\n--- DATA QUALITY REPORT ---")

# Total rows aur columns
print("Total Rows:", df_cleaned.shape[0])
print("Total Columns:", df_cleaned.shape[1])

# Missing values
print("\nMissing Values in Each Column:")
print(df_cleaned.isnull().sum())

# Duplicate rows
print("\nTotal Duplicate Rows:", df_cleaned.duplicated().sum())

# Data types
print("\nColumn Data Types:")
print(df_cleaned.dtypes)


# Numerical Data Validation

print("\n--- NUMERICAL DATA VALIDATION ---")

# Property price check
print("Minimum Property Price (Lakhs):", df_cleaned["Price_in_Lakhs"].min())
print("Maximum Property Price (Lakhs):", df_cleaned["Price_in_Lakhs"].max())

# Property size check
print("Minimum Property Size:", df_cleaned["Size_in_SqFt"].min())
print("Maximum Property Size:", df_cleaned["Size_in_SqFt"].max())

# BHK check
print("Minimum BHK:", df_cleaned["BHK"].min())
print("Maximum BHK:", df_cleaned["BHK"].max())

# Property year check
print("Minimum Year Built:", df_cleaned["Year_Built"].min())
print("Maximum Year Built:", df_cleaned["Year_Built"].max())

# Negative values check
print("\nNegative Property Prices:", (df_cleaned["Price_in_Lakhs"] < 0).sum())
print("Zero or Negative Sizes:", (df_cleaned["Size_in_SqFt"] <= 0).sum())
print("Zero or Negative BHK:", (df_cleaned["BHK"] <= 0).sum())


# Construction Year Validation

invalid_years = (
    (df_cleaned["Year_Built"] < 1900)
    | (df_cleaned["Year_Built"] > 2026)
).sum()

print("Invalid Construction Years:", invalid_years)


# Step 8: Final Data Validation

print("\n--- FINAL VALIDATION ---")

# Construction year check
invalid_years = (
    (df_cleaned["Year_Built"] < 1900)
    | (df_cleaned["Year_Built"] > 2026)
).sum()

print("Invalid Construction Years:", invalid_years)

# Final dataset quality check
print("Missing Values:", df_cleaned.isnull().sum().sum())
print("Duplicate Rows:", df_cleaned.duplicated().sum())

print("Final Dataset Shape:", df_cleaned.shape)


# Part-1 Exploratory Data Analysis (EDA)

print("\n--- PROPERTY TYPE ANALYSIS ---")

# Har property type ki count nikalna
property_counts = df_cleaned["Property_Type"].value_counts()

print(property_counts)


# Part-2: Create a chart of Property types

import matplotlib.pyplot as plt

property_counts = df_cleaned["Property_Type"].value_counts()

plt.figure(figsize=(8, 5))

property_counts.plot(kind="bar")

plt.title("Number of Properties by Property Type")
plt.xlabel("Property Type")
plt.ylabel("Number of Properties")

plt.xticks(rotation=0)
plt.tight_layout()

plt.show()


# State-wise Average Property Price Analysis

print("\n--- STATE-WISE AVERAGE PROPERTY PRICE ---")

state_avg_price = df_cleaned.groupby("State")["Price_in_Lakhs"].mean()

state_avg_price = state_avg_price.sort_values(ascending=False)

print(state_avg_price.round(2))


# City-wise Average Property Price Analysis

print("\n--- CITY-WISE AVERAGE PROPERTY PRICE ---")

city_avg_price = df_cleaned.groupby("City")["Price_in_Lakhs"].mean()

city_avg_price = city_avg_price.sort_values(ascending=False)

print(city_avg_price.round(2))
