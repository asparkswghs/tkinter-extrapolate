# Functions for Drawing complex items to the canvas
import tkinter
from typing import Dict

padding = 20
start = 12.5
max_points = 20

def graph(canvas: tkinter.Canvas, max_x: int, max_y: int) -> Dict[float, float]:
    """ Draw an all-positive line graph on the given `canvas`, given max possible x and y values.
    Returns int: width of 1 unit on graph """
    global padding
    global start
    global max_points
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
    canvas.create_line(pad(start), 0, pad(start), max_y*unit["y"])

    # Horizontal Axis
    h = max_y*unit["y"] # Height for line
    canvas.create_line(pad(start), max_y*unit["y"], pad(max_x*unit["x"]), max_y*unit["y"])
    for i in units_x:
        if i > 0:
            w = i*unit["x"] # Unit for Width
            canvas.create_text(pad(w), h, text=f'{i}')
    
    return unit

def extrapolate(canvas: tkinter.Canvas, unit: dict, points: dict, max_x: int, max_y: int) -> None:
    """ Draws line based on two points, with continued trajectory """
    global padding
    global start
    base_x = padding + start
    base_y = max_y * unit["y"]
    scale_x = lambda x: base_x+(x*unit["x"]) # Scale coordinates to units on canvas
    scale_y = lambda x: base_y-(x*unit["y"])
    points_new = {
        "a": ( (scale_x(points["a"][0])), scale_y(points["a"][1]) ), # point a: (x, y)
        "b": ( (scale_x(points["b"][0])), scale_y(points["b"][1]) ), # point b: (x, y)
    }
    print(points_new) #TODO
    canvas.create_line(*points_new["a"], *points_new["b"], width=3) # Draws user-provided points
    # y = mx + b
    m = (points["a"][1] - points["b"][1]) / (points["a"][0] - points["b"][0]) # (rise, run)
    b =  points["a"][1] - (m*points["a"][0]) # b = y - mx
    y = lambda x: (m*x) + b
    x = lambda y: (y - b) / m
    if m < 0: # Corrections, because the drawn line is predictably off
        corr_x = -1*unit["x"]
        corr_y = -1*unit["y"]
    else:
        corr_x = unit["x"]
        corr_y = unit["y"]
    points_extr = {
        "a": ( scale_x(x(0)), scale_y(0) ), # this stays the same, no need to recalculate
        "b": ( scale_x(max_x)+corr_x, scale_y(y(max_x))+corr_y ), # Calculate point of farthest possible X on graph
    }
    print(f'ext b: {points_extr["b"]}') #TODO
    canvas.create_line(*points_extr["a"], *points_extr["b"]) # Draws new projected points