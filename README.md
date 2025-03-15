# LUTkit

## What is it?
**LUTkit** is a set of python scripts to create quick 'n' dirty LUTs by doing automatic color matching on a pair of images. It's primarily targetting LUTs for usage in Unreal Engine projects but it's possible to convert the resulting LUTs so they can be used in other game engines and software.

## Prerequisites
Check requirements.txt.

**Note:** These exact versions of packages might not be needed but I'm too lazy to check.

## Usage
```
python end_to_end.py <source image> <reference image> <output lut path> [--test]
```
`source image` is the image you wish to color correct (e.g. a screenshot from your game, a still from your video, or just about any image you want).

`reference image` is the image with the desired look.

`output lut path` is the path to save the resulting LUT to. The LUT will be saved in the standard .cube format as well as a .png for use in Unreal Engine. The resulting LUT dimensions are 16x16x16.

`--test` is optional. If enabled, the resulting LUT will be applied to the `source image` and saved as `test_result.png` in the current directory. This can be used to quickly check if color matching was performed correctly.

## Known Issues
The resulting LUT can end up a bit brighter and / or less contrast-y than the reference image. This is most likely due to the extremely naive algorithm for creating the LUT. I plan to revise it and / or add approximate color correction sometime in the future.