#!/usr/bin/env python3
import tkinter as tk

from libs import draw

# Functions
def validate(P):
    """ Validates Entry boxes, to only contain integers """
    if str.isdigit(P) or P == "":
        return True
    else:
        return False

def callback_draw():
    """ Clears and draws to the Canvas """

    canvas.delete('all')
    draw.graph(canvas, 10, 10) #XXX

# Window
window = tk.Tk()
window.geometry("600x400")
window.minsize(600, 400)
window.title("Data Extrapolator")
window.grid_rowconfigure(5, weight=1)
window.grid_columnconfigure(0, weight=1)

call_validate = window.register(validate) # Register Validation Function

# Entries
entries = {"a": None, "b": None}
for i in entries:
    entries[i] = {
        "x": tk.Entry(window,  validate='all', validatecommand=(call_validate, '%P')),
        "y": tk.Entry(window,  validate='all', validatecommand=(call_validate, '%P'))
    }

# Labels
label_instr = tk.Label(window, text='Data Extrapolator\nExtrapolates data based on the 2 points provided.')

for i in entries:
    entries[i]["label"] = tk.Label(window, text=f'{i} = ')
    entries[i]["("] = tk.Label(window, text='(')
    entries[i][","] = tk.Label(window, text=',')
    entries[i][")"] = tk.Label(window, text=')')

# Buttons
button = tk.Button(window, text='Extrapolate', command=callback_draw)

# Canvas
canvas = tk.Canvas(window)

# Grid
label_instr.grid(column=1, row=0, columnspan=5)

# 0     | 1    | 2     | 3   | 4     | 5
# label | "("" | entry | "," | entry | ")"
row = 1
for i in entries:
    entries[i]["label"].grid(column=1, row=row)
    entries[i]["("].grid(column=2, row=row)
    entries[i]["x"].grid(column=3, row=row)
    entries[i][","].grid(column=4, row=row)
    entries[i]["y"].grid(column=5, row=row)
    entries[i][")"].grid(column=6, row=row)
    row += 1

button.grid(column=2, row=4, columnspan=4)

canvas.grid(column=0, row=5, columnspan=100, sticky='nsew')

# Present Window
draw.graph(canvas, 10, 10)
window.mainloop()
