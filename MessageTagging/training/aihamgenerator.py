import csv
import os
import time
from tqdm import tqdm

from MessageTagging.training.chatgptprompter import Prompter
from MessageTagging.training.promptgenerator import PromptGenerator


def hamgenerator(iterations, output_file):
    prompter = Prompter()
    prompt_generator = PromptGenerator('companies.csv', 'names.csv')
    prompter.set_context(
        "Generate distinct, very short responses for a contact form, as an employer contacting a potential employee initially. Invent all names, avoid placeholders. No special formatting or line breaks. No subject line. Only provide the prompt. Just one answer at a time.")

    file_exists = os.path.isfile(output_file)  # Check if file exists

    with open(output_file, mode='a' if file_exists else 'w', newline='',
              encoding='utf-8') as file:  # Open file in append mode if exists, else in write mode
        writer = csv.writer(file)
        if not file_exists:  # Write header row only if file didn't exist before
            writer.writerow(['label', 'text'])

        for i in tqdm(range(iterations), desc="Generating Messages"):
            generated_prompt = prompt_generator.generate_prompt()
            generated_message = prompter.prompt(generated_prompt)
            writer.writerow(['ham', generated_message])
            file.flush()  # ensure that data is written to disk immediately


if __name__ == "__main__":
    start_time = time.time()  # Store the start time
    while (True):
        elapsed_time = time.time() - start_time  # Calculate the elapsed time
        if elapsed_time > 7200:  # Check if 2 hours (7200 seconds) have passed
            break  # If 2 hours have passed, exit the loop
        try:
            hamgenerator(100, 'training_data.csv')
        except Exception as e:  # Use `except` instead of `catch`
            print(f"Exception occurred: {e}. Restarted application")
