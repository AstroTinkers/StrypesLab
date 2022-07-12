import tkinter.filedialog
from tkinter import *
import PIL.ImageFilter
from PIL import ImageTk, Image


def open_file():
    global image1
    file = tkinter.filedialog.askopenfile(filetypes=[("Images", "*.jpg")])
    if file:
        print(file.name)
        image1 = Image.open(file.name).resize((300, 500))
        image1 = ImageTk.PhotoImage(image1)
        image.configure(image=image1, width="300", height="500")
        image.image = image1


def blur(img):
    img = Image.open(img).filter(PIL.ImageFilter.BLUR)
    out = img.filter()


def contour(img):
    pass


def detail(img):
    pass


def edge_enhance(img):
    pass


def emboss(img):
    pass








main_window = Tk()
main_window.title("Image editor")
main_window.geometry("800x600")
frame = Frame(main_window)
frame.grid()

image1 = ""
browse = Button(frame, text="Browse", command=open_file)
browse.grid(row=2, column=1)
image = Label(frame, image=image1)
image.grid(row=1, column=0, columnspan=2)
blur_b = Button(frame, text="Blur", command=lambda: blur(image1))
blur_b.grid(row=0, column=0)





main_window.mainloop()
