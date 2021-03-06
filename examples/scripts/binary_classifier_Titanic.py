import pandas as pd
from supervised.automl import AutoML
import os

from sklearn.metrics import accuracy_score

df = pd.read_csv("tests/data/Titanic/train.csv")

X = df[df.columns[2:]]
y = df["Survived"]

automl = AutoML(
        results_path="examples/AutoML_Titanic",
        total_time_limit=60*60,
        start_random_models=10,
        hill_climbing_steps=3,
        top_models_to_improve=3,
        train_ensemble=True)

automl.fit(X, y)

pred = automl.predict(X)

print("Train accuracy", accuracy_score(y, pred["label"]))

test = pd.read_csv("tests/data/Titanic/test_with_Survived.csv")
test_cols = [
        "Parch",
        "Ticket",
        "Fare",
        "Pclass",
        "Name",
        "Sex",
        "Age",
        "SibSp",
        "Cabin",
       "Embarked"
    ]
pred = automl.predict(df[test_cols])
print("Test accuracy", accuracy_score(test["Survived"], pred["label"]))

