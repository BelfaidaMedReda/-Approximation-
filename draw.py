#!/usr/bin/env python3 
import sys 
import subprocess
from random import randint
from PIL import Image
from monte_carlo import *

step=30
offset=10

segments={
    0:['a','b','c','d','e','g'],
    1:['b','c'],
    2:['a','b','g','d','e'],
    3:['a','b','f','c','d'],
    4:['b','c','g','f'],
    5:['a','f','g','c','d'],
    6:['a','f','g','e','d','c'],
    7:['a','b','c'],
    8:['a','b','c','d','e','f','g'],
    9:['a','b','c','d','f','g']
}

light_segments={
    'a':[(-(step+1),k) for k in range(-(step+1),1)],
    'b':[(k,0) for k in range(-(step+1),0)],   
    'c':[(k,0) for k in range(1,step+2)],
    'd':[(step+1,k) for k in range(-(step+1),1)],
    'e':[(k,-(step+1)) for k in range(1,step+2)],
    'f':[(0,k) for k in range(-(step+1),1)],
    'g':[(k,-(step+1)) for k in range(-(step+1),0)],
}

pink=(255,0,255)
blue=(0,0,255)
black=(0,0,0)
pink_color="255 0 255"
blue_color="0 0 255"
blank_color="255 255 255"
black_color="0 0 0" 
ppm_files=[]

def get_str_decimal_part(number):
    return str(number)[2:]

def search_pixel(point,img_size):
    x,y=point
    j=int((x+1)*(img_size-1)/2)
    i=int((y+1)*(img_size-1)/2)
    return i,j

def draw_comma(pixels_matrix,starting_pos):
    i,j=starting_pos
    for k in range(offset):
        pixels_matrix[i+step-1][j+k]=black 
        pixels_matrix[i+step][j+k]=black 
        pixels_matrix[i+step+1][j+k]=black
    return pixels_matrix

def draw_number(pixels_matrix,number,starting_pos):
    assert 0<=number<=9 
    i,j=starting_pos
    pixels_matrix[i][j]=black
    if number==0:
        pixels_matrix[i][j-step]=black
    for seg in segments[number]:
        for offset in light_segments[seg]:
            pixels_matrix[i+offset[0]][j+offset[1]]=black
    return pixels_matrix

def generate_ppm_file(image_size,points,state_number,value):
    value=str(value)
    file_name=f"img{state_number}_"+value[0]+"-"+value[2:]+".ppm"
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
    index=len(value)//2
    i=(image_size//2)+step  # positioning i relatively to the center
    j= i-(step+offset)*(index-1) # positioning j as well
    current=(i,j)
    copy=current
    pixels_matrix=draw_comma(pixels_matrix,copy)
    copy=(copy[0],copy[1]-offset)
    pixels_matrix=draw_number(pixels_matrix,int(value[0]),copy)
    current=(current[0],current[1]+step+offset)
    for number in value[2:]:
        pixels_matrix=draw_number(pixels_matrix,int(number),current)
        current=(current[0],current[1]+step+offset)
    for i in range(image_size):
        for j in range(image_size):
            if pixels_matrix[i][j] == blue:       
                print(blue_color,file=target_file)
            elif pixels_matrix[i][j]==pink:
                print(pink_color,file=target_file)
            elif pixels_matrix[i][j]==black:
                print(black_color,file=target_file)
            else:
                print(blank_color,file=target_file)
    ppm_files.append(file_name)

    
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
    frames = [Image.open(image) for image in ppm_files]
    frames[0].save('output.gif', save_all=True, append_images=frames[1:], duration=500, loop=0)

if __name__=="__main__":
    draw()