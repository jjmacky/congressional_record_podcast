import os
import json
from openai import OpenAI
from prompts import newsworthiness_prompt, summarization_prompt, previous_summary_prompt, themeing_prompt, intro_outro_prompt, short_episode_prompt # Import prompts
from file_utilities import EpisodeManager
from config import chamber_to_search_string, chamber_to_podcast_title
'''
Define variables for this module
'''
summary_percent = 0.25 # How long (in %) should the summary be relative to the original article?
max_summary_word_count = 3500 # Set max length of article summary


'''
Define functions
'''
def get_newsworthy_score(content, api_key):
    client = OpenAI(api_key=api_key)
    
    api_content = f'''
        {newsworthiness_prompt}

        BEGINNING OF CONTENT:

        {content}

        END OF CONTENT
    '''

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON about newsworthiness."},
            {"role": "user", "content": api_content}
        ]
    )
    # Assuming the response is a JSON string, parse it into a dictionary
    try:
        response_data = json.loads(completion.choices[0].message.content)
        return response_data  # Now this should be a dictionary
    except json.JSONDecodeError:
        print("Failed to parse the response as JSON")
        return {}


def score_text_files_in_directory(episode_manager, api_key):
    directory = episode_manager.directories['todays_text_directory']
    print("Sorting files...")
    sorted_files_list = episode_manager.find_and_sort_files(directory, "text")
    auto_importance_length = 5000 # Articles of this length are automatically scored high
    all_scores = []  # List to hold all score data

    # Loop over all files in the directory
    for file_path in sorted_files_list:
        
        criteria = (
            os.path.isfile(file_path) and 
            "summary" not in file_path and 
            chamber_to_search_string[episode_manager.chamber] in file_path
        )

        # Check if it's a file and not a subdirectory
        if criteria:
            # Read the content of the file
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Print status
            print(f"Scoring Content from {file_path}...")

            # Calculate the length of content in number of words
            word_count = len(content.split())

            if word_count >= auto_importance_length:
                # Manually create a JSON entry for excessively long files
                score_json = {"score": 4} 
            else:
                # Get newsworthiness score for shorter files
                score_json = get_newsworthy_score(content, api_key)

            # Append the file name (with directory) and word count to the score JSON
            score_json.update({'file': file_path, 'word_count': word_count})

            # Append the score JSON to the list of all scores
            all_scores.append(score_json)

    # Save all_scores JSON in the specified directory
    scores_path = episode_manager.directories['todays_json_scores_path']
    with open(scores_path, 'w', encoding='utf-8') as f:
        json.dump(all_scores, f, ensure_ascii=False, indent=4)

    print(f"Scores saved to {scores_path}")
    return all_scores


def prepare_thematic_json(scores):
    chamber_directory = "../Episodes/CREC-2023-05-22/House"
    thematic_json = []

    for record in scores:
        if record.get('score', 0) in [3, 4, 5]:
            file_path = record.get('file', '')
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read(1500)  # Read only the first 1000 characters or the full article if shorter
            thematic_json.append({
                "file": file_path,
                "file_content": file_content
            })

    # Save the thematic JSON data to a file
    prepped_themes_path = os.path.join(chamber_directory, "prepped_themes.json")
    with open(prepped_themes_path, 'w', encoding='utf-8') as file:
        json.dump(thematic_json, file, ensure_ascii=False, indent=4)

    print(f"Thematic JSON file prepared and saved to {prepped_themes_path}.")
    return thematic_json



def get_themes(episode_manager, thematic_json, api_key):
    client = OpenAI(api_key=api_key)
    
    api_content = f'''
        {themeing_prompt}

        BEGIN FILE LIST. PLESE RETURN THEMATIC JSON BASED ON THE BELOW.
        {thematic_json}
        END FILE LIST. PLESE RETURN THEMATIC JSON BASED ON THE ABOVE.

        {themeing_prompt}
    '''

    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON about themes."},
            {"role": "user", "content": api_content}
        ]
    )

    try:
        response_data = json.loads(completion.choices[0].message.content)
        # Save response to a file
        file_path = episode_manager.directories["todays_themes_json_path"]
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(response_data, file, ensure_ascii=False, indent=4)
        print(f"Themes response successfully received and saved to {file_path}")
        return response_data  # Now this should be a dictionary
    except json.JSONDecodeError:
        print("Failed to parse the response as JSON")
        return {}


