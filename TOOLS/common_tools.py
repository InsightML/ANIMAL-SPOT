import os

def run_on_files(folder_path, func, file_extensions=None, *args, **kwargs):
    """
    Run a specified function on all files in a directory with given file extensions.

    Parameters:
    folder_path (str): The path to the directory containing the files.
    func (callable): The function to run on each file. It should accept a file path as the first argument.
    file_extensions (list, optional): List of file extensions to filter by. If None, all files are processed.
    *args: Additional positional arguments to pass to the function. (e.g., arg1, arg2)
    **kwargs: Additional keyword arguments to pass to the function. (e.g., key1=value1, key2=value2)

    Returns:
    list: A list of tuples, where each tuple contains the filename and the values returned by the function.
    """
    if file_extensions is None:
        file_extensions = []

    results = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if not file_extensions or file.lower().endswith(tuple(file_extensions)):
                file_path = os.path.join(root, file)
                try:
                    result = func(file_path, *args, **kwargs)
                    results.append((file, result))
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
    
    return results
