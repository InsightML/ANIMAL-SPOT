import pandas as pd
import shutil
import os
import numpy as np
from pydub import AudioSegment

from sequence_len_calculator import get_audio_length_in_milliseconds
from common_tools import run_on_files

def clean_and_concatenate(value, delimiter):
    """Clean and concatenate values with a given delimiter."""
    if pd.isnull(value):
        return ""
    if isinstance(value, int):
        return f"{value}{delimiter}"
    value = str(value).replace(" ", "").replace("_", "-").replace(".", "-")
    return f"{value}{delimiter}"

def construct_filename(row, columns):
    """Construct the new filename from the DataFrame row."""
    cleaned_values = []
    after_info = False
    
    for col in columns:
        if col == 'CLASSNAME':
            cleaned_values.append(clean_and_concatenate("target", "-"))
            continue
        if col == 'LABELINFO (Optional)' or after_info:
            cleaned_values.append(clean_and_concatenate(row[col], "_"))
            after_info = True
        else:
            cleaned_values.append(clean_and_concatenate(row[col], "-"))
    
    filename = "".join(cleaned_values).rstrip("-_") + ".wav"
    return filename

def process_call_audio_files(excel_file, input_wav_folder, output_wav_folder, columns_to_process):
    """
    Processes audio files based on metadata in an Excel file.
    
    Parameters:
    - excel_file (str): Path to the Excel file containing metadata.
    - input_wav_folder (str): Path to the folder containing the input .wav files.
    - output_wav_folder (str): Path to the folder where processed .wav files will be saved.
    - columns_to_process (list): List of column names to use for constructing new filenames.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_wav_folder, exist_ok=True)

    # Load the Excel file
    df = pd.read_excel(excel_file, sheet_name='Data')

    # Process each row in the DataFrame
    for index, row in df.iterrows():
        new_filename = construct_filename(row, columns_to_process)
        try:
            source_file = os.path.join(input_wav_folder, row['FILENAME'])
        except TypeError:
            print(f"Error processing row {index}: Filename not found")
            continue
        destination_file = os.path.join(output_wav_folder, new_filename)

        try:
            shutil.copy(source_file, destination_file)
            print(f"File copied: {source_file} -> {destination_file}")
        except FileNotFoundError:
            print(f"File not found: {source_file}")

# Columns to process
columns_to_process = [
    'CLASSNAME', 'Reef', 'Time of day', 'Breeding', 'Rank',
    'Interaction with', 'LABELINFO (Optional)', 'ID', 'YEAR',
    'TAPENAME', 'START TIME (MS)', 'END TIME (MS)'
]

def split_audio(input_file_path, chunk_length_ms, output_folder, filename=None):
    # Load the audio file
    audio = AudioSegment.from_file(input_file_path)
    
    # Get the base filename without extension
    base_filename = filename if filename else os.path.splitext(os.path.basename(input_file_path))[0]
    
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Calculate number of chunks
    total_length_ms = len(audio)
    num_chunks = (total_length_ms + chunk_length_ms - 1) // chunk_length_ms  # Ceiling division
    
    # Split and save chunks
    for i in range(num_chunks):
        start_time = i * chunk_length_ms
        end_time = min(start_time + chunk_length_ms, total_length_ms)
        chunk = audio[start_time:end_time]
        
        chunk_filename = f"{base_filename}_chunk_{i + 1}.wav"
        chunk_path = os.path.join(output_folder, chunk_filename)
        
        chunk.export(chunk_path, format="wav")
        print(f"Saved chunk {i + 1} to {chunk_path}")


def process_noise_audio_files(input_wav_folder, output_wav_folder, columns_to_process):
    """
    Processes noise audio files and prints information for each file and column.
    
    Parameters:
    - input_wav_folder (str): Path to the folder containing the input .wav files.
    - output_wav_folder (str): Path to the folder where processed .wav files will be saved.
    - columns_to_process (list): List of column names to process.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_wav_folder, exist_ok=True)
    
    # Loop over each file in the input folder
    for root, _, files in os.walk(input_wav_folder):
        for file in files:
            if file.lower().endswith('.wav') and not file.startswith('.'):
                print(f"Processing file: {file}")
                file_path = os.path.join(root, file)
                audio_length = get_audio_length_in_milliseconds(file_path)
                # Nest a loop over each column
                new_filename = ""
                for column in columns_to_process:
                    print(f"Processing column: {column}")
                    # Placeholder for actual processing logic
                    if column == 'CLASSNAME':
                        new_filename += "noise-"
                    elif column == 'Reef':
                        print("Reef logic goes here")
                    elif column == 'Time of day':
                        print("Time of day logic goes here")
                    elif column == 'Breeding':
                        print("Breeding logic goes here")
                    elif column == 'Rank':
                        print("Rank logic goes here")
                    elif column == 'Interaction with':
                        print("Interaction with logic goes here")
                    elif column == 'LABELINFO (Optional)':
                        new_filename += "_"
                    elif column == 'ID':
                        random_number = np.random.randint(1000, 9999)
                        new_filename += f"{random_number}_"
                    elif column == 'YEAR':
                        new_filename += "2024_"
                    elif column == 'TAPENAME':
                        new_filename += "Noisetapename_"
                    elif column == 'START TIME (MS)':
                        new_filename += "0_"
                    elif column == 'END TIME (MS)':
                        new_filename += f"{audio_length}.wav"
                    else:
                        print(f"Unknown column: {column}")
                print(f"New filename: {new_filename}")
                # Save audio file with new filename
                destination_file = os.path.join(output_wav_folder, new_filename)
                shutil.copy(file_path, destination_file)
                print(f"File copied: {file_path} -> {destination_file}")


excel_file = "/Users/ferddei/Library/CloudStorage/GoogleDrive-fredericjohn.student@gmail.com/My Drive/1. Projects/6. Clown Fish Acoustics/ANIMAL-SPOT_file-name-structure.xlsx"
input_wav_folder = "/Users/ferddei/Library/CloudStorage/GoogleDrive-fredericjohn.student@gmail.com/My Drive/1. Projects/6. Clown Fish Acoustics/Clown_fish_data"
output_wav_folder = "/Volumes/InsightML/NAS/3_Lucia_Yllan/Clown_Fish_Acoustics/data/training_data/clown_fish_data_binary"

input_wav_folder_noise = "/Volumes/InsightML/NAS/3_Lucia_Yllan/Clown_Fish_Acoustics/data/noise"
output_wav_folder_noise = "/Volumes/InsightML/NAS/3_Lucia_Yllan/Clown_Fish_Acoustics/data/training_data/clown_fish_data_binary"
output_chunk_folder = "/Volumes/InsightML/NAS/3_Lucia_Yllan/Clown_Fish_Acoustics/data/noise_chunked"
run_on_files(input_wav_folder_noise, split_audio, [".wav"], 1000, output_chunk_folder)
process_call_audio_files(excel_file, input_wav_folder, output_wav_folder, columns_to_process)
process_noise_audio_files(output_chunk_folder, output_wav_folder_noise, columns_to_process)