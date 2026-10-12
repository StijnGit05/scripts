import json
from pathlib import Path
from PIL import Image

config_path = Path(__file__).resolve().parent / 'configInvert.json'
with config_path.open('r', encoding='utf-8') as config_file:
    config = json.load(config_file)

INPUT_IMAGE = config['INPUT_IMAGE']
OUTPUT_IMAGE = config['OUTPUT_IMAGE']

def invert_image_colors(input_path, output_path):
    try:
        # Open the image
        image = Image.open(input_path)

        # Convert to RGB if not already (handles grayscale, black/white, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Invert the colors
        inverted_image = Image.eval(image, lambda x: 255 - x)

        # Save the inverted image
        inverted_image.save(output_path)
        print(f"Inverted image saved to {output_path}")

    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    invert_image_colors(INPUT_IMAGE, OUTPUT_IMAGE)
