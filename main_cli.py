
import argparse
from pathlib import Path
import os
import cv2
from process import (
    apply_adaptive_thresholding,
    apply_gaussian_smoothing,
    apply_laplacian_filter,
    apply_morphological_operation,
    apply_sobel_filter,
)
from visualize import add_white_boarder, crop_image, resize_image


def resize_image_factor(img, factor):
    """Resize the image by the given factor."""
    h, w = img.shape[:2]
    new_h = int(h * factor)
    new_w = int(w * factor)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)


def process_single_image(img_path, args):
    # Read the input image
    img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)

    # Ensure image was loaded
    if img is None:
        raise ValueError(f"Failed to load image from path: {img_path}")

    # Convert image to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # List to keep track of applied operations
    operations = []

    # Crop image if arguments provided
    if all([args.ymin, args.ymax, args.xmin, args.xmax]):
        img = crop_image(img, args.ymin, args.ymax, args.xmin, args.xmax)
        operations.append("cropped")

    # Add white border if argument provided
    if args.border_width:
        img = add_white_boarder(img, args.border_width)
        operations.append(f"border{args.border_width}")

    # Resize image if arguments provided
    if args.resize_dim and args.resize_val:
        img = resize_image(img, args.resize_dim, args.resize_val)
        operations.append(f"resize{args.resize_val}{args.resize_dim}")

    # Resize image by the given factor
    if args.resize_factor != 1.0:
        img = resize_image_factor(img, args.resize_factor)
        operations.append(f"resized{args.resize_factor}")

    # Apply morphological operation if argument provided
    if args.morph:
        img = apply_morphological_operation(img, args.morph)
        operations.append(args.morph)

    # Apply Gaussian smoothing if flag set
    if args.gaussian:
        img = apply_gaussian_smoothing(img)
        operations.append("gaussian")

    # Apply adaptive thresholding if argument provided
    if args.adaptive:
        img = apply_adaptive_thresholding(img, args.adaptive)
        operations.append(args.adaptive)

    # Apply Sobel filter if argument provided
    if args.sobel:
        img += apply_sobel_filter(img, args.sobel)
        operations.append(f"sobel{args.sobel}")

    # Apply Laplacian filter if flag set
    if args.laplacian:
        img = apply_laplacian_filter(img)
        operations.append("laplacian")

    # Generate the output file name
    output_filename = f"{'_'.join([img_path.stem] + operations)}{img_path.suffix}"
    output_path = args.output / output_filename

    # Save the processed image
    cv2.imwrite(str(output_path), img)

def main(args):
    # If the image argument is a directory, process all images inside it
    if args.image.is_dir():
        for img_file in args.image.iterdir():
            if img_file.suffix in ['.jpg', '.jpeg', '.png', '.bmp', '.tif']:
                process_single_image(img_file, args)
    else:
        process_single_image(args.image, args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenCV Image Processing for OCR")

    # Image input and output paths with default values
    parser.add_argument("--image", default=Path("./images"), type=Path, help="Path to the input image or folder containing images.")
    parser.add_argument("--output", default=Path("./results"), type=Path, help="Path to save the processed image or folder to save processed images.")

    # Crop arguments with default values
    parser.add_argument("--ymin", default=None, type=int, help="Y-coordinate for the top of the cropping rectangle.")
    parser.add_argument("--ymax", default=None, type=int, help="Y-coordinate for the bottom of the cropping rectangle.")
    parser.add_argument("--xmin", default=None, type=int, help="X-coordinate for the left of the cropping rectangle.")
    parser.add_argument("--xmax", default=None, type=int, help="X-coordinate for the right of the cropping rectangle.")

    # Add white border with default value
    parser.add_argument("--border_width", default=None, type=int, help="Width of white border to add around the image.")

    # Resize arguments with default values
    parser.add_argument("--resize_dim", default=None, choices=['h', 'w'], help="Dimension to resize, 'h' for height or 'w' for width.")
    parser.add_argument("--resize_val", default=None, type=int, help="Value to resize the specified dimension to.")
    parser.add_argument("--resize_factor", default=1.0, type=float, help="Factor by which to resize the image. Greater than 1 enlarges, between 0 and 1 shrinks.")

    # Processing functions with default values
    parser.add_argument("--morph", default=None, choices=['open', 'close'], help="Apply morphological operation.")
    parser.add_argument("--gaussian", default=False, action='store_true', help="Apply Gaussian smoothing.")
    parser.add_argument("--adaptive", default=None, choices=['gaussian', 'mean'], help="Apply adaptive thresholding.")
    parser.add_argument("--sobel", default=None, choices=['h', 'v'], help="Apply Sobel filter.")
    parser.add_argument("--laplacian", default=False, action='store_true', help="Apply Laplacian filter.")

    args = parser.parse_args()
    
    # Ensure the output directory exists
    args.output.mkdir(parents=True, exist_ok=True)
    
    main(args)
