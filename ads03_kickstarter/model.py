import json
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
# from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier


def diff_in_days(df, time1, time2):
    days_diff = pd.to_datetime(df[time1], unit='s') - pd.to_datetime(df[time2], unit='s')
    out = pd.DataFrame(data={'difference_days': days_diff.dt.days})
    return out


def preprocess(df):
    df.dropna(subset=['name'], inplace=True, axis=0)
    df.reset_index(drop=True, inplace=True)
    msk_eval = df.evaluation_set
    X_eval = df[msk_eval].drop(['state', 'evaluation_set'], axis=1)
    X = df[~msk_eval].drop(['state', 'evaluation_set'], axis=1)
    y = df[~msk_eval]['state']
    X.reset_index(drop=True, inplace=True)
    y.reset_index(drop=True, inplace=True)
    X_eval.reset_index(drop=True, inplace=True)
    return X, y, X_eval


class MyFeatures:
    def fit(self, *_):
        return self

    def transform(self, X):
        df = X.copy()
        # multiplying goal with static_uds_rate and log
        df["goal_usd"] = df["goal"] * df["static_usd_rate"]
        df["goal_usd_log"] = np.log1p(df["goal_usd"])
        # adding campaign_duration
        df['campaign_duration'] = diff_in_days(df, 'deadline', 'launched_at')
        df['usd_day'] = df.goal_usd/df.campaign_duration
        # extracting category info
        df_categ = df['category'].apply(json.loads)
        # extracting profile info (active/inactive)
        df_profile = json_normalize(df['profile'].apply(json.loads)).state == 'inactive'
        # getting new frame with columns
        df = df[['goal_usd', "goal_usd_log", 'campaign_duration', 'usd_day', 'launched_at', 'country']]
        df = df.join(json_normalize(df_categ)[['slug', 'position', 'id']])
        df['profile_inactive'] = df_profile.astype('b')
        return df


class Scaler:
    def __init__(self, features):
        self._features = features
        self._scaler = None

    def fit(self, X, _):
        scaler = preprocessing.MinMaxScaler()
        scaler.fit(X[self._features])
        self._scaler = scaler
        return self

    def transform(self, X):
        df = X[self._features]
        trdf = self._scaler.transform(df)
        return pd.DataFrame(trdf, columns=df.columns).join(X.drop(self._features, axis=1))


class OneHot:
    def __init__(self, categories):
        self._categories = categories
        self._model = None

    def fit(self, X, _):
        self._model = preprocessing.OneHotEncoder(drop='first', sparse=False)
        self._model.fit(X[self._categories])
        return self

    def transform(self, X):
        array = self._model.transform(X[self._categories])
        cols = self._model.get_feature_names(self._categories)
        df = pd.DataFrame(array, columns=cols).join(X)
        df.drop(self._categories, axis=1, inplace=True)
        return df


def train(X, y):
    """Trains a new model on X and y and returns it.

    :param X: your processed training data
    :type X: pd.DataFrame
    :param y: your processed label y
    :type y: pd.DataFrame with one column or pd.Series
    :return: a trained model
    """
    categorical = ['slug', 'country']
    numerical = ['goal_usd', "goal_usd_log", 'campaign_duration', 'usd_day', 'launched_at', 'position', 'id']
    features = ('make_features', MyFeatures())
    dummy = ('dummy', OneHot(categorical))
    scale = ('scale', Scaler(numerical))
    pca = ('pca', PCA(n_components=0.80, whiten=True))
    # clf = ('clf', LogisticRegression(penalty='l2', C=0.003, solver='liblinear'))
    clf = ('clf', KNeighborsClassifier(n_neighbors=39, weights='distance'))

    pipeline = Pipeline([features, dummy, scale, pca, clf])

    return pipeline.fit(X, y)


def predict(model, X_test):
    y_pred = model.predict(X_test)
    return y_pred


# _df = pd.read_csv("data/kickstarter.csv")
# _X, _y, _X_eval = preprocess(_df)
# _model = train(_X, _y)
# print(predict(_model, _X_eval).sum())
