import os
import pandas as pd


def append_csv_in_directory(directory, output_file):
    # List all files in the specified directory
    files = os.listdir(directory)

    # Filter out the CSV files
    csv_files = [f for f in files if f.endswith('.csv')]

    # Initialize an empty list to hold the DataFrames
    dfs = []

    # Loop through the CSV files and append them to dfs list
    for csv_file in csv_files:
        file_path = os.path.join(directory, csv_file)
        df = pd.read_csv(file_path)
        dfs.append(df)

    # Concatenate all the DataFrames in the dfs list
    appended_df = pd.concat(dfs, ignore_index=True)

    # Write the appended DataFrame to the output file
    appended_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    # Specify the output file (in the current directory)
    output_file = 'appended_file.csv'

    # Get the current directory
    current_directory = os.getcwd()

    # Call the function
    append_csv_in_directory(current_directory, output_file)