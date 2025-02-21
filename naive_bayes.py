import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer

df = pd.read_csv("combined_district_data_cong.csv") 

cat_cols = ["Winning Party"]
df[cat_cols] = df[cat_cols].apply(LabelEncoder().fit_transform)
df = df.drop(columns=["Voter Turnout (%)"])
df = df.select_dtypes(include=[np.number])

X = df.drop(columns=["Winning Party"])
y = df["Winning Party"]
imputer = SimpleImputer(strategy='-')
X = imputer.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

nb = GaussianNB()
nb.fit(X_train, y_train)

y_pred = nb.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
