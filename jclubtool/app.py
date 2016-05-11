import tkinter as tk
from PIL import Image, ImageTk
from .pages import PageCollection

class SelectionBox:

    def __init__(self, canvas):
        self.canvas = canvas
        self.id = 0

    def delete(self):
        if self.id:
            self.canvas.delete(self.id)
            self.id = 0

    def new(self, x, y):
        self.delete()
        self.id = self.canvas.create_rectangle(x, y, x + 1, y + 1)

    @property
    def coords(self):
        return self.canvas.coords(self.id)

    def update(self, x, y):

        coords = self.canvas.coords(self.id)

        # Correct for if the rectangle wasn't drawn top-left to bottom-right
        index = 0 if x < coords[0] else 2
        coords[index] = x

        index = 1 if x < coords[1] else 3
        coords[index] = y

        self.canvas.coords(self.id, *coords)


class Application(tk.Frame):

    def __init__(self, images, master=None):

        tk.Frame.__init__(self, master=master)
        self.images = PageCollection(images)


        self.pack()
        self._createWidgets()
        self.selectbox = SelectionBox(self.canvas)

        canv_height = self.canvas.winfo_height()
        self.images.set_scale(canv_height)
        self.show_img()

    def _createWidgets(self, width=600, height=700):
        """Setup method.  Creates all buttons, canvases, and defaults before starting app."""


        self.btn_prev = tk.Button(self, text='Prev', command=self.prev_page)
        self.btn_prev.pack(side='top')

        self.btn_next = tk.Button(self, text='Next', command=self.next_page)
        self.btn_next.pack(side='top')

        # Make the main Canvas, where most everything is drawn
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack(side='right')
        self.canvas.update()


        # Set up selection rectangle functionality
        self.canvas.bind("<Button-1>", self.selectbox_create)
        self.canvas.bind("<B1-Motion>", self.selectbox_update)
        self.canvas.bind("<ButtonRelease-1>", self.get_subimage)
        self.canvas.bind("<Configure>", self.on_resize)


    def on_resize(self, event):
        self.images.set_scale(event.height)
        self.show_img()

    def selectbox_delete(self):
        if self.selectbox:
            self.canvas.delete(self.selectbox)
        self.selectbox = 0

    def selectbox_create(self, event):
        self.selectbox.new(event.x, event.y)

    def selectbox_update(self, event):
        self.selectbox.update(event.x, event.y)

    def show_img(self):
        """Displays a rescaled page to fit the canvas size."""

        self.selectbox.delete()
        img = self.images.get_scaled_img()

        #tkinter gotcha--must save photoimage as attribute, or it garbage collects it.
        self._photoimg = ImageTk.PhotoImage(image=img)

        self.canvas.create_image(0, 0, image=self._photoimg, anchor='nw')


    def get_subimage(self, event):
        img = self.images.get_subimage(*self.selectbox.coords)
        img.save('img.jpg')

    def next_page(self):
        self.images.next_page()
        self.show_img()

    def prev_page(self):
        self.images.prev_page()
        self.show_img()


