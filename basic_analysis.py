import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("Illinois_District_all.csv")
print("Missing values:")
df.isnull().sum

#Basic info
print("Shape of the dataset:", df.shape)
print("Column Data Types:")
print(df.dtypes)

print("First few rows of the dataset:")
print(df.head())

#Convert columns with "Estimate" or "MOE" in their name to numeric types
for col in df.columns:
    if 'Estimate' in col or 'MOE' in col:
        df[col] = pd.to_numeric(df[col], errors='coerce')

#Check
print("New data type:")
print(df.dtypes)

print("Missing values in cols:")
print(df.isnull().sum())

print("Summary stats:")
print(df.describe())

print("Unique val cts:")
for column in df.columns:
    print(f"{column}: {df[column].nunique()} unique values")

#Histograms for numerical cols
numeric_df = df.select_dtypes(include=['float64', 'int64'])

if not numeric_df.empty:
    numeric_df.hist(bins=20, figsize=(15, 10))
    plt.show()
else:
    print("No numeric columns.")

#Bar charts
categorical_columns = df.select_dtypes(include=['object']).columns

for col in categorical_columns:
    plt.figure(figsize=(10, 5))
    sns.countplot(y=col, data=df)
    plt.title(f"Distribution of {col}")
    plt.show()

#Correlation matrix
if not numeric_df.empty:
    print("Correlation matrix for numerical columns:")
    corr_matrix = numeric_df.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix")
    plt.show()
else:
    print("No numeric columns available.")
