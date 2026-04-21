from typing import final

import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, RandomizedSearchCV
from sklearn.metrics import accuracy_score
from lightgbm import LGBMClassifier
from PIL.Image import register_extension
df_value = pd.read_csv("test.csv")
df = pd.read_csv("train.csv")
def preprocesing(df):
    df = df.copy()

    df["PassengerIdNumber"] = df["PassengerId"].str[:4].astype(int)
    df["PassengerIdGroup"] = df["PassengerId"].str[5:].astype(int)

    df["CabinNuN"] = np.where(df["Cabin"].isna(), 1, 0)
    df["Cabin"] = df["Cabin"].fillna("U/0/U")
    df[["CabinLater1", "CabinNum", "CabinLater2"]] = df["Cabin"].str.split("/", expand=True)
    df["CabinNum"] = df["CabinNum"].astype(int)
    df["Age"] = df["Age"].fillna(0).astype(int)

    df[["RoomService", "FoodCourt", "ShoppingMall", "Spa", 'VRDeck']] = df[["RoomService", "FoodCourt", "ShoppingMall", "Spa", 'VRDeck']].fillna(0).astype(int)

    df["TotalSpend"] = df[["RoomService", "FoodCourt", "ShoppingMall", "Spa", 'VRDeck']].sum(axis=1)
    df['MaxSpend'] = df[["RoomService", "FoodCourt", "ShoppingMall", "Spa", 'VRDeck']].max(axis=1)
    df["AnySpend"] = np.where(df["TotalSpend"] > 0, 1, 0)
    df["LuxuryUser"] = np.where(df['Spa'] + df["VRDeck"] > 0, 1, 0 )
    df["Kapsula"]  = np.where(df["TotalSpend"] == 0, 1, 0 )
    df['GroupSize'] = df.groupby("PassengerIdNumber")["PassengerIdNumber"].transform("count")
    df["IsAlone"] = np.where(df["GroupSize"] == 1, 1, 0)
    df["Yang"] = np.where(df['Age'] <= 18, 1, 0)
    df['MiddleAge'] = np.where((df['Age'] > 18) & (df["Age"] <= 40), 1, 0)
    df["Old"] = np.where(df['Age'] > 40, 1, 0)
    df['PlanetMeanSpend'] = df.groupby("HomePlanet")["TotalSpend"].transform("mean")
    df["Planet_VIP"] = df["HomePlanet"] + "_" + df["VIP"].astype(str)

    df = pd.get_dummies(df, columns=["HomePlanet", "CryoSleep", "Destination", "VIP", 'CabinNuN', "CabinLater1", "CabinLater2", "LuxuryUser", "Kapsula", "AnySpend", "IsAlone", "Yang", "MiddleAge", "Old", "Planet_VIP"])
    df = df.drop(columns=["Name", "Cabin", "PassengerId"])

    return df
def tune(x, y):
    gkf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    parameters = {
        "n_estimators": [500, 800, 1000, 900, 1100, 1500],
        "max_depth": [ 5, 6, 9, 10, 12],
        "num_leaves": [32, 64, 128, 256, 512],
        "learning_rate": [0.1, 0.01, 0.02, 0.03, 0.04],

    }
    Search = RandomizedSearchCV(
        LGBMClassifier(random_state=42, verbose=-1),
        parameters,
        cv=gkf,
        scoring='accuracy',
    )
    Search.fit(x, y)
    return Search.best_params_, Search.best_score_
def train_model_cv(X, y, n_splits=5):
    kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    acc_list = []
    for train_index, test_index in kf.split(X, y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        model = LGBMClassifier(
            n_estimators=900,
            learning_rate=0.01,
            num_leaves=32,
            max_depth=5,
            verbose=-1,
        )
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        acc_list.append(accuracy_score(y_test, pred))
    final_model = LGBMClassifier(
        n_estimators=700,
        learning_rate=0.03,
        num_leaves=32,
        max_depth=9,
        verbose=-1,
    )
    final_model.fit(X, y)
    return final_model, acc_list
#X, y
X = preprocesing(df)
y = X["Transported"]
X = X.drop(columns=["Transported"])
group = df["HomePlanet"]

#res
final_model, acc = train_model_cv(X, y, n_splits=5)

X_value = preprocesing(df_value)
y_pred = final_model.predict(X_value)
X, X_value = X.align(X_value, join="left", axis=1, fill_value=0)
print(acc)