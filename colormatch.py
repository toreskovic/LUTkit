# python script that takes two images and does automatic color grading
# Usage: python colormatch.py <source_image> <target_image>

from color_matcher import ColorMatcher
from color_matcher.normalizer import Normalizer
from PIL import Image
import numpy as np
import sys


def color_match(img_src, img_ref, strength=1.0):
    img_src = Normalizer(np.asarray(img_src)).type_norm()
    img_ref = Normalizer(np.asarray(img_ref)).type_norm()

    cm = ColorMatcher()
    # these two work ok-ish
    # img_res = cm.transfer(src=img_src, ref=img_ref, method='mkl')
    # img_res = cm.transfer(src=img_src, ref=img_ref, method='mvgd')
    img_res = cm.transfer(src=img_src, ref=img_ref, method='hm')

    # these two work better but need similar lighting conditions
    # img_res = cm.transfer(src=img_src, ref=img_ref, method='hm-mkl-hm')
    img_res_2 = cm.transfer(src=img_src, ref=img_ref, method='hm-mvgd-hm')
    # img_res_2 = cm.transfer(src=img_src, ref=img_ref, method='hm')

    # blend the results
    img_res = img_res * 0.5 + img_res_2 * 0.5

    # blend the result with the original image using the strength parameter
    # img_res = img_src * (1 - strength) + img_res * strength

    # convert to PIL image
    img_res = Normalizer(img_res).uint8_norm()
    img_res = Image.fromarray(img_res)

    return img_res

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python colormatch.py <source_image> <target_image>")
        sys.exit(1)
        src_path = sys.argv[1]
        ref_path = sys.argv[2]

        img_src = Image.open(src_path).convert('RGB')
        img_ref = Image.open(ref_path).convert('RGB')

        img_res = color_match(img_src, img_ref)

        output_path = src_path.split(".")[0] + "_matched.png"
        img_res.save(output_path)