# scripts/fetch_data.py

import requests
import pandas as pd
import os
import logging
import pprint

# Configure logging
logging.basicConfig(
    filename='../fetch_data.log',  # Log file in project root
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Define the API endpoint
API_URL = "https://myheroacademia-api.onrender.com/characters"

def fetch_characters():
    try:
        print("Sending request to API...")
        response = requests.get(API_URL)
        print(f"Received response with status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        print(f"Data type received: {type(data)}")

        # Use pprint for better readability
        pp = pprint.PrettyPrinter(indent=4)
        print("Sample data:")
        pp.pprint({k: v[:2] if isinstance(v, list) else v for k, v in data.items()})

        # Initialize an empty list to hold all characters
        all_characters = []

        # Define the categories to extract
        categories = ['students', 'villains', 'heroes', 'other']

        for category in categories:
            if category in data:
                characters = data[category]
                if isinstance(characters, list):
                    for char in characters:
                        if isinstance(char, dict):
                            char['category'] = category.capitalize()  # Add category field
                            all_characters.append(char)
                        else:
                            logging.warning(f"Expected dict in {category}, but got {type(char)}: {char}")
                            print(f"Warning: Expected dict in {category}, but got {type(char)}. See log for details.")
                else:
                    logging.error(f"Expected list for category '{category}', but got {type(characters)}.")
                    print(f"Error: Expected list for category '{category}', but got {type(characters)}.")
            else:
                logging.warning(f"Category '{category}' not found in API response.")
                print(f"Warning: Category '{category}' not found in API response.")

        if all_characters:
            logging.info(f"Successfully fetched {len(all_characters)} characters from the API.")
            return all_characters
        else:
            logging.warning("No character data fetched from the API.")
            print("Warning: No character data fetched from the API.")
            return []

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        print(f"HTTP error: {http_err}")
    except ValueError as json_err:
        logging.error(f"JSON decoding failed: {json_err}")
        print(f"JSON decoding error: {json_err}")
    except Exception as err:
        logging.exception("An unexpected error occurred:")
        print(f"An unexpected error occurred: {err}")
    return []

def save_characters_to_csv(characters, output_path):
    if not characters:
        logging.warning("No characters to save to CSV.")
        print("Warning: No characters to save to CSV.")
        return

    # Extract all unique keys from the characters to define CSV columns
    all_keys = set()
    for char in characters:
        all_keys.update(char.keys())

    # Define the desired order of columns (optional)
    desired_order = ['id', 'name', 'category', 'name_japanese', 'hero_name', 'hero_name_japanese',
                    'other_names', 'quirk', 'quirk_japanese', 'quirk_description',
                    'hero_school', 'class', 'affiliation', 'civilian_description', 'type',
                    'image_path']

    # Reorder columns, placing desired_order first and then others
    columns = [key for key in desired_order if key in all_keys] + sorted(all_keys - set(desired_order))

    data = []

    for idx, char in enumerate(characters, start=1):
        char_data = {}
        for key in columns:
            # Handle missing keys
            char_data[key] = char.get(key, "")
        # Define ImagePath if 'id' exists
        if 'id' in char and char['id']:
            char_data['image_path'] = f"images/characters/character_{char['id']}.png"
        else:
            logging.warning(f"Character at index {idx} is missing 'id': {char}")
            print(f"Warning: Character at index {idx} is missing 'id'. See log for details.")
            char_data['image_path'] = ""

        data.append(char_data)

    df = pd.DataFrame(data)

    # Ensure the 'data/' directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        logging.info(f"Character data saved to {output_path}")
        print(f"Character data saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to save data to CSV: {e}")
        print(f"Error saving CSV: {e}")

def main():
    characters = fetch_characters()
    if characters:
        # Use absolute path for output
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        output_path = os.path.join(project_root, 'data', 'characters.csv')
        save_characters_to_csv(characters, output_path)
    else:
        logging.warning("No character data fetched; skipping CSV saving.")
        print("Warning: No character data fetched; skipping CSV saving.")

if __name__ == "__main__":
    main()
