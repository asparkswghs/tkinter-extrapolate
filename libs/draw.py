# Functions for Drawing complex items to the canvas
import tkinter
from typing import Dict

padding = 10
start = 12.5

def graph(canvas: tkinter.Canvas, max_x: int, max_y: int) -> Dict[float, float]:
    """ Draw an all-positive line graph on the given `canvas`, given max possible x and y values.
    Returns int: width of 1 unit on graph """
    global padding
    global start
    canvas.update()
    width = canvas.winfo_width() - padding
    height = canvas.winfo_height() - padding

    unit = {
        "x": width/max_x,
        "y": height/max_y,
    }
    pad = lambda x: x + padding

    # Vertical Axis
    for i in range(0, max_y+1):
        h = i*unit["y"] # Unit for Height, offset to show labels properly
        canvas.create_text(5, h, text=f'{max_y - i}')
        canvas.create_line(10, h, 15, h)
    canvas.create_line(start, 0, start, max_y*unit["y"])

    # Horizontal Axis
    h = max_y*unit["y"] # Height for line
    canvas.create_line(start, max_y*unit["y"], max_x*unit["x"], max_y*unit["y"])
    for i in range(0, max_x+1):
        w = i*unit["x"] # Unit for Width
        canvas.create_text(w, h, text=f'{i}')
    
    return unit

def extrapolate(canvas: tkinter.Canvas, unit: dict, points: dict, max_x: int, max_y: int):
    """ Draws line based on two points, with continued trajectory """
    global padding
    global start
    points_new = {
        "a": (max_x*unit["x"]-points["a"][0], max_y*unit["y"]-points["a"][1]), # point a: (x, y)
        "b": (max_x*unit["x"]-points["b"][0], max_y*unit["y"]-points["b"][1]), # point a: (x, y)
    }
    canvas.create_line(*points_new["a"], *points_new["b"], width=4)
    canvas.create_line(*points_new["a"], points_new["b"][0]*1000, points_new["b"][1]*1000)