# Monte Carlo π Estimation and 7-Segment Display Visualization

This project provides an approximation of π using the Monte Carlo method and visualizes the results on a 7-segment display in a series of PPM images, which are then combined into an animated GIF.

This Markdown file now includes:
1. An overview of the project
2. Explanations for both `monte_carlo.py` and `draw.py` scripts
3. Usage instructions for both scripts
4. A detailed explanation of the `draw.py` script's functions
5. The resulting GIF animation showing the π approximation

The GIF is included at the end of the file and should display when the Markdown is rendered, assuming the `output.gif` file is in the same directory as this Markdown file.

## Overview

The project consists of two main scripts:

1. **`monte_carlo.py`**: This script uses the Monte Carlo method to approximate the value of π.
2. **`draw.py`**: This script generates a series of PPM images representing a 7-segment display showing the approximated value of π. The images are then compiled into an animated GIF.

## `monte_carlo.py`

This script estimates the value of π by generating random points within a square and calculating the ratio of points that fall inside a unit circle.

### Usage

```bash
./monte_carlo.py points_number

# draw.py

This script generates a series of images showing the value of π approximated by the Monte Carlo method on a 7-segment display. The images are then combined into an animated GIF.

## Usage

    ./draw.py image_size points_number decimal_places_number

- `image_size`: The size of the generated images (must be greater than 100).
- `points_number`: The number of points used for the Monte Carlo estimation (must be greater than 100).
- `decimal_places_number`: The number of decimal places to display (between 1 and 5).

Example: ./draw.py 500 10000 3

## Script Explanation

### Constants:
Define the geometry of the 7-segment display and color definitions.

### Functions:

1. `check_for_ppm_files()`: Checks for existing .ppm files in the directory.
2. `delete_ppm_files()`: Deletes all .ppm files in the directory.
3. `seven_segments(i, step)`: Generates points for each segment of a 7-segment display.
4. `get_str_decimal_part(number)`: Gets the string representation of the decimal part of a number.
5. `search_pixel(point, img_size)`: Converts a point to pixel coordinates in the image.
6. `draw_comma(pixels_matrix, starting_pos)`: Draws a comma (decimal point) in the pixels matrix.
7. `draw_number(pixels_matrix, number, base_pos)`: Draws a number on the 7-segment display in the pixels matrix.
8. `generate_ppm_file(image_size, points, state_number, value)`: Generates a PPM file representing a 7-segment display image.
9. `draw()`: Main function to draw the images and create an animated GIF.

## Result

Here's an animation showing the approximation of π using the Monte Carlo method:

![Animation of π approximation](https://github.com/BelfaidaMedReda/-Approximation-/blob/main/output.gif)
