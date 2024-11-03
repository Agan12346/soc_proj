import pandas as pd

# Read both CSVs
df_old = pd.read_csv('il_congressional_districts_acs_2016_2018_2022.csv')
df_2020 = pd.read_csv('2020_data.csv')

# Matching columns
column_mapping = {
    'District': 'District',
    'Total_Population': 'Total_Pop',
    'White_Alone': 'White_Count',
    'Black_Alone': 'Black_Count',
    'Asian_Alone': 'Asian_Count',
    'Hispanic_Latino': 'Hispanic_Count',
    'Foreign_Born': 'Foreign_Born_Count',
    'Total_Male': lambda x: x['Total_Pop'] - x['Female_Count'],
    'Total_Female': 'Female_Count',
    'Median_Household_Income': 'Median_Income',
    'Below_Poverty_Level': 'Total_In_Poverty',
    'In_Labor_Force': lambda x: x['Total_Pop'] - x['Unemployed_Count'],
    'Unemployed': 'Unemployed_Count',
    'Owner_Occupied': 'Owner_Occupied_Units',
    'Commute_Public_Transit': 'Public_Transit_Users'
}

df_2020_matched = pd.DataFrame()

# Fill in matched columns
for old_col, new_col in column_mapping.items():
    if callable(new_col):
        # Handle calculated columns
        df_2020_matched[old_col] = new_col(df_2020)
    else:
        # Direct column mapping
        df_2020_matched[old_col] = df_2020[new_col]

df_2020_matched['Year'] = 2020

df_2020_matched['Dist_clean'] = df_2020_matched['District']

# Keep only the columns that exist in the original dataset
existing_columns = df_old.columns
df_2020_matched = df_2020_matched[df_2020_matched.columns.intersection(existing_columns)]

# Append the new data to the existing dataset
df_combined = pd.concat([df_old, df_2020_matched], ignore_index=True)

# Sort
df_combined = df_combined.sort_values(['Year', 'District'])

df_combined.to_csv('combined_district_data.csv', index=False)
