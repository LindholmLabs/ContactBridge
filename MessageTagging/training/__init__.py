import pickle

import pandas as pd
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import os


def generate_model():
    current_dir = os.getcwd()

    data_path = os.path.join(current_dir, 'final_training_data.csv')
    model_save_path = os.path.join(current_dir, 'saved_model')

    ## Load data
    data = pd.read_csv(data_path, sep=';', header=0)
    data = data.dropna(subset=['text'])

    # Prepare text data
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(data['text'])

    sequences = tokenizer.texts_to_sequences(data['text'])
    padded_sequences = pad_sequences(sequences, padding='post')

    # Save tokenizer
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(padded_sequences,
                                                        data['label'].apply(lambda x: 1 if x == 'spam' else 0),
                                                        test_size=0.2, random_state=42)

    # Build model
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=16,
                                  input_length=padded_sequences.shape[1]),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # Compile model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train model
    model.fit(X_train, y_train, epochs=300, validation_data=(X_test, y_test))

    # Save the entire model to a file
    print(f'Model will be saved to: {model_save_path}')
    model.save(model_save_path)


if __name__ == "__main__":
    generate_model()