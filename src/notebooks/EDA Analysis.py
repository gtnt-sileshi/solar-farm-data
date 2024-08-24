#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Print the current working directory for debugging
print("Current Working Directory:", os.getcwd())

# Load the CSV file (update the path if necessary)
data = pd.read_csv("data/benin-malanville.csv")

# Display the first few rows of the dataframe
print(data.head())

# Display the shape of the dataframe
print(data.shape)

# Describe the dataframe
print(data.describe())

# Check for unique values in a few selected columns
print(data['Comments'].unique())
print(data['Cleaning'].unique())

# Check for missing values
print(data.isnull().sum())

# If needed, drop any columns with a high number of missing values (more than 50% missing)
threshold = len(data) * 0.5
data_cleaned = data.dropna(axis=1, thresh=threshold)

# Display the first few rows after any potential cleaning
print(data.head())

# Univariate Analysis: Distribution plots
fig, ax = plt.subplots(1, 2, figsize=(20, 6))
sns.histplot(data['Tamb'], ax=ax[0])  # Adjust column names as needed
ax[0].set_title("Tamb")
sns.histplot(data['RH'], ax=ax[1])  # Adjust column names as needed
ax[1].set_title("RH")
plt.ylim(0, 2500)
plt.show()

# Scatter plots
a4_dims = (20, 7)
fig, axs = plt.subplots(ncols=3, figsize=a4_dims)
sns.scatterplot(x="GHI", y="DNI", ax=axs[0], data=data)  # Adjust columns as needed
sns.scatterplot(x="GHI", y="DHI", ax=axs[1], data=data)  # Adjust columns as needed
sns.scatterplot(x="DNI", y="DHI", ax=axs[2], data=data)  # Adjust columns as needed

plt.show()
