import tkinter
from tkinter import *
from tkinter import ttk


def bmi_calc(*args):
    # Function to calculate the BMI index
    bmi_height = int(height_entry.get())
    bmi_weight = int(weight_entry.get())
    result.set(f'{bmi_weight / ((bmi_height/100)**2):.2f}')


def update_graph():
    # Function to update graph image
    global graph_L
    if result.get():
        if float(result.get()) < 18.5:
            graph_L.configure(image=graph_1, justify=CENTER, background='#26a69a')
        if float(result.get()) < 25:
            graph_L.configure(image=graph_2, justify=CENTER, background='#26a69a')
        if float(result.get()) < 30:
            graph_L.configure(image=graph_3, justify=CENTER, background='#26a69a')
        if float(result.get()) < 35:
            graph_L.configure(image=graph_4, justify=CENTER, background='#26a69a')
        if float(result.get()) < 40:
            graph_L.configure(image=graph_5, justify=CENTER, background='#26a69a')
        else:
            graph_L.configure(image=graph_6, justify=CENTER, background='#26a69a')


# Main window of app
main_window = Tk()
main_window.title('BMI Calculator')
main_window.configure(background='#26a69a')
frame = tkinter.Frame(main_window, width=400, height=200, background='#26a69a')
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
height_L = Label(main_window, bg='#26a69a', fg='white', font='Verdana', text='Please input you height in cm:')
height_L.grid(column=0, row=0, sticky='w', padx=6, pady=2)
weight_L = Label(main_window, bg='#26a69a', fg='white', font='Verdana', text='Please input you weight in kg:')
weight_L.grid(column=0, row=1, sticky='w', padx=6, pady=2)

height = StringVar()
height_entry = Entry(main_window, bg='white', bd=4, font='Verdana', justify='right', width=4)
height_entry.grid(column=1, row=0, sticky='e', padx=6, pady=2)
weight_entry = Entry(main_window, bg='white', bd=4, font='Verdana', justify='right', width=4)
weight_entry.grid(column=1, row=1, sticky='e', padx=6, pady=2)

# Button to calculate BMI index
calc_button = Button(main_window, text='Calculate', font='Verdana', command=lambda: [bmi_calc(), update_graph()],
                     height=1, relief=RAISED, justify=CENTER)
calc_button.grid(column=0, columnspan=2, row=2, sticky='we', padx=6, pady=4)
# Bind 'Enter' key to Calculate button
main_window.bind('<Return>', lambda x: [bmi_calc(), update_graph()])


# Images to show
graph_0 = PhotoImage(file='./BMI/0.png')
graph_1 = PhotoImage(file='./BMI/1.png')
graph_2 = PhotoImage(file='./BMI/2.png')
graph_3 = PhotoImage(file='./BMI/3.png')
graph_4 = PhotoImage(file='./BMI/4.png')
graph_5 = PhotoImage(file='./BMI/5.png')
graph_6 = PhotoImage(file='./BMI/6.png')
graph = graph_0
graph_L = Label(main_window)
graph_L.grid(column=0, columnspan=3, row=3, padx=1, pady=4)
graph_L.configure(image=graph, justify=CENTER, background='#26a69a')

result = StringVar()
ttk.Label(main_window, textvariable=result, font='Verdana', foreground='white', background='#26a69a', justify=CENTER) \
    .grid(column=0, columnspan=3, row=4, padx=6, pady=4)

# Set the cursor to the first input upon starting the app
height_entry.focus()
main_window.mainloop()
