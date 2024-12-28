import pandas as pd
import os

# Constants
DATA_CSV_PATH = '../data/characters.csv'
IMAGE_DIR = '../images/characters/'

def main():
    # Load the CSV with 'id' and 'name' as strings, fill NaN with empty strings
    try:
        df = pd.read_csv(DATA_CSV_PATH, dtype={'id': str, 'name': str})
        # Replace NaN with empty strings in 'id' and 'name'
        df['id'] = df['id'].fillna('').astype(str)
        df['name'] = df['name'].fillna('').astype(str)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {DATA_CSV_PATH}")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # List to hold characters missing images
    missing_images = []

    # Iterate over each character
    for index, row in df.iterrows():
        # Extract character ID and name, ensuring they are strings
        character_id = row.get('id', '').strip()
        character_name = row.get('name', '').strip()

        # Define the expected image filename
        image_filename = f"character_{character_id}.png"
        image_path = os.path.join(IMAGE_DIR, image_filename)

        # Check if the image file exists
        if not os.path.exists(image_path):
            missing_images.append({'id': character_id, 'name': character_name})

    # Output the results
    if missing_images:
        print("Characters missing images:")
        for char in missing_images:
            print(f"ID: {char['id']}, Name: {char['name']}")
    else:
        print("All characters have corresponding images.")

if __name__ == "__main__":
    main()
