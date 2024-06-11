import os
import json
from bs4 import BeautifulSoup

def extract_text_to_file(source_file_path, target_directory):
    """
    Extracts text from an HTML file and saves it to a new file in the target directory.

    :param source_file_path: The file path of the source HTML file.
    :param target_directory: The directory where the extracted text file will be saved.
    """

    # Ensure the target directory exists, create if not
    os.makedirs(target_directory, exist_ok=True)

    # Extract the filename without extension and construct new filename
    base_filename = os.path.basename(source_file_path)
    new_filename = os.path.splitext(base_filename)[0] + ".txt"
    target_file_path = os.path.join(target_directory, new_filename)

    # Read the source HTML file and extract text
    with open(source_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        text_content = soup.get_text(separator='\n', strip=True)

    # Write the extracted text to the new file
    with open(target_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text_content)

    print(f"Extracted text from {source_file_path} to {target_file_path}")


def extract_text_from_files(file_list, target_directory):
    """
    Takes a list of HTML file paths and extracts the text of each one, saving it to a new file in the target directory.

    :param file_list: List of HTML file paths.
    :param target_directory: Directory where the text files will be saved.
    """
    # Ensure the target directory exists, if not create it
    os.makedirs(target_directory, exist_ok=True)

    for file_path in file_list:
        try:
            # Extract the text to a new file in the target directory
            extract_text_to_file(file_path, target_directory)
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")


def create_podcast_script(episode_manager):
    # Read the intro and outro from the JSON file
    with open(episode_manager.directories['todays_script_in_out_json_path'], 'r', encoding='utf-8') as json_file:
        script_parts = json.load(json_file)
        intro = script_parts['intro']
        outro = script_parts['outro']
    
    # Read the main content of the podcast
    with open(episode_manager.directories['todays_concat_summary_path'], 'r', encoding='utf-8') as file:
        main_content = file.read()
    
    # Concatenate the intro, main content, and outro
    full_script = f"{intro}\n\n{main_content}\n\n{outro}"
    
    # Save the final result to final_script.txt
    with open(episode_manager.directories['final_script_path'], 'w', encoding='utf-8') as final_file:
        final_file.write(full_script)
    
    print(f"Script saved to {episode_manager.directories['final_script_path']}")


def read_script(file_path='final_script.txt'):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def split_text(text, max_length=4096):
    """
    Split the text into chunks, each with a maximum length of `max_length`.
    Tries to split at the end of lines or sentences for better coherence.
    """
    chunks = []
    while text:
        # Find the nearest earlier end-of-line or sentence to split at
        split_at = text.rfind('\n', 0, max_length) + 1 if '\n' in text[0:max_length] else text.rfind('. ', 0, max_length) + 1
        if split_at <= 0:  # No end-of-line or sentence end found; split at max_length
            split_at = max_length
        chunk, text = text[:split_at], text[split_at:]
        chunks.append(chunk.strip())
    return chunks