import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# Load dataset
data = pd.read_csv("../dataset/bagasse_data.csv")

# Encode categorical data
le = LabelEncoder()

data["impurity_level"] = le.fit_transform(data["impurity_level"])
data["color"] = le.fit_transform(data["color"])
data["odor"] = le.fit_transform(data["odor"])
data["quality_label"] = le.fit_transform(data["quality_label"])

# Features and labels
X = data.drop("quality_label", axis=1)
y = data["quality_label"]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
with open("model.pk1", "wb") as f:
    pickle.dump(model, f)

print("Model trained successfully and saved as model.pk1")