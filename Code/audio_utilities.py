import os
from pydub import AudioSegment
from openai import OpenAI
from text_utilities import read_script, split_text


def synthesize_speech(text_chunks, api_key, output_directory):
    """
    For each text chunk, synthesize speech and save the audio file in the specified directory.
    Returns the list of audio file paths.
    """
    client = OpenAI(api_key=api_key)
    audio_paths = []
    
    # Ensure output directory exists, create if it doesn't
    os.makedirs(output_directory, exist_ok=True)

    for i, chunk in enumerate(text_chunks, start=1):
        try:
            # Synthesize speech for the chunk
            response = client.audio.speech.create(
              model="tts-1-hd",
              voice="alloy",
              input=chunk  # Ensure to use 'chunk' as the input text
            )
            # Define a unique filename for each audio chunk and include the output directory in the path
            audio_file_name = f"chunk_{i}.mp3"
            audio_path = os.path.join(output_directory, audio_file_name)
            audio_paths.append(audio_path)

            # Stream the response to file in the specified directory
            with open(audio_path, "wb") as audio_file:
                audio_file.write(response.content)

            print(F"{audio_file_name} creted.")
        except Exception as e:
            print(f"Error synthesizing chunk {i}: {e}")

    return audio_paths


def combine_audio_files(audio_paths, final_audio_path):
    """
    Combine all the audio files into one final audio file using PyDub.
    
    :param audio_paths: List of paths to the audio files.
    :param final_audio_path: Path for the output combined audio file.
    """
    combined = AudioSegment.empty()  # Create an empty AudioSegment

    # Loop through the list of audio file paths and concatenate them
    for path in audio_paths:
        # Load the audio file
        audio = AudioSegment.from_file(path)
        combined += audio  # Append audio to the combined AudioSegment

    # Export the combined audio files into one file
    combined.export(final_audio_path, format="mp3")


def create_intro(intro_music, start_fade_in, end_fade_in, start_fade_out, end_fade_out, start_gain, mid_gain, end_gain, total_duration):
    """
    Apply custom fading for intro.
    """
    # Apply constant gain to the whole audio then apply fades
    intro = intro_music + start_gain
    intro = intro.fade(from_gain=start_gain, to_gain=mid_gain, start=start_fade_in, end=end_fade_in) # Apply the linear fade in
    intro = intro.fade(from_gain=mid_gain, to_gain=end_gain, start=start_fade_out, end=end_fade_out) # Apply the linear fade out
    intro = intro[:total_duration] # Trim the audio to the total_duration
    return intro


def create_outro(outro_music, total_duration, mid_gain):
    """
    Apply custom fading for outro.
    """
    outro = outro_music.fade(from_gain=mid_gain, to_gain=-1, start=15000, end=20000)
    outro = outro[:total_duration]
    outro = outro.fade_in(duration=5000)
    outro = outro.fade_out(duration=5000)
    return outro


def mix(intro, outro, speaking):
    speaking = AudioSegment.silent(duration=7000) + speaking
    mix_speaking_and_intro = speaking.overlay(intro)
    outro_overlay_position = len(mix_speaking_and_intro) - 15000
    mix_speaking_and_intro += AudioSegment.silent(duration=15000)
    final_mix =  mix_speaking_and_intro.overlay(outro, position=outro_overlay_position)
    return final_mix


def create_spoken_audio(episode_manager, api_key):
    script = read_script(file_path=episode_manager.directories['final_script_path'])
    text_chunks = split_text(text = script, max_length=4096)
    audio_paths = synthesize_speech(text_chunks, api_key, output_directory=episode_manager.directories['todays_audio_directory'])
    combine_audio_files(audio_paths, final_audio_path=episode_manager.directories['spoken_audio_path'])