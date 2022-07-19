import atexit
import os
import tkinter.filedialog
from tkinter import *
from PIL import ImageTk, Image, ImageFilter


def open_file():
    global image1
    global imagedata
    global image_path
    file = tkinter.filedialog.askopenfile(filetypes=[("Images", "*.jpg")])
    if file:
        imagedata = Image.open(file.name).resize((300, 500))
        imagedata.save("temp.jpg")
        image_info.config(text=f"Mode: {imagedata.mode}\nSize: {imagedata.size}\nWidth: {imagedata.width}\nHeight: "
                               f"{imagedata.height}")
        image_path = file.name
        image1 = ImageTk.PhotoImage(imagedata)
        image.configure(image=image1, width="300", height="500")
        image.image = image1


def blur():
    global image1
    try:
        img1 = Image.open("temp.jpg").resize((300, 500))
        img2 = img1.filter(ImageFilter.BLUR)
        img2.save("temp.jpg")
        img3 = ImageTk.PhotoImage(img2)
        image1 = img3
        image.config(image=image1)
    except:
        pass


def contour():
    global image1
    try:
        img1 = Image.open("temp.jpg").resize((300, 500))
        img2 = img1.filter(ImageFilter.CONTOUR)
        img2.save("temp.jpg")
        img3 = ImageTk.PhotoImage(img2)
        image1 = img3
        image.config(image=image1)
    except:
        pass


def detail():
    global image1
    try:
        img1 = Image.open("temp.jpg").resize((300, 500))
        img2 = img1.filter(ImageFilter.DETAIL)
        img2.save("temp.jpg")
        img3 = ImageTk.PhotoImage(img2)
        image1 = img3
        image.config(image=image1)
    except:
        pass


def edge_enhance():
    global image1
    try:
        img1 = Image.open("temp.jpg").resize((300, 500))
        img2 = img1.filter(ImageFilter.EDGE_ENHANCE)
        img2.save("temp.jpg")
        img3 = ImageTk.PhotoImage(img2)
        image1 = img3
        image.config(image=image1)
    except:
        pass


def emboss():
    global image1
    try:
        img1 = Image.open("temp.jpg").resize((300, 500))
        img2 = img1.filter(ImageFilter.EMBOSS)
        img2.save("temp.jpg")
        img3 = ImageTk.PhotoImage(img2)
        image1 = img3
        image.config(image=image1)
    except:
        pass


def edge_enhance_more():
    global image1
    try:
        img1 = Image.open("temp.jpg").resize((300, 500))
        img2 = img1.filter(ImageFilter.EDGE_ENHANCE_MORE)
        img2.save("temp.jpg")
        img3 = ImageTk.PhotoImage(img2)
        image1 = img3
        image.config(image=image1)
    except:
        pass


def rotate_img(degrees):
    global image1
    try:
        img1 = Image.open("temp.jpg").resize((300, 500))
        img2 = img1.rotate(degrees)
        img2.save("temp.jpg")
        img3 = ImageTk.PhotoImage(img2)
        image1 = img3
        image.config(image=image1)
    except:
        pass


def exit_cleanup():
    os.remove("temp.jpg")


main_window = Tk()
main_window.title("Image editor")
main_window.geometry("695x600")
frame = Frame(main_window)
frame.grid(row=0, column=0)
image1 = ""
imagedata = ""
image_path = ""
browse = Button(frame, text="Browse", command=open_file)
browse.grid(row=3, column=1)
rotate_clock = Button(frame, text="Rotate Clockwise", command=lambda: rotate_img(-90), width=20)
rotate_clock.grid(row=3, column=0)
rotate_anti_clock = Button(frame, text="Rotate Anti Clockwise", command=lambda: rotate_img(90), width=20)
rotate_anti_clock.grid(row=3, column=2)
image = Label(frame, image=image1, width=43, height=33, relief=RIDGE)
image.grid(row=2, column=0)
image_info = Label(frame, text=f"Mode: \nSize: \nWidth: \nHeight: ", width=43, height=33, relief=RIDGE)
image_info.grid(row=2, column=2)
blur_b = Button(frame, text="Blur", command=blur, width=10)
blur_b.grid(row=0, column=0)
cont_b = Button(frame, text="Contour", command=contour, width=10)
cont_b.grid(row=0, column=1)
detail_b = Button(frame, text="Detail", command=detail, width=10)
detail_b.grid(row=0, column=2)
edge_en_b = Button(frame, text="Edge Enhance", command=edge_enhance, width=10)
edge_en_b.grid(row=1, column=0)
emb_b = Button(frame, text="Emboss", command=emboss, width=10)
emb_b.grid(row=1, column=1)
edge_en_m_b = Button(frame, text="Edge More", command=edge_enhance_more, width=10)
edge_en_m_b.grid(row=1, column=2)

atexit.register(exit_cleanup)

main_window.mainloop()
