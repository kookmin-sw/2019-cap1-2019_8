import configparser
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
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



if __name__ == "__main__":
    df = pd.read_csv(data)
    x_train = df.iloc[:, :-1].values
    y_train = df.iloc[:, -1].values

    compare_model(x_train, y_train)