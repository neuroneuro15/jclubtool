import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog

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


class Application(tk.Frame):

    images = []

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.pack()
        self.createWidgets()

    def createWidgets(self, width=1000, height=1000):

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()
        self.canvas.update()

        img_names = filedialog.askopenfilenames()
        self.load_images(img_names)

        self.show_img(0)

    def load_images(self, filenames):
        for filename in filenames:
            img = AppImage(filename, height=self.height)
            self.images.append(img)



    def show_img(self, idx):
        self.curr_img = self.images[idx]
        self.canvas.create_image(self.width // 2, self.height// 2, image=self.curr_img.photoimg)

    @property
    def width(self):
        return self.canvas.winfo_width()

    @property
    def height(self):
        return self.canvas.winfo_height()


root = tk.Tk()
root.title('jclubtool')
app = Application(master=root)

app.mainloop()