from keras.layers.core import Dense
from keras.models import Sequential
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline


class Preprocessor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = X.reshape(X.shape[0], 784)

        if y is None:
            return X

        y = np_utils.to_categorical(y, 4)
        return X, y


def keras_builder():
    model = Sequential()
    model.add(Dense(16, input_shape=(784,), activation="relu"))
    model.add(Dense(4, activation="softmax"))
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    return model


def build_model():
    preprocessor = Preprocessor()

    model = KerasClassifier(build_fn=keras_builder, batch_size=16, epochs=3)

    return Pipeline([("preprocessor", preprocessor), ("model", model)])
