newsworthiness_prompt = f'''
    Please review the following content from the Congressional Record and score it according to this rubric. Only return the score like this "{{"score": 3}}" with no additional descrption.
    
    Scoring Rubric: Congressional Record Newsworthiness
    Score 1: Minimal Interest

    Criteria: Content is procedural or routine with little to no impact on current political events or legislation.
    Example: Routine announcements, minor procedural changes.
    Score 2: Low Interest

    Criteria: Content includes general discussions or minor legislative activities that have a low impact on current politics or public policy.
    Example: Early-stage discussions of legislation, minor committee reports.
    Score 3: Moderate Interest

    Criteria: Content covers developing stories, moderate legislative actions, or issues that have a potential to influence public policy or political discourse.
    Example: Active committee hearings, moderate policy debates, or updates on legislation.
    Score 4: High Interest

    Criteria: Content pertains to major legislative actions, significant political events, or debates that have a substantial impact on national policy or the political landscape.
    Example: Major bill discussions, significant political appointments, or landmark committee findings.
    Score 5: Essential Interest

    Criteria: Content is critical for understanding current Congress, including major legislative decisions, high-profile political events, or any urgent matters that immediately affect governance, policy, or public welfare.
    Example: Passage of major legislation, significant political developments, or emergency actions.
    
    Additional Considerations to help with scoring (for context only, do not add in response):
    Historical Context: How does the content fit within the larger historical and political context?
    Public Impact: What is the potential or actual impact on the public?
    Urgency: Is the information timely and urgent?
    Political Significance: Does it involve major political figures or pivotal political movements?
    Legislative Gravity: Is it about significant changes in law or policy?

    Only return the score like this "{{"score": 3}}" with no additional descrption. Example output: {{"score": 3}}. 
    '''

summarization_prompt = f'''
Your task is to create a podcast script summarizing text from the Congressional Record. This script will form part of a larger podcast dedicated to Congressional proceedings, aimed at a politically savvy audience. The summary should be engaging, informative, and presented in a neutral, objective manner. Use the tone of the New York Times.

Instructions:

1. Start with a Specific Transition: Begin with a brief, relevant transition statement, such as "In today's healthcare discussions..."

2. Neutral and Factual Reporting: Summarize the content in a way that focuses on factual reporting. Use direct quotes and clear attribution to congresspeople for any claims or statements made. Preface quotes with "quote."

3. Avoid Biased Language and Tone: Do not use language that implies value judgments or adopt the tone of the congressional proceedings. Your language should be neutral and objective.

4. Balanced Representation of Viewpoints: Ensure that your summary provides a balanced representation of all viewpoints presented in the text, without favoring any particular perspective.

5. Include Contextual Information: Where relevant, include contextual information to enhance understanding, but ensure it is clearly distinct from the direct reporting.

6. Engagement without Sensationalism: While keeping the summary engaging, avoid sensationalizing the content. Focus on the key developments and implications of the discussions.

7. No Extraneous Elements: Do not add speaker identifiers, script cues, or commentary about the script instructions.

8. Regular Reviews for Neutrality and Factuality: Be prepared to regularly review and adjust your script to ensure ongoing neutrality and adherence to factual reporting.

9. Outcome and Details: Include important details such as the outcome of discussions, the status of bills, and schedules for future discussions. Give details about the end result. Did the bill pass or fail? Was it merely introduced? When will discussions resume?

'''

editing_prompt = f'''
    For the below text:
    REMOVE speaker identifiers (ex. "Host") and cues (ex. "[Slight pause]" or "[Introductory Music]").
    REMOVE any podcast introduction language.
    CREATE an outro at the end of the script.
    Improve the flow with transitions.
    DO NOT summarize or remove any text. Do NOT change the language of the summary, only add an intro, transitions, and an outro. Your update should include the original text in full.
    You should return a file that is at least as long ast the original because you are not removing content, you are only adding.
    You should return the script ready to read as is (every word will be read) so it should only contain text meant to be read outloud.
    '''

