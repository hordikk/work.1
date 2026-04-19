import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GroupKFold
data_frame = pd.read_csv("train.csv")
data_frame_test = pd.read_csv("test.csv")
#Function
def preprocesing(df):
    df = df.copy()
    only_str = df.select_dtypes(include="object").columns
    #future engineering
    df['TotalLot'] = df[["LotFrontage", "LotArea", 'TotalBsmtSF']].sum(axis=1)
    df["SFTotal"] =  df["2ndFlrSF"] + df["1stFlrSF"]
    df["AllBath"] = ( 0.5 * df["BsmtHalfBath"] + df["FullBath"] + df["BsmtFullBath"] + 0.5 * df["HalfBath"] )




    df = pd.get_dummies(df, columns=only_str)
    df["LotFrontage"] = df["LotFrontage"].fillna(df["LotFrontage"].median()).astype(int)
    df["GarageYrBlt"] = df["GarageYrBlt"].fillna(df["GarageYrBlt"].median()).astype(int)


    return df

def tune(X, y, group):
    gkf = GroupKFold(n_splits=3)

    param_grid = {

        'n_estimators': [500, 1000, 2000],
        "learning_rate": [0.01, 0.03, 0.05],
        "num_leaves": [32, 64, 128],
    }
    Search = RandomizedSearchCV(
        LGBMRegressor(verbose=-1, random_state=42),
        param_grid,
        cv=gkf,
    )
    Search.fit(X, y, groups=group)
    return Search.best_params_, Search.best_score_

def train_model_cv(X, y, group, n_splits=5):
    gkf = GroupKFold(n_splits=n_splits)
    mae_list = []
    mse_list = []

    for train_index, test_index in gkf.split(X, y, group):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        model = LGBMRegressor(
            n_estimators=500,
            random_state=42,
            learning_rate=0.01,
            predict_disable_shape_check=True,
            num_leaves=128,
            verbose=-1
        )
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        mae_list.append(mean_absolute_error(y_test, pred))
        mse_list.append(mean_squared_error(y_test, pred))
    final_model = LGBMRegressor(
        n_estimators=500,
        random_state=42,
        learning_rate=0.01,
        num_leaves=128,
        predict_disable_shape_check=True,
        verbose=-1
    )
    final_model.fit(X, y)
    return final_model, mae_list, mse_list
#X, y, group
X = preprocesing(data_frame.drop("SalePrice", axis=1))
X_value = preprocesing(data_frame_test)
X, X_value = X.align(X_value, join="left", axis=1, fill_value=0)
y = np.log1p(data_frame["SalePrice"])
groups = data_frame["Neighborhood"]

#tune
#best_params, best_score = tune(X, y, groups)
#final check value
final_model, mae_list, mse_list = train_model_cv(X, y, groups)
y_pred_log = final_model.predict(X_value)
y_pred = np.expm1(y_pred_log)
#result
res = pd.DataFrame({
    "Id": data_frame_test["Id"],
    "SalePrice": y_pred,
})
res.to_csv("submission.csv", index=False)
print(mae_list, mse_list)
