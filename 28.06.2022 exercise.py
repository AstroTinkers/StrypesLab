from tkinter import *


def num_press(num):
    global expression
    expression = expression + str(num)
    equation.set(expression)


def equals_to():
    global expression
    result = str(eval(expression))
    equation.set(result)
    expression = ""


def num_clear():
    global expression
    expression = ""
    equation.set("")


main_window = Tk()
main_window.title("Calculator")
main_window.iconbitmap('calc.ico')
main_window.configure(background='dark gray')
main_window.geometry("300x400")
equation = StringVar()
expression = ""

# Display row
display = Entry(main_window, textvariable=equation, justify=CENTER, width=30, relief=RAISED)
display.grid(columnspan=4, sticky='nsew', pady=5, padx=5)
num_equal = Button(main_window, text="=", height=1, width=5, padx=5, pady=3, relief=RAISED, command=lambda: equals_to())
num_equal.grid(column=3, row=0)

# Numbers
# Row 1
num_1 = Button(main_window, text="1", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("1"),
               background='dark blue', foreground='white')
num_1.grid(column=0, row=5, sticky=W)
num_2 = Button(main_window, text="2", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("2"))
num_2.grid(column=1, row=5)
num_3 = Button(main_window, text="3", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("3"),
               background='dark blue', foreground='white')
num_3.grid(column=2, row=5)
num_plus = Button(main_window, text="+", height=1, width=5, padx=3, pady=1, relief=RAISED,
                  command=lambda: num_press("+"))
num_plus.grid(column=3, row=5)

# Row 2
num_4 = Button(main_window, text="4", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("4"),
               background='dark blue', foreground='white')
num_4.grid(column=0, row=4, sticky=W)
num_5 = Button(main_window, text="5", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("5"))
num_5.grid(column=1, row=4)
num_6 = Button(main_window, text="6", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("6"),
               background='dark blue', foreground='white')
num_6.grid(column=2, row=4)
num_minus = Button(main_window, text="-", height=1, width=5, padx=3, pady=1, relief=RAISED,
                   command=lambda: num_press("-"))
num_minus.grid(column=3, row=4)

# Row 3
num_7 = Button(main_window, text="7", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("7"),
               background='dark blue', foreground='white')
num_7.grid(column=0, row=3, sticky=W)
num_8 = Button(main_window, text="8", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("8"))
num_8.grid(column=1, row=3)
num_9 = Button(main_window, text="9", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("9"),
               background='dark blue', foreground='white')
num_9.grid(column=2, row=3)
num_c = Button(main_window, text="C", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_clear())
num_c.grid(column=3, row=3)


main_window.mainloop()
