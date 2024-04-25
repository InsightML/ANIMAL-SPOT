import pandas as pd
import shutil
import os

excel_file = "C:\\Users\\JackL\\Downloads\\ANIMAL-SPOT_file-name-structure.xlsx"
input_wav_folder = "C:\\Users\\JackL\\Downloads\\6. Clown Fish Acoustics-20240417T132045Z-001\\6. Clown Fish Acoustics\\Clown_fish_data"
output_wav_folder = "output"

if not os.path.exists(output_wav_folder):
    os.makedirs(output_wav_folder)

df = pd.read_excel(excel_file, sheet_name='Data')

columns_to_process = ['CLASSNAME', 'Reef', 'Time of day', 'Breeding', 'Rank', 
                      'Interaction with', 'LABELINFO (Optional)', 'ID', 'YEAR', 
                      'TAPENAME', 'START TIME (MS)', 'END TIME (MS)']

def clean_and_concatenate(value, delimiter):
    if pd.isnull(value):
        return ""
    
    if isinstance(value, int):
        return f"{value}{delimiter}"
    
    value = str(value).replace(" ", "").replace("_", "-")
    return f"{value}{delimiter}"

for index, row in df.iterrows():
    cleaned_values = []

    after_info = False
    
    for col in columns_to_process:
        if col == 'LABELINFO (Optional)' or after_info:
            cleaned_values.append(clean_and_concatenate(row[col], "_"))
            after_info = True
        else:
            cleaned_values.append(clean_and_concatenate(row[col], "-"))
    
    string = "".join(cleaned_values)
    string = string.rstrip("-_")
    string = f"{string}.wav"
    filename = row['FILENAME']
    source_file = f"{input_wav_folder}\\{filename}"
    destination_file = f"{output_wav_folder}\\{string}"

    try:
        shutil.copy(source_file, destination_file)
        print(f"File copied: {source_file} -> {destination_file}")
    except FileNotFoundError:
        print(f"File not found: {source_file}")
        continue