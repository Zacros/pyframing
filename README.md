# Prepare your images for printing!

This tool will crop the image at the center and then up/down-scale based on the DPI-Print Size given

## Standalone usage via terminal

_virtual env recommended_

`pip3 install -r requirements.txt`

#### Params Required

- imgPath : Path to the image
- print_size : Print size in inches, example 10x12
- DPI : Dots Per Inch, example 300

#### Usage example

`python pyframing.py test_image.jpg 10x12 300`

The processed image will be saved at the same path of the original image.

## Usage as a lib

Core functions to use

```
# Load the image
image = cv2.imread(".../test.jpg")

# Prepare the image for printing
ready_to_print_image= crop_fit_to_inch_dpi(image, inch_size = [5, 7], dpi =300)

# Save image as a file
save_cv2_image(image, path, dpi, params = None)
```
