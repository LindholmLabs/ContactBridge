import csv
import random
import string
import os


def generate_random_word(max_length=40):
    length = random.randint(1, max_length)
    word = ''.join(random.choices(string.ascii_lowercase, k=length))
    return word


def generate_random_sentence(max_words=10):
    num_words = random.randint(1, max_words)
    sentence = ' '.join(generate_random_word() for _ in range(num_words))
    if random.random() < 0.5:
        sentence += '.'
    return sentence


def main():
    num_sentences = 500  # Number of sentences to generate (you can change this)

    # Get the current directory
    current_directory = os.getcwd()
    # Construct the path to the output file in the current directory
    output_file = os.path.join(current_directory, 'final_training_data.csv')

    # Check if the file already exists to decide on writing headers
    file_exists = os.path.isfile(output_file)

    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['label', 'text'])  # Write header row if file does not exist

        for i in range(num_sentences):
            sentence = generate_random_sentence()
            writer.writerow(['spam', sentence])


if __name__ == "__main__":
    main()