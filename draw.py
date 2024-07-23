#!/usr/bin/env python3 
import sys 
import subprocess
from monte_carlo.py import estimate

pink_color="255 0 255 \n"
blue_color="0 0 255 \n"

def get_decimal_part(number):
    number=str(number)
    return int(number[2:])

def generate_ppm_file(image_size,gen,points_number,state_number,value):
    integer_part=int(value)
    decimal_part=get_decimal_part(value)
    file_name=f"img{state_number}_{integer_part}-{decimal_part}.ppm"
    file=open(file_name,"w")
    





    
def draw():
    if len(sys.argv) < 4:
        print("Usage : ./draw.py image_size points_number decimal_places_number")
        print("image_size denotes the image size and it should be greater than 100")
        print("points_number denotes the number of points and it should be greater than 100")
        print("decimal_places_number denotes the number of decimal places and it should be between 1 and 5")
    image_size=sys.argv[1]
    points_number=sys.argv[2]
    decimal_places_number=sys.argv[3]
    for i in range(1,11):
        tmp=int((i*points_number)/10)
        gen,value=estimate(tmp)
        value=round(value,decimal_places_number)
        generate_ppm_file(image_size,gen,tmp,i,value)





if __name__=="__main__":
    draw()