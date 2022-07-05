from tkinter import *


def num_press(num):
    global display_num
    if display_num == "0":
        display_num = ""
    display_num = display_num + str(num)
    display.delete("1.0", "end")
    display.insert("1.0", display_num)


def equals_to():
    global display_num
    try:
        result = str(eval(display_num))
    except ZeroDivisionError:
        result = "0"
    display_num = result
    display.delete("1.0", "end")
    display.insert("1.0", result)


def num_clear_all():
    global display_num
    display_num = ""
    display.delete("1.0", "end")


def num_clear_entry():
    global display_num
    display_num2 = ""
    for num in display_num[::-1]:
        if num.isnumeric():
            display_num2 = display_num[:display_num.index(num)]
        else:
            break
    display_num = display_num2
    display.delete("1.0", "end")
    display.insert("1.0", display_num)


def memory_clear():
    global memory
    memory = ""


def memory_plus():
    global memory
    global display_num
    display_num2 = ""
    if display_num[0] == "-" and len(display_num) > 0:
        for num in display_num[1:]:
            if num.isdigit():
                display_num2 = display_num[:display_num.index(num)+1]
            else:
                break
    else:
        for num in display_num:
            if num.isdigit():
                display_num2 = display_num[:display_num.index(num)+1]
            else:
                break
    display_num = display_num2
    if memory != "":
        memory = str(int(memory) + int(display_num))
    else:
        memory = str(display_num)
    display_num = ""


def memory_minus():
    global memory
    global display_num
    memory = int(memory) - int(display_num)
    display_num = ""


def memory_recall():
    global memory
    global display_num
    if display_num != "":
        if display_num[-1].isnumeric():
            display_num = memory
        else:
            display_num = str(display_num) + str(memory)
    else:
        display_num = str(memory)
    display.delete("1.0", "end")
    display.insert("1.0", display_num)


def memory_switch():
    global memory
    if memory == "":
        num_mc["state"] = DISABLED
        num_m_minus["state"] = DISABLED
        num_m_recall["state"] = DISABLED
    else:
        num_mc["state"] = NORMAL
        num_m_minus["state"] = NORMAL
        num_m_recall["state"] = NORMAL


def change_sign():
    global display_num
    if display_num[0] == "-":
        display_num = str(display_num[1:])
    else:
        display_num = "-" + str(display_num)
    display.delete("1.0", "end")
    display.insert("1.0", display_num)


def factorial():
    global display_num
    if display_num == "" or eval(display_num) == 0:
        display_num = "0"
    else:
        prod = 1
        for i in range(1, eval(display_num)+1):
            prod = prod * i
        display_num = str(prod)
    display.delete("1.0", "end")
    display.insert("1.0", display_num)


# Global colors
BACKGROUND = "#1c1c1c"
BUTTONS = "#858585"
FONT = "#ececec"


main_window = Tk()
main_window.title("Calculator")
main_window.iconbitmap("calc.ico")
main_window.configure(background=BACKGROUND)
main_window.resizable(False, False)
equation = StringVar()
display_num = ""
expression = ""
memory = ""

# Display row
display = Text(main_window, height=2, width=27, relief=RAISED, bg=FONT, fg=BACKGROUND, padx=3, pady=1)
display.grid(columnspan=4, pady=3, padx=1)
num_equal = Button(main_window, text="=", height=1, width=5, padx=5, pady=5, relief=RAISED, command=lambda: equals_to(),
                   bg=FONT, fg=BACKGROUND)
num_equal.grid(column=4, row=0, padx=5, pady=5)

# Calculator layout
# Row 0
num_mc = Button(main_window, text="MC", height=1, width=5, padx=3, pady=1, relief=RAISED, state=DISABLED,
                command=lambda: [memory_clear(), memory_switch()], bg=BUTTONS, fg=FONT)
num_mc.grid(column=0, row=2, padx=5, pady=5)
num_m_plus = Button(main_window, text="M+", height=1, width=5, padx=3, pady=1, relief=RAISED, state=NORMAL,
                    command=lambda: [memory_plus(), memory_switch()], bg=BUTTONS, fg=FONT)
num_m_plus.grid(column=1, row=2, padx=5, pady=5)
num_m_minus = Button(main_window, text="M-", height=1, width=5, padx=3, pady=1, relief=RAISED, state=DISABLED,
                     command=lambda: [memory_minus()], bg=BUTTONS, fg=FONT)
num_m_minus.grid(column=2, row=2, padx=5, pady=5)
num_m_recall = Button(main_window, text="MR", height=1, width=5, padx=3, pady=1, relief=RAISED, state=DISABLED,
                      command=lambda: [memory_recall(), memory_switch()], bg=BUTTONS, fg=FONT)
