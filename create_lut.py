# this is a python script that takes two images (base and color corrected version) and creates a .cube lut from them
# usage: python create_lut.py <base_image> <corrected_image> <output_lut>

import numpy as np
from PIL import Image
from pillow_lut import load_cube_file
import colour
import sys

def generate_lut_from_images(base_img, corrected_img, size=16):
    """
    Generate a .cube LUT file from two images (base and color corrected version)
    
    Parameters:
        base_image_path: Path to the original image
        corrected_image_path: Path to the color corrected image
        size: Size of the LUT cube (default 33x33x33)
    """
    
    # Ensure images are the same size
    if base_img.size != corrected_img.size:
        raise ValueError("Images must be the same size")
    
    # Convert images to numpy arrays and normalize to 0-1
    base_array = np.array(base_img).astype(float) / 255.0
    corrected_array = np.array(corrected_img).astype(float) / 255.0

    # check if there's a value higher than 1
    if np.any(base_array > 1) or np.any(corrected_array > 1):
        raise ValueError("Images must be in the range 0-255")

    if np.any(base_array < 0) or np.any(corrected_array < 0):
        raise ValueError("Images must be in the range 0-255")
    
    # Create the LUT structure
    lut_size = size
    lut_data = np.zeros((lut_size, lut_size, lut_size, 3))
    color_samples = np.zeros((lut_size, lut_size, lut_size, 4))
    
    for i in range(base_array.shape[0]):
        for j in range(base_array.shape[1]):
            # Get color values from both images
            base_color = base_array[i, j]
            corrected_color = corrected_array[i, j]
            
            # Calculate LUT indices
            x = int(base_color[0] * (lut_size - 1))
            y = int(base_color[1] * (lut_size - 1))
            z = int(base_color[2] * (lut_size - 1))
            
            # Store the mapping
            # lut_data[x, y, z] = corrected_color
            color_samples[x, y, z, :3] += corrected_color
            # add sample count
            color_samples[x, y, z, 3] += 1
    
    # average the color samples
    for i in range(lut_size):
        for j in range(lut_size):
            for k in range(lut_size):
                if color_samples[i, j, k, 3] > 0:
                    color_samples[i, j, k, :3] = color_samples[i, j, k, :3] / color_samples[i, j, k, 3]
    
    for i in range(lut_size):
        for j in range(lut_size):
            for k in range(lut_size):
                if color_samples[i, j, k, 3] == 0:
                    identity = [i / (lut_size - 1), j / (lut_size - 1), k / (lut_size - 1)]
                    # color_samples[i, j, k, :3] = identity
                    # use nearest sample that has a value
                    nearest = identity
                    nearest_dist = 1000
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            for dz in [-1, 0, 1]:
                                if dx == 0 and dy == 0 and dz == 0:
                                    continue
                                nx, ny, nz = i + dx, j + dy, k + dz
                                if 0 <= nx < lut_size and 0 <= ny < lut_size and 0 <= nz < lut_size:
                                    if color_samples[nx, ny, nz, 3] > 0:
                                        dist = np.linalg.norm([nx - i, ny - j, nz - k])
                                        if dist < nearest_dist:
                                            nearest = color_samples[nx, ny, nz, :3]
                                            nearest_dist = dist
                    color_samples[i, j, k, :3] = nearest
    
    lut_data = color_samples[:, :, :, :3]

    # Create the LUT object
    lut3d = colour.LUT3D(
        table=lut_data,
        name='Generated LUT',
        domain=np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]),
        size=lut_size
    )

    return lut3d
    

def test_lut(image_path, lut_path, output_path):
    """
    Test the generated LUT by applying it to an image
    """
    # Load the image and LUT
    img = Image.open(image_path)
    lut = load_cube_file(lut_path)
    
    # Apply the LUT and save
    result = img.filter(lut)
    result.save(output_path)
    print(f"Test image saved at: {output_path}")

# Example usage
if __name__ == "__main__":
    # check arguments
    if len(sys.argv) != 4:
        print("Usage: python create_lut.py <base_image> <corrected_image> <output_lut>")
        sys.exit(1)
    
    base_image_path = sys.argv[1]
    corrected_image_path = sys.argv[2]
    output_lut_path = sys.argv[3]

    base_img = Image.open(base_image_path).convert('RGB')
    corrected_img = Image.open(corrected_image_path).convert('RGB')
    
    # Generate LUT
    out_lut = generate_lut_from_images(
        base_img,
        corrected_img,
        size=33
    )

    # add .cube extension if not present
    if not output_lut_path.endswith(".cube"):
        output_lut_path += ".cube"
    # Write the CUBE file
    colour.write_LUT(out_lut, output_lut_path)
    
    print(f"LUT file generated successfully at: {output_lut_path}")
    
    # Test the generated LUT
    test_lut(
        base_img,
        output_lut_path,
        "test_result.png"
    )
