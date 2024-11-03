import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier, XGBRegressor

train_data = pd.read_csv("combined_district_data.csv")
train_data = train_data[train_data['Year'].isin([2016, 2018, 2022])]

# Features
selected_columns = [
    'Total_Population', 'Total_Pop_Citizenship', 'US_Born_Citizen', 'US_Territory_Born_Citizen',
    'US_Born_Abroad_Citizen', 'Naturalized_Citizen', 'Non_Citizen', 'Total_Pop_Birth', 'Native_Born',
    'Foreign_Born', 'Total_Foreign_Born', 'Entered_2010_Later', 'Entered_2000_2009', 'Entered_Before_2000',
    'Pop_5Years_Over', 'White_Alone', 'Black_Alone', 'Native_American_Alone', 'Asian_Alone',
    'Pacific_Islander_Alone', 'Other_Race_Alone', 'Two_Or_More_Races', 'Hispanic_Latino', 'Total_Male',
    'Total_Female', 'Median_Household_Income', 'Total_Households_Income', 'Income_Less_10000',
    'Income_10000_14999', 'Income_15000_19999', 'Income_20000_24999', 'Income_25000_29999',
    'Income_30000_34999', 'Income_35000_39999', 'Income_40000_44999', 'Income_45000_49999',
    'Income_50000_59999', 'Income_60000_74999', 'Income_75000_99999', 'Income_100000_124999',
    'Income_125000_149999', 'Income_150000_199999', 'Income_200000_Plus', 'Total_Pop_Poverty',
    'Below_Poverty_Level', 'Pop_25_Over', 'No_Schooling', 'High_School_Diploma', 'Some_College_Less_1yr',
    'Associates_Degree', 'Bachelors_Degree', 'Masters_Degree', 'Professional_Degree', 'Doctorate_Degree',
    'Total_Households', 'Family_Households', 'Married_Couple_Family', 'Other_Family', 'Nonfamily_Households',
    'Living_Alone', 'Not_Living_Alone', 'In_Labor_Force', 'Civilian_Labor_Force', 'Employed', 'Unemployed',
    'Total_Housing_Units', 'Owner_Occupied', 'Renter_Occupied', 'Workers_16_Over', 'Commute_Car',
    'Commute_Public_Transit', 'Commute_Bicycle', 'Commute_Walk', 'Work_From_Home', 'Total_Households_Internet',
    'Has_Internet', 'No_Internet', 'Dist_clean'
]

X = train_data[selected_columns]
y_classification = train_data['Winning Party']
y_regression = train_data[['Votes Blue', 'Votes Red']]

le = LabelEncoder()
y_classification_encoded = le.fit_transform(y_classification)

# Split data into training and test
X_train, X_test, y_train_class, y_test_class = train_test_split(X, y_classification_encoded, test_size=0.2, random_state=42)
X_train, X_test, y_train_reg, y_test_reg = train_test_split(X, y_regression, test_size=0.2, random_state=42)

# Train
#Winning party
clf = XGBClassifier(random_state=42)
clf.fit(X_train, y_train_class)

#Vote counts
reg = XGBRegressor(random_state=42)
reg.fit(X_train, y_train_reg)

# Load the test data
test_data_path = 'il_congressional_districts_acs_2016_2018_2022.csv'
test_data = pd.read_csv(test_data_path)

# Filter
district_15_2023 = test_data[(test_data['Year'] == 2023) & (test_data['Dist_clean'] == 15)]
district_15_2023 = district_15_2023[selected_columns]

# Test
# Winning party
y_pred_class_d15 = clf.predict(district_15_2023)
predicted_winners = le.inverse_transform(y_pred_class_d15)

#Vote cts
y_pred_reg_d15 = reg.predict(district_15_2023)

# Display predictions
print("Predicted winning paty:", predicted_winners)
print("Predicted vote counts:", y_pred_reg_d15)
