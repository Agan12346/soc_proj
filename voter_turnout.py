import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from a CSV file
data = pd.read_csv('cong_voting.csv')

print(data.head())
print(data.info())


# Check for missing values
print(data.isnull().sum())


# Generate descriptive statistics
print(data.describe())

