# python script that takes an image and applies a LUT to it
# Usage: python apply_lut.py <LUT>
# the image will be saved as <LUT>.png

from PIL import Image
from pillow_lut import load_cube_file
import sys

# if len(sys.argv) != 3:
#     print("Usage: python apply_lut.py <image> <LUT>")
#     sys.exit(1)

def apply_lut(lut_path):
    lut = load_cube_file(lut_path)
    im = Image.open("LUT neutral 16.png")
    output_path = lut_path.split(".")[0] + ".png"
    im.filter(lut).save(output_path)

    return output_path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python apply_lut.py <LUT>")
        sys.exit(1)
