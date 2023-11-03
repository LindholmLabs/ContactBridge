import os
import pandas as pd


def clean_csv(input_file, output_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Loop through each column in the DataFrame
    for column in df.columns:
        # Convert NaN values to empty strings
        df[column] = df[column].fillna('')

        # Ensure the column data is of string type
        df[column] = df[column].astype(str)

        # Replace newline characters with spaces
        df[column] = df[column].str.replace('\n', ' ')

        # Replace multiple consecutive commas with a single comma
        df[column] = df[column].str.replace(',+', ',')

    # Write the cleaned DataFrame to a new CSV file
    df.to_csv(output_file, index=False)


def clean_all_csv_in_directory(directory):
    # List all files in the specified directory
    files = os.listdir(directory)

    # Filter out the CSV files
    csv_files = [f for f in files if f.endswith('.csv')]

    # Loop through the CSV files and clean them
    for csv_file in csv_files:
        input_file = os.path.join(directory, csv_file)
        output_file = os.path.join(directory, 'cleaned_' + csv_file)
        clean_csv(input_file, output_file)


if __name__ == "__main__":
    # Get the current directory
    current_directory = os.getcwd()

    # Specify the input and output files
    input_file = os.path.join(current_directory, 'appended_file.csv')
    output_file = os.path.join(current_directory, 'cleaned_appended_file.csv')

    # Call the function
    clean_csv(input_file, output_file)