#!/usr/bin/env python3 
import sys 
import subprocess
from monte_carlo import *

pink=(255,0,255)
blue=(0,0,255)
pink_color="255 0 255"
blue_color="0 0 255"
blank_color="255 255 255"

def get_decimal_part(number):
    number=str(number)
    return int(number[2:])

def generate_ppm_file(image_size,points,state_number,value):
    integer_part=int(value)
    decimal_part=get_decimal_part(value)
    file_name=f"img{state_number}_{integer_part}-{decimal_part}.ppm"
    target_file=open(file_name,"w")
    magic_number="P3"
    print(magic_number,file=target_file)
    dimensions=f"{image_size} {image_size}"
    print(dimensions,file=target_file)
    print(255,file=target_file)
    pixels_matrix=[[(255,255,255)]*image_size for _ in range(image_size)]
    for point in points : 
        i,j=search_pixel(point,image_size)
        pixels_matrix[i][j]=blue if in_circle(point) else pink 
    for i in range(image_size):
        for j in range(image_size):
            if pixels_matrix[i][j] == blue:       
                print(blue_color,file=target_file)
            elif pixels_matrix[i][j]==pink:
                print(pink_color,file=target_file)
            else:
                print(blank_color,file=target_file)

def search_pixel(point,img_size):
    x,y=point
    j=int((x+1)*(img_size-1)/2)
    i=int((y+1)*(img_size-1)/2)
    return i,j

    
def draw():
    if len(sys.argv) < 4:
        print("Usage : ./draw.py image_size points_number decimal_places_number")
        print("image_size denotes the image size and it should be greater than 100")
        print("points_number denotes the number of points and it should be greater than 100")
        print("decimal_places_number denotes the number of decimal places and it should be between 1 and 5")
        sys.exit(1)
    image_size=int(sys.argv[1])
    points_number=int(sys.argv[2])
    decimal_places_number=int(sys.argv[3])
    for i in range(1,11):
        tmp=int((i*points_number)/10)
        points,value=estimate(tmp)
        value=round(value,decimal_places_number)
        generate_ppm_file(image_size,points,i,value)



if __name__=="__main__":
    draw()