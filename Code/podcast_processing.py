import os
from pydub import AudioSegment
from config import api_key
from audio_utilities import create_spoken_audio, create_intro, create_outro, mix
from openai_utilities import score_text_files_in_directory, create_summary_from_high_scores, create_script_intro_and_outro
from text_utilities import create_podcast_script
from file_utilities import EpisodeManager

EpisodeManager.static_audio_directory

def generate_podcast_script(episode_manager):
    #score_text_files_in_directory(episode_manager, api_key = api_key)
    create_summary_from_high_scores(episode_manager, api_key=api_key)   
    create_script_intro_and_outro(episode_manager, api_key=api_key)
    create_podcast_script(episode_manager)


def create_podcast(episode_manager):
    create_spoken_audio(episode_manager, api_key=api_key)

    # Load audio
    intro_music = AudioSegment.from_file(os.path.join(EpisodeManager.static_audio_directory, "Sam River - World News.mp3"))
    outro_music = AudioSegment.from_file(os.path.join(EpisodeManager.static_audio_directory, "Sam River - World News.mp3"))
    speaking = AudioSegment.from_file(os.path.join(episode_manager.directories['spoken_audio_path']))

    # Apply custom fade function and specify total duration
    intro = create_intro(
        intro_music=intro_music,
        start_fade_in=5000,  # start of volume decrease fade
        end_fade_in=7000,  # end volume decrease fade
        start_fade_out=15000,  # start fade to 0
        end_fade_out=20000,  # end of fade to zero
        start_gain=5,  # original volume
        mid_gain=-12,  # reduced volume
        end_gain=-60,  # near silence
        total_duration=21000  # end track
    )
    outro = create_outro(outro_music=outro_music, total_duration=30000, mid_gain=-12)
    final_podcast_with_music = mix(intro=intro, outro=outro, speaking=speaking)

    # Export the final podcast
    final_podcast_with_music.export(episode_manager.directories['todays_final_podcast_path'], format="mp3")