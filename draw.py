#!/usr/bin/env python3

import sys
import subprocess
from random import randint
from PIL import Image
from monte_carlo import *

# Constants for the 7-segment display
step = 30
offset = 20
police = 10

# Segment mapping for the 7-segment display
segments = {
    0: ['a', 'b', 'c', 'd', 'e', 'g'],
    1: ['b', 'c'],
    2: ['a', 'b', 'f', 'd', 'e'],
    3: ['a', 'b', 'f', 'c', 'd'],
    4: ['b', 'c', 'g', 'f'],
    5: ['a', 'f', 'g', 'c', 'd'],
    6: ['a', 'f', 'g', 'e', 'd', 'c'],
    7: ['a', 'b', 'c'],
    8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    9: ['a', 'b', 'c', 'd', 'f', 'g']
}

# Color definitions
pink = (255, 0, 255)
blue = (0, 0, 255)
black = (0, 0, 0)
pink_color = "255 0 255"
blue_color = "0 0 255"
blank_color = "255 255 255"
black_color = "0 0 0"
ppm_files = []

def check_for_ppm_files():
    """
    Check for existing .ppm files in the directory (excluding test.ppm).
    
    Returns:
        result_list (list): List of .ppm files.
        check (bool): Boolean indicating if there are any .ppm files.
    """
    result = subprocess.run('ls *.ppm', capture_output=True, text=True, shell=True)
    result_list = [file for file in result.stdout.split() if file != "test.ppm"]
    return result_list, len(result_list) > 0

def delete_ppm_files():
    """
    Delete all .ppm files in the directory (excluding test.ppm).
    """
    result_list, check = check_for_ppm_files()
    if check:
        for file in result_list:
            try:
                subprocess.run(['rm', '-f', file], check=True)
                print(f"File '{file}' successfully deleted.")
            except subprocess.CalledProcessError as e:
                print(f"Error deleting file '{file}': {e}")

