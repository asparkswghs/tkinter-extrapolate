#!/usr/bin/env python3
# Copyright (c) 2024 Austen Sparks
#   Subject to the terms of the MIT License, see LICENSE for details.
import re
import tkinter as tk

from libs import draw

# Init Values
a_x, a_y, b_x, b_y = 0, 0, 0, 0
winsize = (900, 600,)

# Functions
def validate(P) -> bool:
    """ Validates Entry boxes, to only contain integers """
    if str.isdigit(P) or P == "":
        return True
    else:
        return False

def refresh_coords() -> None:
    global a_x, a_y, b_x, b_y
    digit = lambda x: x if str.isdigit(x) else 0 # Sets values to 0 if they aren't an int; e.g. if it's empty
    a_x = int(digit(entries["a"]["x"].get()))
    a_y = int(digit(entries["a"]["y"].get()))
    b_x = int(digit(entries["b"]["x"].get()))
    b_y = int(digit(entries["b"]["y"].get()))

def callback_draw(*args, manual=False) -> None:
    """ Clears and draws to the Canvas """
    global winsize
    newsize = (window.winfo_width(), window.winfo_height(),)
    if winsize != newsize: # Window has been resized, continue with draw
        winsize = newsize
    elif manual: # Was manually called, draw anyways
        refresh_coords()
    else: # Was neither resized nor manually called, don't redraw.
        return
        
    global a_x, a_y, b_x, b_y

    if a_x == 0 and a_y == 0 and b_x == 0 and b_y == 0: # If all values are 0 (i.e. empty) just reset the canvas
        canvas.delete('all')
        draw.graph(canvas, 10, 10)
        return

    addscale = lambda x: x+50 if (x+50)<=400 else x # Adds extra space to graph for extrapolated data

    max_x = addscale(max([a_x, b_x])) # Determine the max needed sizes for X and Y sides
    max_y = addscale(max([a_y, b_y]))

    canvas.delete('all')
    unit = draw.graph(canvas, max_x, max_y) # Create the graph with appropriate sizing
    draw.extrapolate( # Draw the line and projected line
        canvas,
        unit,
        {
            "a": (a_x, a_y,),
            "b": (b_x, b_y,),
        },
        max_x,
        max_y
    )

def callback_button() -> None:
    """ Refreshes values and draws graph, callback for button """
    refresh_coords()
    callback_draw(manual=True)


# Window Properties
window = tk.Tk()
window.geometry("901x601") # See XXX near EOF
window.minsize(600, 400)
window.title("Data Extrapolator")
window.bind('<Configure>', callback_draw)
window.grid_rowconfigure(5, weight=1)    # Ensure row/column for canvas can expand to fill window
window.grid_columnconfigure(0, weight=1) # 

call_validate = window.register(validate) # Register Validation Function

# Entries
entries = {"a": None, "b": None}
for i in entries: # Create coordinate entries
    entries[i] = {
        "x": tk.Entry(window,  validate='all', validatecommand=(call_validate, '%P')),
        "y": tk.Entry(window,  validate='all', validatecommand=(call_validate, '%P'))
    }

# Labels
label_instr = tk.Label(window, text='Data Extrapolator\nExtrapolates data based on the 2 points provided.')

for i in entries: # Create coordinate labels
    entries[i]["label"] = tk.Label(window, text=f'{i} = ')
    entries[i]["("] = tk.Label(window, text='(')
    entries[i][","] = tk.Label(window, text=',')
    entries[i][")"] = tk.Label(window, text=')')

# Buttons
button = tk.Button(window, text='Extrapolate', command=callback_button)

# Canvas
canvas = tk.Canvas(window)

# Grid
label_instr.grid(column=1, row=0, columnspan=5)

# 0         | 1    | 2     | 3   | 4     | 5     | 6
# <spacing> | label | "("" | entry | "," | entry | ")"
#  ^- to allow for canvas to expand to fill window
row = 1
for i in entries: # Append coordinate entries to grid
    entries[i]["label"].grid(column=1, row=row)
    entries[i]["("].grid(column=2, row=row)
    entries[i]["x"].grid(column=3, row=row)
    entries[i][","].grid(column=4, row=row)
    entries[i]["y"].grid(column=5, row=row)
    entries[i][")"].grid(column=6, row=row)
    row += 1

button.grid(column=2, row=4, columnspan=4)

canvas.grid(column=0, row=5, columnspan=100, sticky='nsew') # Add canvas, being able to expand when the window extends

# Present Window
draw.graph(canvas, 10, 10)
window.update()
window.geometry("900x600") # XXX: Workaround for a bug where labels and buttons are not visible until the window is resized.
window.mainloop()
