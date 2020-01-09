import tensorflow as tf
import tensorflow_datasets as tfds
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import joblib


def preprocess(X_batch, y_batch):
    X_batch = tf.strings.substr(X_batch, 0, 300)
    X_batch = tf.strings.regex_replace(X_batch, b"<br\\s*/?>", b" ")
    X_batch = tf.strings.regex_replace(X_batch, b"[^a-zA-Z']", b" ")
    X_batch = tf.strings.split(X_batch)
    return X_batch.to_tensor(default_value=b"<pad>"), y_batch


class CreateFeatures(BaseEstimator, TransformerMixin):
    '''
    Args:
        X: dataframe to be pre-processed

    Output:
        Dataframe transforms raw data into specific feature elements ready to be used for classfication
    '''

    def __init__(self):  # no *args or **kargs
        return None

    def fit(self, X, y=None):
        return self  # nothing else to do

    def transform(self, X, y=None):

        (X_train, y_train), (X_test, y_test) = tf.keras.datasets.imdb.load_data()

        word_index = tf.keras.datasets.imdb.get_word_index()
        id_to_word = {id_ + 3: word for word, id_ in word_index.items()}
        for id_, token in enumerate(("<pad>", "<sos>", "<unk>")):
            id_to_word[id_] = token

        " ".join([id_to_word[id_] for id_ in X_train[0][:10]])

        datasets, info = tfds.load(
            "imdb_reviews", as_supervised=True, with_info=True)
        train_size = info.splits["train"].num_examples

        from collections import Counter
        vocabulary = Counter()
        for X_batch, y_batch in datasets["train"].batch(32).map(preprocess):
            for review in X_batch:
                vocabulary.update(list(review.numpy()))

        vocab_size = 10000
        truncated_vocabulary = [
            word for word, count in vocabulary.most_common()[:vocab_size]]

        words = tf.constant(truncated_vocabulary)
        word_ids = tf.range(len(truncated_vocabulary), dtype=tf.int64)
        vocab_init = tf.lookup.KeyValueTensorInitializer(words, word_ids)
        num_oov_buckets = 1000
        table = tf.lookup.StaticVocabularyTable(vocab_init, num_oov_buckets)

        return table.lookup(tf.constant([X.split()]))


def final_pipeline(feature):
    pipeline = Pipeline([
        ('preprocess', CreateFeatures()),
    ])

    X = pipeline.fit_transform(feature)
    return X


loaded_ld_model = joblib.load('models/langauge_detector.joblib')
target_languages = [
    'Arabic',
    'German',
    'English',
    'Spanish',
    'French',
    'Italian',
    'Japanese',
    'Dutch',
    'Polish',
    'Portugese',
    'Russian']

loaded_sa_model = tf.keras.models.load_model('models/sentiment_analysis.h5')
# feature_transformer = joblib.load('models/feature_transformer.pkl')


class Predict:

    def __init__(self, user_input):
        self.user_input = user_input

    def detect_language(self):
        user_input = self.user_input
        prediction = loaded_ld_model.predict(user_input)
        return target_languages[prediction[0]]

    def analyze_sentiment(self):
        user_input = final_pipeline(self.user_input)
        return loaded_sa_model.predict(user_input)[0][0]
