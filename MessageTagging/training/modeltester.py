import pickle
import os
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# Set the paths
current_dir = os.getcwd()
model_save_path = os.path.join(current_dir, 'saved_model')
tokenizer_save_path = os.path.join(current_dir, 'tokenizer.pickle')

# Load the saved model and tokenizer
model = tf.keras.models.load_model(model_save_path)

with open(tokenizer_save_path, 'rb') as handle:
    tokenizer = pickle.load(handle)

def detect_spam(text):
    # Convert text to sequence and pad it
    sequences = tokenizer.texts_to_sequences([text])
    padded_sequences = pad_sequences(sequences, padding='post', maxlen=5530)  # Updated maxlen to 5530

    # Make prediction
    prediction = model.predict(padded_sequences)[0][0]

    # Convert prediction to label
    label = 'Spam' if prediction >= 0.5 else 'Not Spam'
    confidence = prediction if prediction >= 0.5 else 1 - prediction

    return label, confidence

# Test the function
if __name__ == "__main__":
    while True:
        user_input = input("Enter a message (or type 'exit' to exit): ")
        if user_input.lower() == 'exit':
            break
        label, confidence = detect_spam(user_input)
        print(f'The message is {label} with a confidence of {confidence * 100:.2f}%.')