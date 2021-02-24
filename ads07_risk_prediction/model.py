from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import lightgbm as lgb


pr_info_char = {'A1': 1, 'A2': 1, 'A3': 1, 'A4': 1, 'A5': 1, 'A6': 6, 'A7': 1, 'A8': 1,
                'B1': 2, 'B2': 2, 'C1': 3, 'C2': 2, 'C3': 3, 'C4': 3, 'D1': 4, 'D2': 4,
                'D3': 4, 'D4': 4, 'E1': 5}
pr_info_num = {'A1': 1, 'A2': 2, 'A3': 3, 'A4': 4, 'A5': 5, 'A7': 7, 'A8': 8,
               'B1': 1, 'B2': 2, 'C1': 1, 'C2': 2, 'C3': 3, 'C4': 4,
               'D1': 1, 'D2': 2, 'D3': 3, 'D4': 4, 'E1': 1}


class Processor(BaseEstimator, TransformerMixin):

    def fit(self, *_):
        return self

    def transform(self, X, y=None):
        # Encoding Product_info_2
        # X['Product_Info_2_char'] = X.Product_Info_2.apply(lambda x: pr_info_char.get(x, 0))
        # X['Product_Info_2_num'] = X.Product_Info_2.apply(lambda x: pr_info_num.get(x, 0))
        # ADDING BMI * Age feature:
        X['BMI_Age'] = X['BMI'] * X['Ins_Age']
        # GETTING Medical_Keywords_Sum COLUMN:
        var_types = Variables()
        X['_Medical_Keywords_Sum'] = X[var_types.dummy].sum(axis=1)
        # LABEL ENCODE CATEGORICAL VARIABLES
        # PipeLabelEncoder(var_types.categorical_to_label).transform(X)
        # ReplaceNAN(var_types.replacenan_features)
        drop_feat = DropFeatures(var_types.to_drop)
        X = drop_feat.transform(X)

        return X


class DropFeatures:
    def __init__(self, features):
        self._features = features

    def fit(self, *_):
        return self

    def transform(self, X):
        return X.drop(self._features, axis=1)


class ReplaceNAN:
    def __init__(self, features, replacement_value=-100):
        self._features = features
        self.replacement_value = replacement_value

    def fit(self, *_):
        return self

    def transform(self, X):
        X[self._features] = X[self._features].fillna(self.replacement_value)
        return X


class PipeLabelEncoder:
    def __init__(self, categories):
        self._categories = categories
        self._encoder = LabelEncoder()

    def fit(self, X, _):
        self._encoder.fit(X[self._categories])
        return self

    def transform(self, X):
        X[self._categories] = X[self._categories].apply(self._encoder.fit_transform)
        return X


class Variables:
    def __init__(self):
        self.numerical = ['Product_Info_4', 'Ins_Age', 'Ht', 'Wt', 'BMI', 'Employment_Info_1', 'Employment_Info_4',
                          'Employment_Info_6', 'Insurance_History_5', 'Family_Hist_2', 'Family_Hist_3',
                          'Family_Hist_4', 'Family_Hist_5']

        self.categorical = ['Product_Info_1', 'Product_Info_2', 'Product_Info_3', 'Product_Info_5', 'Product_Info_6',
                            'Product_Info_7', 'Employment_Info_2', 'Employment_Info_3', 'Employment_Info_5',
                            'InsuredInfo_1', 'InsuredInfo_2', 'InsuredInfo_3', 'InsuredInfo_4', 'InsuredInfo_5',
                            'InsuredInfo_6', 'InsuredInfo_7', 'Insurance_History_1', 'Insurance_History_2',
                            'Insurance_History_3', 'Insurance_History_4', 'Insurance_History_7',
                            'Insurance_History_8', 'Insurance_History_9', 'Family_Hist_1', 'Medical_History_2',
                            'Medical_History_3', 'Medical_History_4', 'Medical_History_5',
                            'Medical_History_6', 'Medical_History_7', 'Medical_History_8', 'Medical_History_9',
                            'Medical_History_11', 'Medical_History_12', 'Medical_History_13', 'Medical_History_14',
                            'Medical_History_16', 'Medical_History_17', 'Medical_History_18', 'Medical_History_19',
                            'Medical_History_20', 'Medical_History_21', 'Medical_History_22', 'Medical_History_23',
                            'Medical_History_25', 'Medical_History_26', 'Medical_History_27', 'Medical_History_28',
                            'Medical_History_29', 'Medical_History_30', 'Medical_History_31', 'Medical_History_33',
                            'Medical_History_34', 'Medical_History_35', 'Medical_History_36', 'Medical_History_37',
                            'Medical_History_38', 'Medical_History_39', 'Medical_History_40', 'Medical_History_41']
        self.categorical_to_label = ['Product_Info_2', 'Product_Info_3']

        self.dummy = ['Medical_Keyword_1', 'Medical_Keyword_2', 'Medical_Keyword_3', 'Medical_Keyword_4',
                      'Medical_Keyword_5', 'Medical_Keyword_6', 'Medical_Keyword_7', 'Medical_Keyword_8',
                      'Medical_Keyword_9', 'Medical_Keyword_10', 'Medical_Keyword_11', 'Medical_Keyword_12',
                      'Medical_Keyword_13', 'Medical_Keyword_14', 'Medical_Keyword_15', 'Medical_Keyword_16',
                      'Medical_Keyword_17', 'Medical_Keyword_18', 'Medical_Keyword_19', 'Medical_Keyword_20',
                      'Medical_Keyword_21', 'Medical_Keyword_22', 'Medical_Keyword_23', 'Medical_Keyword_24',
                      'Medical_Keyword_25', 'Medical_Keyword_26', 'Medical_Keyword_27', 'Medical_Keyword_28',
                      'Medical_Keyword_29', 'Medical_Keyword_30', 'Medical_Keyword_31', 'Medical_Keyword_32',
                      'Medical_Keyword_33', 'Medical_Keyword_34', 'Medical_Keyword_35', 'Medical_Keyword_36',
                      'Medical_Keyword_37', 'Medical_Keyword_38', 'Medical_Keyword_39', 'Medical_Keyword_40',
                      'Medical_Keyword_41', 'Medical_Keyword_42', 'Medical_Keyword_43', 'Medical_Keyword_44',
                      'Medical_Keyword_45', 'Medical_Keyword_46', 'Medical_Keyword_47', 'Medical_Keyword_48']

        self.discrete = ['Medical_History_1', 'Medical_History_10', 'Medical_History_15', 'Medical_History_24',
                         'Medical_History_32']

        self.replacenan_features = ['Family_Hist_2', 'Family_Hist_3', 'Family_Hist_4', 'Family_Hist_5',
                                    'Medical_History_1', 'Medical_History_10', 'Medical_History_15',
                                    'Medical_History_24', 'Medical_History_32', 'Employment_Info_1',
                                    'Employment_Info_4', 'Employment_Info_6', 'Insurance_History_5']

        self.to_drop = ['Id', 'Product_Info_2']

    def print_numerical(self):
        print(self.numerical)


def build_model():
    preprocessor = Processor()
    clf_params = {'subsample_freq': 1, 'objective': 'multiclass', 'random_state': 1, 'num_class': 8, 'metric':
                  'multi_logloss', 'learning_rate': 0.1, 'bagging_fraction': 1, 'lambda': 0.8, 'num_leaves': 35,
                  'n_estimators': 120, 'max_depth': 15}

    model = lgb.LGBMClassifier(**clf_params)

    return Pipeline([("preprocessor", preprocessor), ("model", model)])
