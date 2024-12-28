# scripts/download_images.py

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging

# Configure logging
logging.basicConfig(
    filename='../download_images.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Constants
API_URL = "https://myheroacademia.fandom.com/wiki/"
DATA_CSV_PATH = '../data/characters.csv'
IMAGE_DIR = '../images/characters/'
HEADERS = {
    'User-Agent': 'MyHeroAcademiaDashboardBot/1.0 (https://yourwebsite.com/)'  # Replace with your info
}
REQUEST_DELAY = 1  # Seconds between requests to be polite

def fetch_image_url(character_name):
    """
    Fetches the image URL for a given character from the Fandom Wiki.

    Args:
        character_name (str): The name of the character.

    Returns:
        str or None: The direct URL to the character's image, or None if not found.
    """
    try:
        # Format the character name for the URL
        formatted_name = character_name.replace(' ', '_')
        url = f"{API_URL}{formatted_name}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the image tag within the infobox
        image_tag = soup.find('img', class_='pi-image-thumbnail')
        if image_tag and 'src' in image_tag.attrs:
            image_url = image_tag['src']
            # Some URLs may start with //, add the protocol
            if image_url.startswith('//'):
                image_url = 'https:' + image_url
            return image_url
        else:
            logging.warning(f"No image found for {character_name}")
            return None

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error for {character_name}: {http_err}")
    except Exception as err:
        logging.error(f"Error fetching image for {character_name}: {err}")
    return None

def download_image(image_url, save_path):
    """
    Downloads an image from a URL and saves it to the specified path.

    Args:
        image_url (str): The URL of the image.
        save_path (str): The local filesystem path to save the image.

    Returns:
        bool: True if download is successful, False otherwise.
    """
    try:
        response = requests.get(image_url, headers=HEADERS, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        logging.info(f"Downloaded image to {save_path}")
        return True
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error downloading {image_url}: {http_err}")
    except Exception as err:
        logging.error(f"Error downloading {image_url}: {err}")
    return False

def main():
    # Ensure the image directory exists
    os.makedirs(IMAGE_DIR, exist_ok=True)

    # Load character data
    try:
        df = pd.read_csv(DATA_CSV_PATH, dtype={'id': str})  # Ensure 'id' is read as string
    except FileNotFoundError:
        logging.error(f"CSV file not found at {DATA_CSV_PATH}")
        print(f"Error: CSV file not found at {DATA_CSV_PATH}")
        return
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        print(f"Error reading CSV file: {e}")
        return

    # Iterate over each character and download their image
    for index, row in df.iterrows():
        # Determine which category the character belongs to
        category = str(row.get('category', '')).lower()
        if category not in ['students', 'villains', 'heroes', 'other']:
            logging.warning(f"Unknown category '{category}' for character ID {row.get('id')}")
            continue

        # Extract character name and ID
        character_id = str(row.get('id', '')).strip()
        character_name = str(row.get('name', '')).strip()

        if not character_id or not character_name:
            logging.warning(f"Missing ID or name for row index {index}")
            continue

        # Define the image filename
        image_filename = f"character_{character_id}.png"
        image_path = os.path.join(IMAGE_DIR, image_filename)

        # Skip if image already exists
        if os.path.exists(image_path):
            logging.info(f"Image already exists for {character_name}, skipping download.")
            continue

        # Fetch the image URL
        image_url = fetch_image_url(character_name)
        if image_url:
            success = download_image(image_url, image_path)
            if not success:
                print(f"Failed to download image for {character_name}. See log for details.")
        else:
            print(f"No image URL found for {character_name}. See log for details.")

        # Delay to respect server load
        time.sleep(REQUEST_DELAY)

    print("Image downloading process completed. Check the log file for details.")

if __name__ == "__main__":
    main()
