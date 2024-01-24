# Functions for Drawing complex items to the canvas
import tkinter
from typing import Dict

def graph(canvas: tkinter.Canvas, max_x: int, max_y: int) -> Dict[float, float]:
    """ Draw an all-positive line graph on the given `canvas`, given max possible x and y values.
    Returns int: width of 1 unit on graph """
    canvas.update()
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    unit = {
        "x": width/max_x,
        "y": height/max_y,
    }

    # Vertical Axis
    for i in range(0, max_y+1):
        h = i*unit["y"] # Unit for Height, offset to show labels properly
        canvas.create_text(5, h, text=f'{max_y - i}')
        canvas.create_line(10, h, 15, h)
    canvas.create_line(12.5, 0, 12.5, max_y*unit["y"])

    # Horizontal Axis
    for i in range(0, max_x+1):
        w = i*unit["x"] # Unit for Width
        canvas.create_text