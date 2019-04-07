import configparser
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
import lightgbm as lgb
from sklearn.metrics import accuracy_score

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('config.ini')

data = config.get('FILE', 'DATA')


def compare_model(x_train, y_train):
    models = []
    models.append(("LR", LogisticRegression()))
    models.append(("DT", DecisionTreeClassifier()))
    models.append(("SVM", SVC()))
    models.append(("NB", GaussianNB()))
    models.append(("KNN",KNeighborsClassifier()))
    models.append(("RF", RandomForestClassifier()))
    models.append(("GB", GradientBoostingClassifier()))
    models.append(("AB",AdaBoostClassifier()))
    models.append(("ANN", MLPClassifier()))

    for name, model in models:
        model.fit(x_train, y_train)
        y_pred = model.predict(x_train)
        print(name, "'s Accuracy is ", accuracy_score(y_train, y_pred))


def run_lgb(x_train, y_train)
    # create dataset for lightgbm
    lgb_train = lgb.Dataset(x_train, y_train)
    # specify your configurations as a dict
    params = {
        'boosting_type': 'gbdt',
        'objective': 'regression',
        'metric': {'l2', 'l1'},
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': 0
    }
    print('Starting training...')
    # train
    gbm = lgb.LGBMRegressor(num_leaves=31,
                            learning_rate=0.05,
                            n_estimators=20)
    gbm.fit(x_train, y_train,
            eval_set=[(x_train, y_train)],
            eval_metric='l1',
            early_stopping_rounds=10)
    y_pred = gbm.predict(x_train)
    # convert into binary values
    for i in range(len(y_pred)):
        if y_pred[i] >= .5:
            y_pred[i] = 1
        else:
            y_pred[i] = 0

    print("LGB's Accuracy is ", accuracy_score(y_train, y_pred))



if __name__ == "__main__":
    df = pd.read_csv(data)
    x_train = df.iloc[:, :-1].values
    y_train = df.iloc[:, -1].values

    compare_model(x_train, y_train)
    run_lgb(x_train, y_train)