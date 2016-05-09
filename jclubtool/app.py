from tkinter import *
from PIL import Image, ImageTk

class AppImage:

    def __init__(self, filename, height=None, scale=None):

        self.img = Image.open(filename)
        self.img_scaled, self.photoimg = None, None
        self.rescale(scale=scale, height=height)


    def rescale(self, scale=None, height=None):

        if height:
            scale = height / self.img.size[1]
        if not scale:
            scale = 1.

        size = self.img.size
        self.img_scaled = self.img.resize((int(size[0] * scale), int(size[1] * scale)))
        self.photoimg = ImageTk.PhotoImage(image=self.img_scaled)


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.pack()
        self.createWidgets()

    def createWidgets(self, width=1000, height=1000):

        self.canvas = Canvas(self, width=width, height=height)
        self.canvas.pack()
        self.canvas.update()

        img = AppImage("img-9.jpg", height=height)
        self.show_img(img)


    def show_img(self, app_img):
        self.img = app_img
        self.canvas.create_image(self.width // 2, self.height// 2, image=self.img.photoimg)

    @property
    def width(self):
        return self.canvas.winfo_width()

    @property
    def height(self):
        return self.canvas.winfo_height()


root = Tk()
root.title('jclubtool')
app = Application(master=root)

app.mainloop()