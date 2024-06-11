import requests
import zipfile
import os

def download_and_unzip(url, extract_to):
    """
    Download a zip file and extract its contents.

    :param url: URL to the zip file.
    :param extract_to: Directory where contents will be extracted.
    """
    # Send a HTTP request to the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Define the zip file name, you might want to use temp files or specific naming
        zip_name = "temp.zip"
        
        # Write the content of the response to a zip file
        with open(zip_name, 'wb') as zip_file:
            zip_file.write(response.content)
        
        # Now, unzip the file
        with zipfile.ZipFile(zip_name, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        # Clean up the zip file
        os.remove(zip_name)
    else:
        print(f"Failed to retrieve the zip file. Status Code: {response.status_code}")
