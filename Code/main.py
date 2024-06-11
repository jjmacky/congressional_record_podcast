import os
from file_utilities import EpisodeManager
from podcast_processing import generate_podcast_script, create_podcast
from network_utilities import download_and_unzip
from config import todays_url, episodes_directory

# Set OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

def download_files_once():
    download_and_unzip(todays_url, extract_to=episodes_directory)

def main(chamber):
    episode_manager = EpisodeManager(chamber)
    
    episode_manager.prepare_files_for_processing()
    generate_podcast_script(episode_manager)
    create_podcast(episode_manager)
    #episode_manager.cleanup_local_files()

    return episode_manager

if __name__ == "__main__":
    # Step 1: Download files once
    #download_files_once()

    # Step 2: Process each chamber
    episode_managers = [main(chamber) for chamber in ['House', 'Senate']]

    # Step 3: Cleanup after all chambers have been processed
    #for manager in episode_managers:
     #   manager.cleanup_global_files()
