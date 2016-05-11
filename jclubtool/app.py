import tkinter as tk
from PIL import Image, ImageTk


class SelectionCoords:

    def __init__(self, canvas):
        self.canvas = canvas
        self.rect_id = None
        self.x0, self.y0, self.x1, self.y1 = (0,) * 4

    def reset(self, x0, y0):
        self.x0, self.y0 = x0, y0
        self.x1 = x0 + 5
        self.y1 = y0 + 5

        self._draw_rect()

    def stretch_to(self, x1, y1):
        self.x1, self.y1 = x1, y1

        self._draw_rect()

    def _draw_rect(self):

        if self.rect_id:
            self.canvas.delete(self.rect_id)

        self.rect_id = self.canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1)





class Application(tk.Frame):

    def __init__(self, images, master=None):

        tk.Frame.__init__(self, master=master)
        self.images = images
        self.__page_idx = 0


        self.pack()
        self._createWidgets()
        self.selection_coords = SelectionCoords(self.canvas)

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
        self.canvas.bind("<Button-1>", self.create_new_rect)
        self.canvas.bind("<B1-Motion>", self.stretch_rect)
        # self.canvas.bind("<ButtonRelease-1>", self._print_coords)
        self.canvas.bind("<Configure>", self.on_resize)


    def on_resize(self, event):
        self.show_img()


    def create_new_rect(self, event):
        self.selection_coords.reset(event.x, event.y)

    def stretch_rect(self, event):
        self.selection_coords.stretch_to(event.width, event.height)

    @property
    def page_idx(self):
        return self.__page_idx

    @page_idx.setter
    def page_idx(self, value):
        self.__page_idx = max(0, min(value, len(self.images)-1))

    @staticmethod
    def rescale(img, height):
        width = int((height / img.size[1]) * img.size[0])
        return img.resize((width, height))

    def show_img(self):
        """Displays a rescaled page to fit the canvas size."""

        img = self.images[self.page_idx]
        img_scaled = self.rescale(img, self.height)

        #tkinter gotcha--must save photoimage as attribute, or it garbage collects it.
        self._photoimg = ImageTk.PhotoImage(image=img_scaled)

        self.canvas.create_image(0, 0, image=self._photoimg, anchor='nw')

    def get_subimage(self, event):
        rect = self.selection_coords
        pim_size = self.curr_img.photoimg.width(), self.curr_img.photoimg.height()
        rect_perc = [rect.x0 / pim_size[0], rect.y0 / pim_size[1], rect.x1 / pim_size[0], rect.y1 / pim_size[1]]

        # Correct for if the rectangle wasn't drawn top-left to bottom-right
        if rect_perc[0] > rect_perc[2]:
            rect_perc[0], rect_perc[2] = rect_perc[2], rect_perc[0]
        if rect_perc[1] > rect_perc[3]:
            rect_perc[1], rect_perc[3] = rect_perc[3], rect_perc[1]



        im_size = self.curr_img.img.size
        im_rect = [int(s * p) for s, p in zip(im_size * 2, rect_perc)]

        subimg = self.curr_img.img.crop(im_rect)
        subimg.save('img.jpg')

    def next_page(self):
        self.show_img(self._img_idx + 1)

    def prev_page(self):
        self.show_img(self._img_idx - 1)

    @property
    def width(self):
        """Canvas width"""
        return self.canvas.winfo_width()

    @property
    def height(self):
        """Canvas height"""
        return self.canvas.winfo_height()


