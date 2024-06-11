import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Access the OPENAI_API_KEY
api_key = os.getenv('OPENAI_API_KEY')

episodes_directory = "../Episodes"
#todays_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
todays_date = "2023-05-22"

todays_extension = "CREC-" + todays_date

todays_url = f"https://www.govinfo.gov/content/pkg/{todays_extension}.zip"

chamber_to_search_string = {
    'House': 'PgH',
    'Senate': 'PgS',
}

chamber_to_podcast_title = {
    'House': "The Congressional Record for the U.S. House of Representatives.",
    'Senate': "The Congressional Record for the U.S. Senate."
}