import pandas as pd
import shutil
import os

excel_file = "/Users/ferddei/Library/CloudStorage/GoogleDrive-fredericjohn.student@gmail.com/My Drive/1. Projects/6. Clown Fish Acoustics/ANIMAL-SPOT_file-name-structure.xlsx"
input_wav_folder = "/Users/ferddei/Library/CloudStorage/GoogleDrive-fredericjohn.student@gmail.com/My Drive/1. Projects/6. Clown Fish Acoustics/Clown_fish_data"
output_wav_folder = "/Volumes/InsightML/NAS/3_Lucia_Yllan/Clown_Fish_Acoustics/data/processed_wavs"

missing_wav_files = []
log_file = "/Volumes/InsightML/NAS/3_Lucia_Yllan/Clown_Fish_Acoustics/logs/wav-renamer.log"

processed_file_count = 0

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
    
    value = str(value).replace(" ", "").replace("_", "-").replace(".", "-")
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
    source_file = os.path.join(input_wav_folder, filename)
    destination_file = os.path.join(output_wav_folder, string)

    try:
        shutil.copy(source_file, destination_file)
        print(f"File copied: {filename} -> {string}")
        processed_file_count += 1
    except FileNotFoundError:
        print(f"File not found: {filename}")
        missing_wav_files.append(filename)
        continue
    except TypeError as e:
        print(f"TypeError for file {filename}: {e}")
        continue

print(f"Missing files: {missing_wav_files}")
print(f"Processed files: {processed_file_count}")
print("Upading log file...")
with open(log_file, "w") as log:
    log.write(f"Missing files: {missing_wav_files} \n")
    log.write(f"Processed files: {processed_file_count} \n")
