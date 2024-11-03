import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv("combined_district_data_cleaned_2016_2020.csv")

#Extract columns
selected_columns = [
    'Total_Population', 'Non_Citizen', 'Native_Born', 'Foreign_Born',
    'White_Alone', 'Black_Alone', 'Hispanic_Latino', 'Total_Male', 'Male_Under_5',
    'Total_Households_Income', 'Median_Household_Income', 'Below_Poverty_Level',
    'Dist_clean'
]
X = data[selected_columns]

y_classification = data['Winner']
y_regression = data[['D', 'R']]

#Winner to int
le = LabelEncoder()
y_classification_encoded = le.fit_transform(y_classification)

#Split data into training and test sets
X_train, X_test, y_train_class, y_test_class = train_test_split(X, y_classification_encoded, test_size=0.2, random_state=42)
X_train, X_test, y_train_reg, y_test_reg = train_test_split(X, y_regression, test_size=0.2, random_state=42)

#Train
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train_class)

reg = RandomForestRegressor(random_state=42)
reg.fit(X_train, y_train_reg)

test_data_path = 'il_congressional_districts_acs_2016_2018_2022.csv'
test_data = pd.read_csv(test_data_path)

#Filter
district_15_data = test_data[(test_data['Year'] == 2023) & (test_data['Dist_clean'] == 15)]
district_15_data = district_15_data[selected_columns]

#Test
y_pred_class_d15 = clf.predict(district_15_data)
predicted_winners = le.inverse_transform(y_pred_class_d15)

y_pred_reg_d15 = reg.predict(district_15_data)

print("Predicted winner:", predicted_winners[0])
print("Predicted vote counts:", y_pred_reg_d15[0])
