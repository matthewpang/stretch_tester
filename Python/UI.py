__author__ = 'matthewpang'
from Tkinter import *
import pickle
import time

root = Tk()
root.title("Stretch Test Interface")

# Define Frame
control_frame = Frame(root)
button_frame = Frame(control_frame)
mode_frame = Frame(control_frame)
switch_frame = Frame(control_frame)

slider_frame = Frame(root)

reset = IntVar()


def resetter(dump):
    reset.set(1)

def simple_defaults():
    initial_displacement.set(0)
    stretch_length.set(0)
    zero_stretch_delay.set(0)
    max_stretch_delay.set(0)


#ON/OFF SWITCH

spacer = Canvas(root, width=30, height=1)
spacer.pack(side=LEFT)
on_off = IntVar()
Canvas(switch_frame, width=1, height=1).pack()
Checkbutton(switch_frame, text="ON/OFF", variable=on_off, font="TimesNewRoman 44 bold").pack()
switch_frame.pack()

#Mode Selection

spacer = Canvas(control_frame, width=1, height=10)
spacer.pack()
mode_label = Label(mode_frame, text="Mode", font="TimesNewRoman 30 bold").pack()
Canvas(mode_frame, width=1, height=1).pack()
mode = IntVar()
Radiobutton(mode_frame, text="Simple", variable=mode, value=0, command=simple_defaults,
            font="TimesNewRoman 28").pack()
Canvas(mode_frame, width=1, height=1).pack()
mode_frame.pack()

#Control Buttons

Canvas(control_frame, width=1, height=10).pack()
golabel = Label(button_frame, text="Go To", font="TimesNewRoman 30 bold").pack()
button_frame.pack()
Canvas(button_frame, width=1, height=1).pack()
go_zero = IntVar()
go_zero.set(0)
def go_zero_setter():
    go_zero.set(1)
Button(button_frame, text=" Zero", command=go_zero_setter, font="TimesNewRoman 28").pack()
Canvas(button_frame, width=1, height=1).pack()
go_min = IntVar()
go_min.set(0)
def go_min_setter():
    go_min.set(1)
Button(button_frame, text="Min Stretch", command=go_min_setter, font="TimesNewRoman 28").pack()
Canvas(button_frame, width=1, height=1).pack()
go_max = IntVar()
go_max.set(0)

def go_max_setter():
    go_max.set(1)
Button(button_frame, text="Max Stretch", command=go_max_setter, font="TimesNewRoman 28").pack()
Canvas(button_frame, width=1, height=1).pack()

v_zero = IntVar()
v_zero.set(0)

reset = IntVar()
reset.set(0)
def reset_setter():
    reset.set(1)

Button(button_frame, text="Home & Reset", command=reset_setter,font="TimesNewRoman 28").pack()
Canvas(button_frame, width=1, height=30).pack()
control_frame.pack(side=LEFT)

#Sliders

initial_displacement = Scale(slider_frame, from_=0, to=4000, orient=HORIZONTAL, resolution=10, tickinterval=500, length=1000,
                   label="Initial Displacement (mils)", width=45, font="TimesNewRoman 12 bold")
initial_displacement.set(0)
initial_displacement.pack()

stretch_length = Scale(slider_frame, from_=0, to=4000, orient=HORIZONTAL, resolution=10, tickinterval=500, length=1000,
                   label="Stretch Length (mils)", width=45, font="TimesNewRoman 12 bold")
stretch_length.set(0)
stretch_length.pack()

zero_stretch_delay = Scale(slider_frame, from_=0, to=300, orient=HORIZONTAL, resolution=0.5,tickinterval=60, length=1000,
                     label="Wait at Zero Stretch (seconds)", width=45, font="TimesNewRoman 12 bold")
zero_stretch_delay.set(0)
zero_stretch_delay.pack()

max_stretch_delay = Scale(slider_frame, from_=0, to=300, orient=HORIZONTAL, resolution=0.5,tickinterval=60, length=1000,
                     label="Wait at Maximum Stretch (seconds)", width=45, font="TimesNewRoman 12 bold")
max_stretch_delay.set(0)
max_stretch_delay.pack()


spacer = Canvas(root, width=30, height=1)
spacer.pack(side=LEFT)

slider_frame.pack(side=LEFT)

spacer = Canvas(root, width=30, height=500)
spacer.pack(side=LEFT)


def write():
    file = open('stream', 'r+')
    a = [0]*11
    a[0] = on_off.get()
    a[1] = v_zero.get()
    a[2] = stretch_length.get()
    a[3] = initial_displacement.get()
    a[4] = zero_stretch_delay.get()
    a[5] = max_stretch_delay.get()
    a[6] = go_max.get()
    a[7] = go_min.get()
    a[8] = go_zero.get()
    a[9] = mode.get()
    a[10] = reset.get()
    pickle.dump(a, file)

    root.after(100, write)


def button_reset():
    if go_max.get() == 1:
        go_max.set(0)
    if go_min.get() == 1:
        go_min.set(0)
    if go_zero.get() == 1:
        go_zero.set(0)
    if reset.get() == 1:
        reset.set(0)

    root.after(250, button_reset)


root.after(100, write)
root.after(500, button_reset)
root.mainloop()
