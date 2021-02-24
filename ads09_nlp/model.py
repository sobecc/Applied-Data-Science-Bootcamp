from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def build_model():
    preprocessor = ColumnTransformer([("processing", TfidfVectorizer(stop_words='english'), "text")])
    return Pipeline([("preprocessor", preprocessor), ("model", MultinomialNB(alpha=.01))])
