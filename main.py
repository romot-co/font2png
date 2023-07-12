# Importing necessary libraries
import argparse
from PIL import Image, ImageFont # For image processing and handling fonts
from fontTools.ttLib import TTFont # For working with TrueType and OpenType fonts
import os

# Function to generate a png image from font file
def generate_png_from_fontfile(font_file, output_dir, image_size=512):
    # Load the font file using TTFont function
    font = TTFont(font_file)
    
    # Get a list of all characters in the font
    chars = font.getBestCmap().keys()
    
    # Create an instance of the FreeType font, at the given size
    pil_font = ImageFont.truetype(font_file, image_size)

    # making directory if doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Loop over all characters
    for char in chars:
        # Change unicode character to string
        char_str = chr(char)

        # Create a new image with RGBA mode 
        image = Image.new('RGBA', (image_size, image_size))
        
        # Importing ImageDraw module & Create a draw object
        from PIL import ImageDraw 
        draw = ImageDraw.Draw(image)

        # Get size of the character written in the font size
        w, h = draw.textsize(char_str, font=pil_font)
        
        # Calculate x and y position to center the character
        x = (image_size - w) / 2
        y = (image_size - h) / 2

        # Draw the text on image
        draw.text((x, y), char_str, font=pil_font)

        # Save the image
        output_filename = os.path.join(output_dir, f"{char}.png")
        image.save(output_filename, 'PNG')

# Main entry point of script.
def main():
    # Creating Argument parser object
    parser = argparse.ArgumentParser(description='Generate images from a font file.')
    
    # Adding arguments to parser object
    parser.add_argument('input_file', type=str, help='The path to the input .otf or .ttf font file.')
    parser.add_argument('output_dir', type=str, help='The directory where the output images will be saved.')
    parser.add_argument('image_size', type=int, help='The size of the output images.')

    # Parsing arguments 
    args = parser.parse_args()

    # call function with parsed arguments.
    generate_png_from_fontfile(args.input_file, args.output_dir, args.image_size)


# Ensure that this script cannot be imported as a module,
# it should only be run as a standalone script.
if __name__ == "__main__":
    main()