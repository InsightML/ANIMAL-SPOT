from pydub import AudioSegment
from common_tools import run_on_files
import matplotlib.pyplot as plt
import numpy as np

def get_audio_length_in_milliseconds(audio_file_path):
    """
    This function reads an audio file and returns its length in milliseconds.
    
    Parameters:
    audio_file_path (str): Path to the audio file.
    
    Returns:
    int: Length of the audio file in milliseconds.
    """
    # Load the audio file
    audio = AudioSegment.from_file(audio_file_path)
    
    # Get the length in milliseconds
    length_in_milliseconds = len(audio)
    
    return length_in_milliseconds

# Calculate the average length of all audio files in a directory
def get_average_audio_length(folder_path):
    """
    This function calculates the average length of all audio files in a directory.
    
    Parameters:
    folder_path (str): Path to the directory containing the audio files.
    
    Returns:
    float: Average length of the audio files in milliseconds.
    """
    # Get the lengths of all audio files in the directory
    lengths = run_on_files(folder_path, get_audio_length_in_milliseconds, [".wav"])
    
    # Calculate the average length
    total_length = sum(length for _, length in lengths)
    num_files = len(lengths)
    average_length = total_length / num_files if num_files > 0 else 0
    
    return average_length, lengths

def plot_audio_lengths(folder_path):
    """
    This function plots the lengths of the audio files, along with the average length and standard deviation.
    
    Parameters:
    folder_path (str): Path to the directory containing the audio files.
    """
    average_length, lengths = get_average_audio_length(folder_path)
    lengths_in_ms = [length for _, length in lengths]
    
    # Calculate standard deviation
    std_dev = np.std(lengths_in_ms)
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(lengths_in_ms, label='Audio Lengths (ms)')
    plt.axhline(y=average_length, color='r', linestyle='-', label=f'Average Length: {average_length:.2f} ms')
    plt.axhline(y=average_length + std_dev, color='g', linestyle='--', label=f'Std Dev: {std_dev:.2f} ms')
    plt.axhline(y=average_length - std_dev, color='g', linestyle='--')
    plt.xlabel('Audio File Index')
    plt.ylabel('Length (ms)')
    plt.title('Audio File Lengths')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Example usage
    folder_path = "/Volumes/InsightML/NAS/3_Lucia_Yllan/Clown_Fish_Acoustics/data/training_data/clown_fish_data_binary"
    average_length, _ = get_average_audio_length(folder_path)
    plot_audio_lengths(folder_path)
    print(f"Average audio length: {average_length} milliseconds")
