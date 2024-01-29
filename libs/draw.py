# Functions for Drawing complex items to the canvas
import tkinter
from typing import Dict

padding = 20
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

    # Step & Units
    if max_x > 20 or max_y > 20:
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
            canvas.create_text(pad(5), h, text=f'{max_y - i}')
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

def extrapolate(canvas: tkinter.Canvas, unit: dict, points: dict, max_x: int, max_y: int):
    """ Draws line based on two points, with continued trajectory """
    global padding
    global start
    base_x = padding + start
    base_y = max_y * unit["y"]
    scale_x = lambda x: x*unit["x"]
    scale_y = lambda x: x*unit["y"]
    points_new = {
        "a": ( (base_x+scale_x(points["a"][0])), base_y-scale_y(points["a"][1]) ), # point a: (x, y)
        "b": ( (base_x+scale_x(points["b"][0])), base_y-scale_y(points["b"][1]) ), # point b: (x, y)
    }
    print(points_new) #TODO
    canvas.create_line(*points_new["a"], *points_new["b"], width=3)
    ext_const = 1000000
    canvas.create_line(*points_new["a"], points_new["b"][0]*(ext_const*unit["x"]), points_new["b"][1]*(ext_const*unit["y"]))