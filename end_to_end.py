from colormatch import color_match
from create_lut import generate_lut_from_images, test_lut
from apply_lut import apply_lut
import sys
from PIL import Image
import colour

# python script that takes in two images and an output lut name
# it uses color_match, generate_lut_from_images, and apply_lut to create the resulting LUT
# usage: python end_to_end.py <source_image> <target_image> <output_lut>

# inserts LUT neutral 16.png to the upper left corner of the image and saves it as a new image
def insert_ref_colors(img_path):
    ref_img = Image.open("LUT neutral 16.png")
    img = Image.open(img_path).convert('RGB')
    img.paste(ref_img, (0, 0))

    return img

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python end_to_end.py <source_image> <target_image> <output_lut> <--test>")
        sys.exit(1)

    source_image = sys.argv[1]
    target_image = sys.argv[2]
    output_lut = sys.argv[3]

    # insert the reference colors to the source image
    img_src = insert_ref_colors(source_image)
    img_ref = Image.open(target_image).convert('RGB')

    # color match the two images
    img_matched = color_match(img_src, img_ref)

    # generate the LUT from the two images
    lut = generate_lut_from_images(img_src, img_matched)

    # write the LUT to a file
    if not output_lut.endswith(".cube"):
        output_lut += ".cube"
    colour.write_LUT(lut, output_lut)

    # test the LUT
    if len(sys.argv) == 5 and sys.argv[4] == "--test":
        test_lut(source_image, output_lut, "test_result.png")

    # apply the LUT to the source image
    apply_lut(output_lut)