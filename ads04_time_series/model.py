# import pandas as pd
from fbprophet import Prophet


def preprocess(df):
    """This function takes a dataframe and preprocesses it so it is
    ready for the training stage.

    The DataFrame contains the time axis and the target column.

    It also contains some rows for which the target column is unknown.
    Those are the observations you will need to predict for KATE
    to evaluate the performance of your model.

    Here you will need to return the training time serie: ts together
    with the preprocessed evaluation time serie: ts_eval.

    Make sure you return ts_eval separately! It needs to contain
    all the rows for evaluation -- they are marked with the column
    evaluation_set. You can easily select them with pandas:

         - df.loc[df.evaluation_set]


    :param df: the dataset
    :type df: pd.DataFrame
    :return: ts, ts_eval
    """
    # remane for Prophet
    df = df.rename(columns={'day': 'ds', 'consumption': 'y'})

    msk_eval = df.evaluation_set
    df.drop("evaluation_set", axis=1, inplace=True)

    # Split training/test data
    ts = df[~msk_eval]
    ts_eval = df[msk_eval]

    # outlier_model = Prophet(growth='linear', daily_seasonality=False, weekly_seasonality=1, yearly_seasonality=1)
    # outlier_model.fit(ts)
    # boundaries = outlier_model.predict()[['yhat_lower', 'yhat_upper']]
    # ts.y = ts.y.mask((ts.y < boundaries.yhat_lower) | (ts.y > boundaries.yhat_upper))

    return ts, ts_eval


def train(ts):
    """Trains a new model on ts and returns it.

    :param ts: your processed training time serie
    :type ts: pd.DataFrame
    :return: a trained model
    """
    forecast_model = Prophet(
        growth='linear',
        mcmc_samples=35,
        daily_seasonality=False,
        weekly_seasonality=5,
        yearly_seasonality=1)
    forecast_model.add_seasonality(name='monthly', period=30.5, fourier_order=1)
    forecast_model.add_country_holidays(country_name='GB')
    forecast_model.fit(ts)

    return forecast_model


def predict(model, ts_test):
    """This functions takes your trained model as well
    as a processed test time serie and returns predictions.

    On KATE, the processed testt time serie will be the ts_eval you built
    in the "preprocess" function. If you're testing your functions locally,
    you can try to generate predictions using a sample test set of your
    choice.

    This should return your predictions either as a pd.DataFrame with one column
    or a pd.Series

    :param model: your trained model
    :param ts_test: a processed test time serie (on KATE it will be ts_eval)
    :return: y_pred, your predictions
    """
    preds = model.predict(ts_test)
    # preds = preds[['ds', 'yhat']]
    # preds.set_index(pd.to_datetime(preds.ds), inplace=True)
    # preds.drop("ds", axis=1, inplace=True)

    return preds.yhat
