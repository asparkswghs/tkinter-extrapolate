""" Functions for Drawing complex items to the canvas """
# Copyright (c) 2024 Austen Sparks
#   Subject to the terms of the MIT License, see LICENSE for details.
import tkinter
from typing import Dict

padding = 20
start = 12.5
max_points = 20
gridline_fill = '#d3d3d3'

def graph(canvas: tkinter.Canvas, max_x: int, max_y: int) -> Dict[float, float]:
    """ Draw an all-positive line graph on the given `canvas`, given max possible x and y values.
    Returns int: width of 1 unit on graph """
    global padding
    global start
    global max_points
    global gridline_fill
    canvas.update()
    width = canvas.winfo_width() - padding
    height = canvas.winfo_height() - padding

    unit = {
        "x": width/max_x,
        "y": height/max_y,
    }
    pad = lambda x: x + padding

    # Step & Units
    if max_x > max_points or max_y > max_points:
        max_all = max([max_x, max_y])
        units = range(0, max_all+1)
        step = 1
        while len(units) > 25:
            step += 1
            units = range(0, max_all+step, step)
        
        units_x = range(0, max_x+step, step)
        units_y = range(0, max_y+step, step)
    else:
        units_x = range(0, max_x+1)
        units_y = range(0, max_y+1)

    # Vertical Axis
    for i in units_y:
        if i >= 0 and max_y - i >= 0:
            h = i*unit["y"] # Unit for Height, offset to show labels properly
            canvas.create_text(pad(0), h, text=f'{max_y - i}')
            canvas.create_line(pad(10), h, pad(15), h)
            canvas.create_line(pad(start), h, width+start, h, fill=gridline_fill)
    canvas.create_line(pad(start), 0, pad(start), max_y*unit["y"])

    # Horizontal Axis
    h = max_y*unit["y"] # Height for line
    canvas.create_line(pad(start), max_y*unit["y"], pad(max_x*unit["x"]), max_y*unit["y"])
    for i in units_x:
        if i > 0:
            w = i*unit["x"] # Unit for Width
            canvas.create_line(pad(w), h, pad(w), 0, fill=gridline_fill)
            canvas.create_text(pad(w), h, text=f'{i}')
    
    return unit

def extrapolate(canvas: tkinter.Canvas, unit: dict, points: dict, max_x: int, max_y: int) -> None:
    """ Draws line based on two points, with continued trajectory """
    global padding
    global start
    base_x = padding + start
    base_y = max_y * unit["y"]
    scale_x = lambda x: (base_x+(x*unit["x"])) - start # Scale coordinates to units on canvas
    scale_y = lambda x: base_y-(x*unit["y"])
    points_new = {
        "a": ( (scale_x(points["a"][0])), scale_y(points["a"][1]) ), # point a: (x, y)
        "b": ( (scale_x(points["b"][0])), scale_y(points["b"][1]) ), # point b: (x, y)
    }
    canvas.create_line(*points_new["a"], *points_new["b"], width=2) # Draws user-provided points
    for i in points_new: # Draw labels for points
        canvas.create_text(points_new[i][0], points_new[i][1]+10, text=i)
    # y = mx + b
    m = (points["a"][1] - points["b"][1]) / (points["a"][0] - points["b"][0]) # (rise, run)
    b =  points["a"][1] - (m*points["a"][0]) # b = y - mx
    y = lambda x: (m*x) + b
    x = lambda y: (y - b) / m
    corr_x = unit["x"] - start # Corrections, because the drawn line is predictably off
    if m == 0:
        points_extr = {
            "a": ( scale_x(0), scale_y(y(max_x)) ),
            "b": ( scale_x(max_x)+corr_x, scale_y(y(max_x)) ),
        }
    else:
        points_extr = {
            "a": ( scale_x(x(0)), scale_y(0) ), # this stays the same, no need to recalculate
            "b": ( scale_x(max_x)+corr_x, scale_y(y(max_x)) ), # Calculate point of farthest possible X on graph
        }
    canvas.create_line(*points_extr["a"], *points_extr["b"], dash=(3,1)) # Draws new projected points