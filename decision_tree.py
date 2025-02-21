import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.tree import export_text

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

feature_importances = pd.DataFrame({'Feature': X.columns, 'Importance': dt.feature_importances_})
feature_importances = feature_importances.sort_values(by="Importance", ascending=False).head(10)

print("Features:")
print(feature_importances)

tree_rules = export_text(dt, feature_names=list(X.columns))
print(tree_rules)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

