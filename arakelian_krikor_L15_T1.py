import tkinter.filedialog
from tkinter import *

import PIL.Image
from PIL import ImageTk, Image, ImageFilter, ImageOps


def open_file():
    global imagedata
    global file_opened
    file = tkinter.filedialog.askopenfile(filetypes=[("Images", "*.jpg")])
    if file:
        imagedata = ImageOps.contain(Image.open(file.name), (500, 500))
        image_info.config(text=f"Mode: {imagedata.mode}\nSize: {imagedata.size}\nWidth: {imagedata.width}\nHeight: "
                               f"{imagedata.height}")
        image_displayed = ImageTk.PhotoImage(imagedata)
        image.configure(image=image_displayed, width=500, height=500)
        image.image = image_displayed
        file_opened = True


def image_ops(filter_passed, image_arg):
    global imagedata
    img_new = image_arg.filter(filter_passed)
    imagedata = img_new
    img_displayed = ImageTk.PhotoImage(img_new)
    image.config(image=img_displayed)
    image.image = img_displayed


def rotate_img(degrees, img_passed):
    global imagedata
    try:
        img_new = img_passed.rotate(degrees)
        imagedata = img_new
        img_displayed = ImageTk.PhotoImage(img_new)
        image.config(image=img_displayed)
        image.image = img_displayed
    except (FileNotFoundError, AttributeError):
        pass


def button_state(file_state):
    if file_state:
        for widget in frame.winfo_children():
            if isinstance(widget, tkinter.Button):
                widget.config(state=NORMAL)


main_window = Tk()
imagedata = PIL.Image.Image()
img = PhotoImage()
file_opened = False
main_window.title("Image editor")
main_window.geometry("1090x600")
frame = Frame(main_window)
frame.grid(row=0, column=0)
browse = Button(frame, text="Browse", command=lambda: [open_file(), button_state(file_opened)])
browse.grid(row=3, column=1)
rotate_clock_b = Button(frame, text="Rotate Clockwise", command=lambda: rotate_img(-90, imagedata), width=20,
                        state=DISABLED)
rotate_clock_b.grid(row=3, column=0)
rotate_anti_clock_b = Button(frame, text="Rotate Anti Clockwise", command=lambda: rotate_img(90, imagedata), width=20,
                             state=DISABLED)
rotate_anti_clock_b.grid(row=3, column=2)
image = Label(frame, image=img, width=500, height=500, relief=RIDGE)
image.grid(row=2, column=0)
image_info = Label(frame, text=f"Mode: \nSize: \nWidth: \nHeight: ", image=img, compound=CENTER, width=500, height=500,
                   relief=RIDGE)
image_info.grid(row=2, column=2)
blur_b = Button(frame, text="Blur", command=lambda: image_ops(ImageFilter.BLUR, imagedata), width=10, state=DISABLED)
blur_b.grid(row=0, column=0)
cont_b = Button(frame, text="Contour", command=lambda: image_ops(ImageFilter.CONTOUR, imagedata), width=10,
                state=DISABLED)
cont_b.grid(row=0, column=1)
detail_b = Button(frame, text="Detail", command=lambda: image_ops(ImageFilter.DETAIL, imagedata), width=10,
                  state=DISABLED)
detail_b.grid(row=0, column=2)
edge_en_b = Button(frame, text="Edge Enhance", command=lambda: image_ops(ImageFilter.EDGE_ENHANCE, imagedata), width=10,
                   state=DISABLED)
edge_en_b.grid(row=1, column=0)
emb_b = Button(frame, text="Emboss", command=lambda: image_ops(ImageFilter.EMBOSS, imagedata), width=10, state=DISABLED)
emb_b.grid(row=1, column=1)
edge_en_m_b = Button(frame, text="Edge More", command=lambda: image_ops(ImageFilter.EDGE_ENHANCE_MORE, imagedata),
                     width=10, state=DISABLED)
edge_en_m_b.grid(row=1, column=2)

main_window.mainloop()