editing_prompt_reinforcement = f'''
    For the above text:
    REMOVE speaker identifiers (ex. "Host") and cues (ex. "[Slight pause]" or "[Introductory Music]" or "Transitional statement").
    REMOVE any podcast introduction language.
    CREATE an outro at the end of the script.
    Improve the flow with transitions.
    DO NOT summarize or remove any text. Do NOT change the language of the summary, only add an intro, transitions, and an outro. Your update should include the original text in full.
    You should return a file that is at least as long ast the original because your focus is adding an intro, transitions, and an outro.
    You should return the script ready to read as is (every word will be read) so it should only contain text meant to be read outloud.
 '''


intro_outro_prompt = f'''
    Write a short (1-3 sentences) intro and outro for this podcast in JSON format.

    Here is an example:

    {{
        "intro":"Welcome to "The Congressional Record for the House of Representatives" podcast, where we delve into the latest activities and discussions held within the hallowed halls of the U.S. House of Representatives. In this episode, we present the highlights from several new proposed pieces of legislation, a fight to see who will be the next Speaker of the House, a resolution to help fight inflation, and much more.",

        "outro":"Thank you for joining us on "The Congressional Record for the House of Representatives."
    }}
'''

short_episode_prompt = f'''
    Say casually in the intro that today's episode is short and keep your own intro short as well. Keep it casual. We don't want to get people too excited when there isn't much content.
'''

terms_dictionary = f'''
    Rep = Representative; H.R. = House of Representatives H. Res. = House Resolution; Bill S. = Senate Bill
'''

previous_summary_prompt = f'''
    Here is the previous podcast topic. If it says "This is the first topic" then the Congressional Record Text you're summarizing is the first for today's podcast. Therefore at the start of your summary say something like, "To get us started..." or "Today we're starting off with..." Or something similar. Do NOT add a full intro, just add a short phrase about getting started.
    Otherwise, examine the previous topic and the new Congressional Record text to be summarized and create a smooth transition at the top of the Congressional Record text you've summarized. If the previous topic and the new Congressional Record topic are about the same or similar subject then the transition should be minimal and focus on an extension of the preivous topic. If it is a new topic then transition with language like:
    "Moving on to...", "Changing topics to...", "Turning our attention to...", "Pivoting to...", "Shifting focus to...", "In other developments..." or similar language.
    '''

themeing_prompt = f'''
Task: Group the content from the U.S. Congressional Record, taken from the House or Senate floor discussions, into thematic categories. Create a JSON list with each file included once, based on its primary theme.

Data: You will work with the first 1,500 characters from a selection of articles.

Thematic Categories:
Use straightforward and recognizable theme titles for categorization. Some examples include:
"Veterans' Affairs"
"Honoring Civil Rights Leaders"
"Improving U.S. Healthcare policy"

Instructions:
1. Identify the Primary Theme: For each file, determine the most significant theme. If a file covers multiple topics, select the most prominent one for categorization.
2. JSON Format: Present the data in a JSON structure. Each entry should state the theme and include the file paths that fall under that theme.
3. Logical Order: Arrange the themes in an order that would flow well in a podcast format, considering the transition between different topics.
[
    {{
       "theme": "Veterans' Affairs",
       "files": ["../Episodes/CREC-2023-11-28/text/CREC-2023-11-28-pt1-PgH5937-8.txt", "../Episodes/CREC-2023-11-28/text/CREC-2023-11-28-pt1-PgH5939.txt", "../Episodes/CREC-2023-11-28/text/CREC-2023-11-28-pt1-PgH5942.txt"]
    }},
    {{
        "theme": "Improving U.S. Healthcare policy"
        "files": ["../Episodes/CREC-2023-05-22/House/text/CREC-2023-05-22-pt1-PgH2474.txt", "../Episodes/CREC-2023-05-22/House/text/CREC-2023-05-22-pt1-PgH2479.txt", "../Episodes/CREC-2023-05-22/House/text/CREC-2023-05-22-pt1-PgH2502-5.txt"]
    }}, [other JSON entries]
]
'''