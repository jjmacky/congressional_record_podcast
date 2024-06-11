import os
import re
import json
import shutil
from text_utilities import extract_text_from_files
from config import episodes_directory, todays_extension, chamber_to_search_string

class EpisodeManager:
    static_audio_directory = "../Audio"

    def __init__(self, chamber):
        self.chamber = chamber
        self.todays_episode_directory = os.path.join(episodes_directory, todays_extension)
        self.directories = self.setup_directories()

    def setup_directories(self):
        todays_chamber_directory = os.path.join(self.todays_episode_directory, self.chamber) # Define the base directory for the chamber
                                            
        # Ensure the base directory exists
        if not os.path.exists(todays_chamber_directory):
            os.makedirs(todays_chamber_directory)

        # Define other directories relative to the base directory
        directories = {
            'todays_html_directory': os.path.join(self.todays_episode_directory, "html") ,
            'todays_text_directory': os.path.join(todays_chamber_directory, "text"),
            'chamber_directory': todays_chamber_directory,
            'todays_json_scores_path': os.path.join(todays_chamber_directory, "scores.json"),
            'todays_themes_json_path': os.path.join(todays_chamber_directory, "theme_response.json"),
            'todays_concat_summary_path': os.path.join(todays_chamber_directory, "concatenated_summary.txt"),
            'todays_script_in_out_json_path': os.path.join(todays_chamber_directory, "script_intro_and_outro.json"),
            'final_script_path': os.path.join(todays_chamber_directory, "final_script.txt"),
            'todays_audio_directory': os.path.join(todays_chamber_directory, "audio"),
            'spoken_audio_path': os.path.join(todays_chamber_directory, "spoken_audio.mp3"),
            'todays_final_podcast_path': os.path.join(todays_chamber_directory, "final_podcast_with_music.mp3")
        }
        return directories

    def get_files_in_directory(self, directory_path):
        all_files = []
        for item in os.listdir(directory_path):
            full_path = os.path.join(directory_path, item)
            if os.path.isfile(full_path):
                all_files.append(full_path)
        return all_files


    def custom_sort_key(self, filename):
        """
        Custom sort function to handle filenames with numerical suffixes.
        
        :param filename: The filename to process.
        :return: A tuple representing the sorting key.
        """
        # Regular expression to match the base filename and the numerical suffix
        match = re.match(r"(.*?)(-\d+)?(\.htm)$", filename)
        if match:
            base, number, ext = match.groups()
            number = int(number[1:]) if number else 0  # Convert number part to integer, default to 0 if not present
            return base, number, ext
        return filename, 0, ''  # Default return value for non-matching filenames


    def find_and_sort_files(self, directory, file_type):
        """
        Find and sort .htm files with a given search string in the filename within the specified directory.
        
        :param directory: Directory to search within.
        :param chamber: Chamber name to determine the search string.
        """
        # Get the search string for the given chamber
        search_string = chamber_to_search_string[self.chamber]
        postfix = {"web":".htm", "text":".txt"}
        sorted_files = []

        # Walk through the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(postfix[file_type]) and search_string in file:
                    sorted_files.append(os.path.join(root, file))

        # Sort the list of filenames using the custom sort key
        sorted_files.sort(key=self.custom_sort_key)
        return sorted_files  # Return the sorted list of file paths


    def read_scores(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
        

    def prepare_files_for_processing(self):
        print("Extracting files...")
        file_list = self.get_files_in_directory(self.directories['todays_html_directory'])
        extract_text_from_files(file_list, self.directories['todays_text_directory'])
    

    def delete_files(self, file_list, directory_list):
        for file in file_list:
            try:
                os.remove(file)
                print(f"Removed {file}")
            except Exception as e:
                print(f"Could not remove {file}: {e}")

        for directory in directory_list:
            try:
                shutil.rmtree(directory)
                print(f"Removed {directory}")
            except Exception as e:
                print(f"Could not remove {directory}: {e}")


    def cleanup_local_files(self):    
        # Delete unneded files
        file_list = [
            self.directories['todays_json_scores_path'],
            self.directories['todays_concat_summary_path'],
            self.directories['todays_script_in_out_json_path'],
            self.directories['spoken_audio_path'],
        ]

        directory_list = [
            self.directories['todays_audio_directory'],
            self.directories['todays_text_directory'],
        ]
        
        self.delete_files(file_list, directory_list)

    def cleanup_global_files(self):
        # Delete unneded files
        file_list = [
            os.path.join(self.todays_episode_directory, "dip.xml"),
            os.path.join(self.todays_episode_directory, "mods.xml"),
            os.path.join(self.todays_episode_directory, "premis.xml")
        ]

        directory_list = [
            self.directories['todays_html_directory'],
            os.path.join(self.todays_episode_directory, "pdf"),
        ]

        self.delete_files(file_list, directory_list)