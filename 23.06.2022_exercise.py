from tkinter import *
from tkinter import ttk


def bmi_calc(*args):
    bmi_height = int(height_entry.get())
    bmi_weight = int(weight_entry.get())
    result.set(f'{bmi_weight / ((bmi_height/100)**2):.2f}')


main_window = Tk()
main_window.title('BMI Calculator')

height = StringVar()
height_entry = ttk.Entry(main_window, textvariable=height, width=10)
height_entry.grid(column=1, row=0)
height_label = ttk.Label(main_window, text='Input your height in cm:')
height_label.grid(column=0, row=0)

weight = StringVar()
weight_entry = ttk.Entry(main_window, textvariable=weight, width=10)
weight_entry.grid(column=1, row=1)
weight_label = ttk.Label(main_window, text='Input your weight in kg:')
weight_label.grid(column=0, row=1)

calc_button = ttk.Button(main_window, text='Calculate', command=bmi_calc)
calc_button.grid(column=1, row=2)

main_window.bind('<Return>', bmi_calc)

result = StringVar()
ttk.Label(main_window, textvariable=result).grid(column=0, row=3)

height_entry.focus()
main_window.mainloop()
