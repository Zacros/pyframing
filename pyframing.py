import cv2
from PIL import Image
import math


# Crop image at center
def center_crop_image(image, proportions = [5, 7] ):

    is_portrait = image.shape[0] > image.shape[1]

    # Crop Image using max size
    max_dim_px = max(image.shape[:2])
    # Portrait
    if is_portrait:
        new_h = max_dim_px # unchanged
        new_w = new_h * proportions[0] / proportions[1]
    # Landscape
    else:
        new_w = max_dim_px # unchanged
        new_h = new_w * proportions[0] / proportions[1]



    x = image.shape[1]/2 - new_w/2
    y = image.shape[0]/2 - new_h/2

    # Crop out of bound
    if x <0 or y <0:
        # CROP image usin min size
        min_dim_px = min(image.shape[:2])
        # Portrait
        if is_portrait:
            new_w = min_dim_px # unchanged
            new_h = new_w * proportions[1] / proportions[0]
        # Landscape
        else:
            new_h = min_dim_px # unchanged
            new_w = new_h * proportions[1] / proportions[0]


    x = image.shape[1]/2 - new_w/2
    y = image.shape[0]/2 - new_h/2

    # Crop the Image from the Center
    crp_image = image[int(y):int(y+new_h), int(x):int(x+new_w)]

    return crp_image


## Upscale or downscale using interpolation 
def resize_image_same_AR(image, max_size_px):
    # calculate scaling factor
    sc = max_size_px/image.shape[0] if image.shape[0] > image.shape[1] else max_size_px/image.shape[1]

    # Choose interpolation method, based on upscaling or downscaling
    # For Upscaling
    # cv2.INTER_LANCZOS4 - interpolation with an 8×8-pixel neighborhood - Higher quality
    # cv2.INTER_CUBIC - interpolation with an 4x4-pixel neighborhood
    interpolation =  cv2.INTER_LANCZOS4 if sc > 1 else cv2.INTER_AREA
    # Rescale or not
    mod_image = cv2.resize(image, dsize = [math.ceil(image.shape[1]*sc), math.ceil(image.shape[0]*sc)], interpolation=interpolation) if sc != 1 else image

    return mod_image


# Crop then up/downscale
def crop_fit_to_inch_dpi(image, inch_size = [5, 7], dpi =300):

    # First crop then down/up-scale
    image = center_crop_image(image, inch_size)
    max_size_px = max(inch_size) * dpi
    min_size_px = min(inch_size) * dpi

    # Resize image to proper dimension respecting the dpi
    image = resize_image_same_AR(image, max_size_px)
    # Remove the excessive pixels due to float scaling factor, in order to be pixel perfect in the final shape
    image = image[:max_size_px, :min_size_px] if image.shape[0]> image.shape[1] else image[:min_size_px, :max_size_px]

    return image



# Params such as -> params = {"optimize":True, "quality":95}
# To JPEG (prob)
def save_cv2_image(image, path, dpi, params = None):
    # From cv2 to PIL colors order
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # From open cv image to PIL
    PILimage = Image.fromarray(image)
    # Save Image with DPI
    # Go for highest quality if no params provided
    # im.save(filename, 'jpeg', icc_profile=im.info.get('icc_profile')) add color profile?
    PILimage.save(path, dpi=(dpi, dpi), quality = 95, subsampling=0) if not params else PILimage.save(path, dpi=(dpi, dpi), **params)




if __name__ == "__main__":
    import os
    import argparse
    #print_sizes = { "5x7" : [5,7], "6x8" : [6,8], "8x10":[8,10], "10x12":[10,12],
    #                "11x14":[11,14], "12x15":[12,15], "16x20":[16,20], "18x24":[18,24]}



    # Parse the arguments
    parser = argparse.ArgumentParser(description='Prepare your images for printing! This tool will crop the image at the center and up/down-scale to the right proportions given the DPI-Print Size')
    parser.add_argument('imgPath', type=str, help='Path to the image')
    parser.add_argument('print_size', type=str, help='Print size in inches, example 6x8')
    parser.add_argument('dpi', type=int, help='Dots Per Inch, example 300')
    args = parser.parse_args()

    # Extract the new image dimensions in inches
    inches = list(map(int, args.print_size.split('x')))
    # Read the image
    image = cv2.imread(args.imgPath)
    # Apply trasformations
    crp_fit_image = crop_fit_to_inch_dpi(image, inch_size = inches, dpi =args.dpi)

    # Extract image path
    directory_path = os.path.dirname(args.imgPath)
    # Extract the image name and remove the file extension
    imageName = os.path.splitext(os.path.basename(args.imgPath))[0]

    save_cv2_image(crp_fit_image, os.path.join(directory_path,imageName+"_ready.jpg"), dpi=args.dpi)



