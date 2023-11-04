import pickle
import os
import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences


class SpamDetector:
    def __init__(self):
        current_dir = os.getcwd()
        model_save_path = os.path.join(current_dir, 'MessageTagging/saved_model')
        tokenizer_save_path = os.path.join(current_dir, 'MessageTagging/tokenizer.pickle')

        self.model = self.load_model(model_save_path)
        self.tokenizer = self.load_tokenizer(tokenizer_save_path)

    @staticmethod
    def load_model(model_save_path):
        return tf.keras.models.load_model(model_save_path)

    @staticmethod
    def load_tokenizer(tokenizer_save_path):
        with open(tokenizer_save_path, 'rb') as handle:
            return pickle.load(handle)

    def detect_spam(self, text):
        sequences = self.tokenizer.texts_to_sequences([text])
        padded_sequences = pad_sequences(sequences, padding='post', maxlen=5530)

        return self.model.predict(padded_sequences)[0][0]


if __name__ == "__main__":
    spam_detector = SpamDetector()

    prediction = spam_detector.detect_spam('Hello, here today at not a scam.cu.uk.rust create your own mlm now')

    if prediction < .05:
        print("not spam")
    else:
        print("spam")

    print(f'Prediction: {prediction:.2f}')