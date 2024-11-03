import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load ACS data from the CSV file
file_path = 'turn_016.csv'
df = pd.read_csv(file_path)

df.columns = [
    'District',
    'Total_Population',
    'Total_Pop_Citizenship',
    'US_Born_Citizen',
    'US_Territory_Born_Citizen',
    'US_Born_Abroad_Citizen',
    'Naturalized_Citizen',
    'Non_Citizen',
    'Total_Votes',
    'Over_18'
]

# Total citizens
df['Total_Citizens'] = (df['US_Born_Citizen'] + df['US_Territory_Born_Citizen'] +
                        df['US_Born_Abroad_Citizen'] + df['Naturalized_Citizen'])

# Eligible voters
df['Eligible_Voters'] = (df['Total_Citizens'] / df['Total_Pop_Citizenship']) * df['Over_18']

model_data = df[['District', 'Total_Population', 'Eligible_Voters', 'Total_Votes']]

# target vars
X = model_data[['Total_Population', 'Eligible_Voters']]
y = model_data['Total_Votes']

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = LinearRegression()
model.fit(X_train, y_train)

district_15_data_2023 = {
    'Total_Population': 745893,  
    'Eligible_Voters': 584241     
}

district_15_df = pd.DataFrame([district_15_data_2023])

#Test
predicted_votes = model.predict(district_15_df)
turnout_rate = predicted_votes[0]/584241*100

print(f"Predicted total votes: {predicted_votes[0]}")
print(f"Predicted rate: {turnout_rate}")