def summarize_by_theme(themes_response, api_key):
    summaries = {}
    previous_summary = "This is the first topic."  # To keep track of the previous summary

    # Extract the list of themes from the response
    if 'themes' in themes_response:
        themes = themes_response['themes']
    else:
        raise ValueError("Invalid 'themes_response' format. Expected a dictionary with a 'themes' key.")

    for theme in themes:
        combined_text = ""
        total_word_count = 0

        print(f"Summarizing {theme['theme']}...")

        if 'files' not in theme:
            raise ValueError("Each theme dictionary must have a 'files' key.")

        for file_path in theme['files']:
            # Check if the file exists
            if not os.path.isfile(file_path):
                print(f"File not found: {file_path}. Skipping.")
                continue  # Skip this file and continue with the next one

            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                combined_text += file_content + "\n\n"
                total_word_count += len(file_content.split())

        target_word_count = min(max(int(total_word_count * summary_percent), 1), max_summary_word_count)

        # Generate summary using the previous summary for context
        summary = summarize_text(combined_text, previous_summary, target_word_count, api_key)
        summaries[theme.get('theme', 'Unnamed Theme')] = summary

        previous_summary = summary

    return summaries


def summarize_text(text, previous_summary, target_word_count, api_key):
    """
    Summarize the provided text using GPT-4.
    """
    client = OpenAI(api_key=api_key)

    api_content = f'''
        {summarization_prompt}
        
        {previous_summary_prompt}
        BEGIN PREVIOUS PODCAST TOPIC. DO NOT SUMMARIZE. CONTEXT ONLY.
        {previous_summary}
        END PREVIOUS PODCAST TOPIC.

        BEGIN NEXT CONGRESSIONAL RECORD PODCAST TOPIC. PLESE SUMMARIZE:
        {text}
        END CONGRESSIONAL PODCAST TOPIC. PLEASE SUMMARIZE THE ABOVE AS INSTRUCTED.

        {summarization_prompt}
        The summary script should be about {target_word_count} words long. 
    '''
    try:
        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are a neutral, measured news script writer like the New York Times."},
                {"role": "user", "content": api_content}
            ]
        )
        return completion.choices[0].message.content # Extract the summary text
    except Exception as e:
        print("Error during API call:", e)
        return "An error occurred."

def combine_themes_into_script(theme_summaries):
    script = ""
    for theme, summary in theme_summaries.items():
        # Add the summary with some transition or introduction if needed
        script += f"{summary}\n\n"  # Add extra newlines for separation
    return script

def create_summary_from_high_scores(episode_manager, api_key):
    scores = episode_manager.read_scores(episode_manager.directories['todays_json_scores_path'])
    thematic_json = prepare_thematic_json(scores) # Returns JSON file to send to API for theme grouping
    themes = get_themes(episode_manager, thematic_json, api_key) # Returns JSON file with theme and associated files
    theme_summaries = summarize_by_theme(themes, api_key)
    script = combine_themes_into_script(theme_summaries)

    # Save the script to the file
    concatenated_summary_path = episode_manager.directories['todays_concat_summary_path']
    with open(concatenated_summary_path, 'w', encoding='utf-8') as file:
        file.write(script)

    return script


def create_script_intro_and_outro(episode_manager, api_key):
    """
    Read the text from the provided file path, send the combined summaries to OpenAI, and get a response.
    """
    client = OpenAI(api_key=api_key)
    
    # Read the text from the provided file path
    with open(episode_manager.directories['todays_concat_summary_path'], 'r', encoding='utf-8') as file:
        summary = file.read()

    word_count = len(summary.split())
    special_messages = []

    # Define conditions and messages in a list or dictionary
    conditions = [
        (word_count < 1000, short_episode_prompt),
    ]

    # Check each condition
    for condition, message in conditions:
        if condition:
            special_messages.append(message)

    # Construct the prompt
    special_text = '\n'.join(special_messages)
    prompt = f'''
        {intro_outro_prompt}
        The name of the podcast is: {chamber_to_podcast_title[episode_manager.chamber]}
        START OF PODCAST TEXT:
        "{summary}"
        END OF PODCAST TEXT
        The name of the podcast is: {chamber_to_podcast_title[episode_manager.chamber]}
        {intro_outro_prompt}
        {special_text}
    '''
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a news script editor."},
                {"role": "user", "content": prompt}
            ]
        )
        intro_and_outro_text = completion.choices[0].message.content 

        # Define the path of the file where you want to save the script
        intro_and_outro_path = episode_manager.directories['todays_script_in_out_json_path'] # Update with your desired file path and name

        # Open the file in write mode and write the final_script_text to it
        with open(intro_and_outro_path, 'w', encoding='utf-8') as file:
            file.write(intro_and_outro_text )  # Write the text to the file
        
        # Optional: return the path to the file or the text itself
        return intro_and_outro_path
    except Exception as e:
        print("Error during API call:", e)
        return "An error occurred."