def seven_segments(i, step):
    """
    Generate the points for each segment of a 7-segment display.
    
    Args:
        i (int): Index for calculating segment points.
        step (int): Step size for segment calculation.
    
    Returns:
        dict: Dictionary with segment points.
    """
    return {
        'a': [(-(step + i + 1), k) for k in range(-(step + 2 * i + 1), 1)],
        'b': [(k, 0) for k in range(-(step + i + 1), 0)],
        'c': [(k, 0) for k in range(1, step + i + 2)],
        'd': [(step + i + 1, k) for k in range(-(step + 2 * i + 1), 1)],
        'e': [(k, -(step + 2 * i + 1)) for k in range(1, step + i + 2)],
        'f': [(j, k) for j in range(-police // 2, police // 2 + 1) for k in range(-(step + 2 * i + 1), 1)],
        'g': [(k, -(step + 2 * i + 1)) for k in range(-(step + i + 1), 0)],
    }

def get_str_decimal_part(number):
    """
    Get the string representation of the decimal part of a number.
    
    Args:
        number (float): Number to extract the decimal part from.
    
    Returns:
        str: String representation of the decimal part.
    """
    return str(number)[2:]

def search_pixel(point, img_size):
    """
    Convert a point to pixel coordinates in the image.
    
    Args:
        point (tuple): Point coordinates (x, y).
        img_size (int): Size of the image.
    
    Returns:
        tuple: Pixel coordinates (i, j).
    """
    x, y = point
    j = int((x + 1) * (img_size - 1) / 2)
    i = int((y + 1) * (img_size - 1) / 2)
    return i, j

def draw_comma(pixels_matrix, starting_pos):
    """
    Draw a comma (decimal point) in the pixels matrix.
    
    Args:
        pixels_matrix (list): Matrix of pixels.
        starting_pos (tuple): Starting position (i, j) for the comma.
    
    Returns:
        list: Updated pixels matrix.
    """
    i, j = starting_pos
    for k in range(offset):
        for p in range(police):
            pixels_matrix[i + step - 1 + p][j + k] = black
            pixels_matrix[i + step + p][j + k] = black
            pixels_matrix[i + step + 1 + p][j + k] = black
    return pixels_matrix

def draw_number(pixels_matrix, number, base_pos):
    """
    Draw a number on the 7-segment display in the pixels matrix.
    
    Args:
        pixels_matrix (list): Matrix of pixels.
        number (int): Number to draw.
        base_pos (tuple): Base position (i, j) for the number.
    
    Returns:
        list: Updated pixels matrix.
    """
    i = base_pos[0]
    for k in range(police):
        j = base_pos[1] + k
        on_segments = seven_segments(k, step)
        pixels_matrix[i][j] = black
        if number == 0:
            pixels_matrix[i][j - (step + 2 * k)] = black
        for seg in segments[number]:
            for offset in on_segments[seg]:
                pixels_matrix[i + offset[0]][j + offset[1]] = black
    return pixels_matrix

def generate_ppm_file(image_size, points, state_number, value):
    """
    Generate a PPM file representing a 7-segment display image.
    
    Args:
        image_size (int): Size of the image.
        points (list): List of points.
        state_number (int): State number for the file name.
        value (float): Value to display.
    """
    value = str(value)
    file_name = f"img{state_number}_{value[0]}-{value[2:]}.ppm"
    target_file = open(file_name, "w")
    magic_number = "P3"
    print(magic_number, file=target_file)
    dimensions = f"{image_size} {image_size}"
    print(dimensions, file=target_file)
    print(255, file=target_file)
    pixels_matrix = [[(255, 255, 255)] * image_size for _ in range(image_size)]
    
    # Draw points
    for point in points:
        i, j = search_pixel(point, image_size)
        pixels_matrix[i][j] = blue if in_circle(point) else pink
    
    # Draw the value on the 7-segment display
    index = len(value) // 2
    i = image_size // 2  # Positioning i relatively to the center
    j = (image_size // 2) + step + police - (step + 2 * police + offset) * (index - 1)  # Positioning j as well
    current = (i, j)
    copy = current
    pixels_matrix = draw_comma(pixels_matrix, copy)
    copy = (copy[0], copy[1] - offset - police)
    pixels_matrix = draw_number(pixels_matrix, int(value[0]), copy)
    current = (current[0], current[1] + step)
    
    for number in value[2:]:
        pixels_matrix = draw_number(pixels_matrix, int(number), current)
        current = (current[0], current[1] + step + police + offset)
    
    # Write pixel data to the PPM file
    for i in range(image_size):
        for j in range(image_size):
            if pixels_matrix[i][j] == blue:
                print(blue_color, file=target_file)
            elif pixels_matrix[i][j] == pink:
                print(pink_color, file=target_file)
            elif pixels_matrix[i][j] == black:
                print(black_color, file=target_file)
            else:
                print(blank_color, file=target_file)
    
    ppm_files.append(file_name)

def draw():
    """
    Main function to draw the images and create an animated GIF.
    """
    if len(sys.argv) < 4:
        print("Usage: ./draw.py image_size points_number decimal_places_number")
        print("image_size denotes the image size and it should be greater than 100")
        print("points_number denotes the number of points and it should be greater than 100")
        print("decimal_places_number denotes the number of decimal places and it should be between 1 and 5")
        sys.exit(1)
    
    image_size = int(sys.argv[1])
    points_number = int(sys.argv[2])
    decimal_places_number = int(sys.argv[3])
    
    for i in range(1, 11):
        tmp = int((i * points_number) / 10)
        points, value = estimate(tmp)
        value = round(value, decimal_places_number)
        generate_ppm_file(image_size, points, i, value)
    
    frames = [Image.open(image) for image in ppm_files]
    frames[0].save('output.gif', save_all=True, append_images=frames[1:], duration=500, loop=0)
    delete_ppm_files()

if __name__ == "__main__":
    draw()
