from PIL import Image
import os

# Define the directory containing images
IMAGE_DIR = '../images/characters/'
TARGET_SIZE = (300, 400)  # Adjust as needed

def optimize_image(image_path, target_size, quality=85):
    """
    Optimizes an image by resizing and compressing it.

    Args:
        image_path (str): Path to the image file.
        target_size (tuple): Desired size as (width, height).
        quality (int): Quality setting for compression (1-95).

    Returns:
        None
    """
    try:
        with Image.open(image_path) as img:
            # Ensure consistent format and avoid transparency issues
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            # Resize the image while maintaining aspect ratio
            img.thumbnail(target_size, Image.LANCZOS)
            # Save the optimized image
            optimized_path = f"{os.path.splitext(image_path)[0]}_optimized.jpg"
            img.save(optimized_path, format="JPEG", optimize=True, quality=quality)
        print(f"Optimized and saved: {optimized_path}")
    except Exception as e:
        print(f"Failed to optimize {os.path.basename(image_path)}: {e}")

def main():
    if not os.path.isdir(IMAGE_DIR):
        print(f"Image directory {IMAGE_DIR} does not exist.")
        return

    for filename in os.listdir(IMAGE_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(IMAGE_DIR, filename)
            optimize_image(image_path, TARGET_SIZE)

    print("Image optimization completed.")

if __name__ == "__main__":
    main()
