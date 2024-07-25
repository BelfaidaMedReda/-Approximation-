#!/usr/bin/env python3 
"""
    This script provides an approximative value of π through Monte Carlo method
"""
import sys 
from random import uniform

def number_generator(n:int):
    for _ in range(n):
        x=uniform(-1,1)
        y=uniform(-1,1)
        yield (x,y)

def in_circle(point:tuple):
    x,y=point
    return x**2+y**2 <= 1 

def estimate(points_number):
    gen=number_generator(points_number)
    points=[]
    count = 0
    for point in gen:
        points.append(point)
        if in_circle(point):
            count+=1
    return points,(4*count)/points_number

def main():
    if len(sys.argv) < 2:
        print("Usage : ./monte_carlo.py points_number")
        print("points_number designates the number of points ")
        sys.exit(1)
    points_number= int(sys.argv[1])
    print(f"An estimation of π by {points_number} points : ",estimate(points_number)[1])    

if __name__=="__main__":
    main()