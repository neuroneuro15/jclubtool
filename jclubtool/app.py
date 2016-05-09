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


class AppImageCollection:

    def __init__(self, filenames, height=None, scale=None):
        self.images = []
        for filename in filenames:
            img = AppImage(filename, height=height, scale=scale)
            self.images.append(img)

    def __getitem__(self, item):
        return self.images[item]

    def rescale(self, scale=None, height=None):
        for img in self.images:
            img.rescale(scale=scale, height=height)

class Application(tk.Frame):

    images = []

    def __init__(self, images, master=None):
        tk.Frame.__init__(self, master)

        assert isinstance(images, AppImageCollection)
        self.images = images

        self.pack()
        self.createWidgets()

    def createWidgets(self, width=700, height=700):

        self.btn_next = tk.Button(self, text='Prev', command=lambda: self.show_img(self._img_idx - 1))
        self.btn_next.pack(side='top')

        self.btn_next = tk.Button(self, text='Next', command=lambda: self.show_img(self._img_idx + 1))
        self.btn_next.pack(side='top')

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack(side='right')
        self.canvas.update()

        self.images.rescale(height=self.height)


        self._img_idx = 0
        self.show_img(self._img_idx)


    def show_img(self, idx):
        try:
            self.curr_img = self.images[idx]
            self._img_idx = idx
        except IndexError:
            pass

        self.canvas.create_image(self.width // 2, self.height// 2, image=self.curr_img.photoimg)

    @property
    def width(self):
        return self.canvas.winfo_width()

    @property
    def height(self):
        return self.canvas.winfo_height()


