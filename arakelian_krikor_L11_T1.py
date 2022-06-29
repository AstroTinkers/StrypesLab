import tkinter
from tkinter import *
from tkinter import ttk


def bmi_calc():
    # Function to calculate the BMI index
    bmi_height = int(height_entry.get())
    bmi_weight = int(weight_entry.get())
    result.set(f'{bmi_weight / ((bmi_height/100)**2):.2f}')


def update_graph(graphs, res):
    # Function to update graph image
    if res:
        graph_values = [18.5, 25, 30, 35, 40]
        for bmi_index in graph_values:
            if res < bmi_index:
                index = graph_values.index(bmi_index) + 1
                break
        else:
            index = 6
        graphs.configure(image=graphics[index], justify=CENTER, background=MAIN_COLOR)


# Main window of app
main_window = Tk()
main_window.title('BMI Calculator')
MAIN_COLOR = '#26a69a'
main_window.configure(background=MAIN_COLOR)
frame = tkinter.Frame(main_window, width=420, height=200, background=MAIN_COLOR)
frame.grid(columnspan=2, rowspan=5, sticky='nwe')
frame.columnconfigure(0, weight=3)
# Main window icon
main_window.iconbitmap('./BMI/bmi_icon.ico')
# Main window dimensions
mw_height = 400
mw_width = 420
# Center main window on the screen
screen_w = main_window.winfo_screenwidth()
screen_h = main_window.winfo_screenheight()
scr_center_x = int(screen_w / 2 - mw_width / 2)
scr_center_y = int(screen_h / 2 - mw_height / 2)
main_window.geometry(f'{mw_width}x{mw_height}+{scr_center_x}+{scr_center_y}')
# Prevent resizing of app window
main_window.resizable(False, False)

# Input labels and fields
height_label = Label(main_window, bg=MAIN_COLOR, fg='white', font='Verdana', text='Please input you height in cm:')
height_label.grid(column=0, row=0, sticky='w', padx=6, pady=2)
weight_label = Label(main_window, bg=MAIN_COLOR, fg='white', font='Verdana', text='Please input you weight in kg:')
weight_label.grid(column=0, row=1, sticky='w', padx=6, pady=2)

height = StringVar()
height_entry = Entry(main_window, bg='white', bd=4, font='Verdana', justify='right', width=4)
height_entry.grid(column=1, row=0, sticky='e', padx=6, pady=2)
weight_entry = Entry(main_window, bg='white', bd=4, font='Verdana', justify='right', width=4)
weight_entry.grid(column=1, row=1, sticky='e', padx=6, pady=2)

# Button to calculate BMI index
calc_button = Button(main_window, text='Calculate',
                     font='Verdana', command=lambda: [bmi_calc(), update_graph(graph_label, float(result.get()))],
                     height=1, relief=RAISED, justify=CENTER)
calc_button.grid(column=0, columnspan=2, row=2, sticky='we', padx=6, pady=4)
# Bind 'Enter' key to Calculate button
main_window.bind('<Return>', lambda x: [bmi_calc(), update_graph(graph_label, float(result.get()))])


# Images to show
graphics = [PhotoImage(file=f"./BMI/{i}.png") for i in range(0, 7)]
graph_label = Label(main_window)
graph_label.grid(column=0, columnspan=3, row=3, padx=1, pady=4)
graph_label.configure(image=graphics[0], justify=CENTER, background=MAIN_COLOR)

result = StringVar()
ttk.Label(main_window, textvariable=result, font='Verdana', foreground='white', background=MAIN_COLOR, justify=CENTER) \
    .grid(column=0, columnspan=3, row=4, padx=6, pady=4)

# Set the cursor to the first input upon starting the app
height_entry.focus()
main_window.mainloop()