num_m_recall.grid(column=3, row=2, padx=5, pady=5)
num_fact = Button(main_window, text="x!", height=1, width=5, padx=3, pady=1, relief=RAISED,
                  command=lambda: factorial(), bg=BUTTONS, fg=FONT)
num_fact.grid(column=4, row=2, padx=5, pady=5)


# Row 1
num_7 = Button(main_window, text="7", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("7"),
               bg=BUTTONS, fg=FONT)
num_7.grid(column=0, row=3, padx=5, pady=5)
num_8 = Button(main_window, text="8", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("8"),
               bg=BUTTONS, fg=FONT)
num_8.grid(column=1, row=3, padx=5, pady=5)
num_9 = Button(main_window, text="9", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("9"),
               bg=BUTTONS, fg=FONT)
num_9.grid(column=2, row=3, padx=5, pady=5)
num_c = Button(main_window, text="C", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_clear_all(),
               bg=BUTTONS, fg=FONT)
num_c.grid(column=3, row=3, padx=5, pady=5)
num_ce = Button(main_window, text="CE", height=1, width=5, padx=3, pady=1, relief=RAISED,
                command=lambda: num_clear_entry(), bg=BUTTONS, fg=FONT)
num_ce.grid(column=4, row=3, padx=5, pady=5)

# Row 2
num_4 = Button(main_window, text="4", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("4"),
               bg=BUTTONS, fg=FONT)
num_4.grid(column=0, row=4, sticky=W, padx=5, pady=5)
num_5 = Button(main_window, text="5", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("5"),
               bg=BUTTONS, fg=FONT)
num_5.grid(column=1, row=4, padx=5, pady=5)
num_6 = Button(main_window, text="6", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("6"),
               bg=BUTTONS, fg=FONT)
num_6.grid(column=2, row=4, padx=5, pady=5)
num_minus = Button(main_window, text="-", height=1, width=5, padx=3, pady=1, relief=RAISED,
                   command=lambda: num_press("-"), bg=BUTTONS, fg=FONT)
num_minus.grid(column=3, row=4, padx=5, pady=5)
num_sqrt = Button(main_window, text="\u221Ax", height=1, width=5, padx=3, pady=1, relief=RAISED,
                  command=lambda: num_press("**0.5"), bg=BUTTONS, fg=FONT)
num_sqrt.grid(column=4, row=4, padx=5, pady=5)

# Row 3
num_1 = Button(main_window, text="1", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("1"),
               bg=BUTTONS, fg=FONT)
num_1.grid(column=0, row=5, sticky=W, padx=5, pady=5)
num_2 = Button(main_window, text="2", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("2"),
               bg=BUTTONS, fg=FONT)
num_2.grid(column=1, row=5, padx=5, pady=5)
num_3 = Button(main_window, text="3", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("3"),
               bg=BUTTONS, fg=FONT)
num_3.grid(column=2, row=5, padx=5, pady=5)
num_plus = Button(main_window, text="+", height=1, width=5, padx=3, pady=1, relief=RAISED,
                  command=lambda: num_press("+"), bg=BUTTONS, fg=FONT)
num_plus.grid(column=3, row=5, padx=5, pady=5)
num_pow = Button(main_window, text="x\u00B2", height=1, width=5, padx=3, pady=1, relief=RAISED,
                 command=lambda: num_press("**2"), bg=BUTTONS, fg=FONT)
num_pow.grid(column=4, row=5, padx=5, pady=5)

# Row 4
num_0 = Button(main_window, text="0", height=1, width=5, padx=3, pady=1, relief=RAISED, command=lambda: num_press("0"),
               bg=BUTTONS, fg=FONT)
num_0.grid(column=0, row=6, sticky=W, padx=5, pady=5)
num_dot = Button(main_window, text=".", height=1, width=5, padx=3, pady=1, relief=RAISED,
                 command=lambda: num_press("."), bg=BUTTONS, fg=FONT)
num_dot.grid(column=1, row=6, padx=5, pady=5)
num_change_sign = Button(main_window, text="+/-", height=1, width=5, padx=3, pady=1, relief=RAISED,
                         command=lambda: change_sign(), bg=BUTTONS, fg=FONT)
num_change_sign.grid(column=2, row=6, padx=5, pady=5)
num_div = Button(main_window, text="/", height=1, width=5, padx=3, pady=1, relief=RAISED,
                 command=lambda: num_press("/"), bg=BUTTONS, fg=FONT)
num_div.grid(column=3, row=6, padx=5, pady=5)
num_mult = Button(main_window, text="x", height=1, width=5, padx=3, pady=1, relief=RAISED,
                  command=lambda: num_press("*"), bg=BUTTONS, fg=FONT)
num_mult.grid(column=4, row=6, padx=5, pady=5)
main_window.mainloop()
