
import pandas as pd
import numpy as np

# Load MovieLens datasets
movies = pd.read_csv("dataset/movies.csv")
ratings = pd.read_csv("dataset/ratings.csv")

# Explore Movies Dataset
print("========== MOVIES DATA ==========")
print(movies.head())

print("\nMovies Shape:", movies.shape)

# Explore Ratings Dataset
print("\n========== RATINGS DATA ==========")
print(ratings.head())

print("\nRatings Shape:", ratings.shape)

# Check missing values
print("\n========== MISSING VALUES ==========")
print("Movies:")
print(movies.isnull().sum())

print("\nRatings:")
print(ratings.isnull().sum())

# Count unique users and movies
print("\n========== DATASET SUMMARY ==========")
print("Unique Users:", ratings["userId"].nunique())
print("Unique Movies:", ratings["movieId"].nunique())
print("Total Ratings:", len(ratings))

print("\nDataset exploration completed successfully!")



# Verify Live Session Dataset Files

import pandas as pd

processed = pd.read_csv("dataset/processed_movies.csv")
train = pd.read_csv("dataset/train_ratings.csv")
test = pd.read_csv("dataset/test_ratings.csv")

print("\n========== LIVE SESSION DATASET VERIFICATION ==========")

print("\nProcessed Movies:")
print(processed.shape)
print(processed.head())

print("\nTraining Ratings:")
print(train.shape)
print(train.head())

print("\nTesting Ratings:")
print(test.shape)
print(test.head())

print("\nMissing Values:")
print("Processed:", processed.isnull().sum().sum())
print("Train:", train.isnull().sum().sum())
print("Test:", test.isnull().sum().sum())
