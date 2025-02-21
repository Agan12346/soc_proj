import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

df = pd.read_csv("combined_district_data_cong.csv")

df["Winning Party"] = LabelEncoder().fit_transform(df["Winning Party"])

df = df.select_dtypes(include=[np.number])
df.fillna(df.median(), inplace=True)

X = df.drop(columns=["Winning Party"])
y = df["Winning Party"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

dt = DecisionTreeClassifier(criterion="gini", random_state=42)
dt.fit(X_train, y_train)
y_pred = dt.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
