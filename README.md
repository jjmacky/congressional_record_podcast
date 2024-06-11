# Overview
This project aims to automate the creation of a political news podcast based on the [Congressional Record](https://www.congress.gov/congressional-record), a daily record of U.S. Senate and House proceedings published by the U.S. Congress.

You can listen to a sample episode here: [Sample Episode](https://open.spotify.com/episode/4PaiU3ldCsrnJUZDdfWasP)

Spotify homepages:
- Senate Podcast: [Link](https://open.spotify.com/show/6kKhJJ4cCQXUhdmiqvsiAb)
- House Podcast: [Link](https://open.spotify.com/show/0BcXB54AisBnodAODcQdAF)

Note: Only a few sample episodes have been released as improvements are ongoing.

# Workflow
The automated workflow, developed in Python, follows these steps:
1. **Download the Data:** Retrieve the current day's Congressional Record in .zip format.
2. **Extract Files:** Unzip the folder, which contains N text files. The number of files varies based on the day's proceedings. The Congressional Record can be extensive, sometimes exceeding 150 pages in PDF format.
3. **Segment by Chamber:** Separate the text files into House and Senate categories based on their filenames.
4. **Filter Files:** Discard text files shorter than a specified word count (e.g., 150 words).
5. **Score Relevance:** Use GPT-4 to score the remaining files on political relevance and interest on a scale of 1 to 5.
6. **Summarize Content:** Iterate through the files, providing the current file and the first 100 words of the next file to GPT-4 for summarization, ensuring a smooth topic transition at the end.
7. **Create Intro and Outro:** Compile all summaries and use GPT-4 to generate an introductory and closing segment based on the concatenated set of summaries.
8. **Combine Summaries:** Merge all summarized files plus the intro and outro into a single document.
9. **Text-to-Speech (TTS):** Convert the combined text to speech using OpenAI's TTS service.
10. **Add Intro Music:** Add intro and outro music into the speech audio file, using a calculation to ensure audio ducking is synchronized correctly.

# Updates Needed
1. **Neutral Tone:** Adjust the prompting strategy to ensure summaries are neutral. Currently, summaries reflect the partisan tone of the speakers. For example, instead of saying, "Here is what Mitch McConnell said about border security," it says, "Mitch McConnell highlighted the problems with Democrats' border policy." The goal is to achieve a more neutral tone.
2. **Consolidate Topics:** Group summaries by topic to avoid repeated transitions. For instance, if gun control is discussed multiple times throughout the day, combine these discussions into a single segment. Current attempts using GPT-4 to categorize by topic have been unsuccessful and need refinement.
3. **Expand Context (Aspirational):** Integrate broader news reports by searching the web for additional context on each topic discussed in the podcast.
4. **Code Cleanup:** Improve the code's structure and readability for better maintainability and performance.
