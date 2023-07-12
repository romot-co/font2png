import argparse
import string
import unicodedata
from PIL import Image, ImageFont
from fontTools.ttLib import TTFont  # For working with TrueType and OpenType fonts
import os
from tqdm import tqdm

# Function to generate a png image from font file...
def generate_png_from_fontfile(font_file, output_dir, image_size=512):
    # Load the font file using TTFont function...
    try:
      font = TTFont(font_file)
    except Exception as e:
      print(f"Error loading font file: {e}")

    valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    char_limit = 255

    def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
        # replace spaces
        for r in replace:
            filename = filename.replace(r,'_')
        
        # keep only valid ascii chars
        cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
        
        # keep only whitelisted chars
        cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
        return cleaned_filename[:char_limit]

    # Get a list of all characters in the font...
    chars = font.getBestCmap().keys()

    # Create an instance of the FreeType font, at the given size...
    pil_font = ImageFont.truetype(font_file, image_size)

    # Making directory if doesn't exist...
    os.makedirs(output_dir, exist_ok=True)

    # Loop over all characters, adding a progress bar from tqdm
    for char in tqdm(chars, desc='Generating images'):
        # Change unicode character to string
        char_str = chr(char)
        
        # Skip non-printable/invalid characters.
        if unicodedata.category(char_str)[0] == "C":
            continue

        # Skip characters outside JIS2014 Full-width characters range and ISO-8859-1 printable characters range.
        if not ((0x4E00 <= char <= 0x9FFC) or 
                (0x3041 <= char <= 0x3096 and char != 0x3097 and char != 0x3098) or 
                (char == 0x309F) or 
                (0x30A1 <= char <= 0x30FA and char != 0x30FB) or 
                (0x30FC <= char <= 0x30FF) or
                (0x20 <= char <= 0x7E) or
                (0xA0 <= char <= 0xFF)):
            continue

        # Create a new image with white background (RGBA)
        image = Image.new('RGBA', (image_size, image_size), (255, 255, 255))

        # Importing ImageDraw module & Create a draw object
        from PIL import ImageDraw 
        draw = ImageDraw.Draw(image)

        # Get size of the character written in the font size
        # textbbox returns the box coordinates as (left, upper, right, lower)
        bbox = draw.textbbox((0, 0), char_str, font=pil_font)
        
        # we calculate the width and height from the bounding box
        w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
        
        # Calculate x and y position to center the character
        x = (image_size - w) / 2
        y = image_size - h - image_size / 16 # 1/16 of image size from bottom

        # Draw the black text on white image
        draw.text((x, y), char_str, fill="black", font=pil_font)

        # Get UTF-8 byte sequence for the character
        utf8_byte_sequence = char_str.encode('utf-8').hex()

        # Save the image. Clean the filename before saving.
        cleaned_char_str = clean_filename(char_str)
        output_filename = os.path.join(output_dir, f"{utf8_byte_sequence}_{cleaned_char_str}.png")
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
