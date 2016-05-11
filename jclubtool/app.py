import tkinter as tk
from PIL import Image, ImageTk


class PageCollection:

    def __init__(self, images):
        self.images = images
        self.__page_idx = 0
        self.display_scale = 1.

    def next_page(self):
        self.page_idx += 1

    def prev_page(self):
        self.page_idx -= 1

    @property
    def page_idx(self):
        return self.__page_idx

    @page_idx.setter
    def page_idx(self, value):
        self.__page_idx = max(0, min(value, len(self.images)-1))

    def get_current_image(self):
        return self.images[self.page_idx]

    def set_scale(self, height):
        self.display_scale = height / self.get_current_image().size[1]

    def get_scaled_img(self):
        """Displays a rescaled page to fit the canvas size."""
        img = self.get_current_image()
        width = int(img.size[0] * self.display_scale)
        height = int(img.size[1] * self.display_scale)

        img_scaled = img.resize((width, height))
        return img_scaled

    def get_subimage(self, x0, y0, x1, y1):

        rect = [x0, y0, x1, y1]
        rect = [int(coord / self.display_scale) for coord in rect]
        subimg = self.get_current_image().crop(rect)
        return subimg





class Application(tk.Frame):

    def __init__(self, images, master=None):

        tk.Frame.__init__(self, master=master)
        self.images = PageCollection(images)
        self.selectbox = 0

        self.pack()
        self._createWidgets()

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
        if self.selectbox:
            self.selectbox_delete()
        self.selectbox = self.canvas.create_rectangle(event.x, event.y,
                                                      event.x + 1, event.y + 1)

    def selectbox_update(self, event):
        boxcoords = self.canvas.coords(self.selectbox)


        # Correct for if the rectangle wasn't drawn top-left to bottom-right
        if event.x < boxcoords[0]:
            boxcoords[0] = event.x
        else:
            boxcoords[2] = event.x

        if event.y < boxcoords[1]:
            boxcoords[1] = event.y
        else:
            boxcoords[3] = event.y

        print(boxcoords)
        self.canvas.coords(self.selectbox, *boxcoords)


    def show_img(self):
        """Displays a rescaled page to fit the canvas size."""

        self.selectbox_delete()

        img = self.images.get_scaled_img()

        #tkinter gotcha--must save photoimage as attribute, or it garbage collects it.
        self._photoimg = ImageTk.PhotoImage(image=img)

        self.canvas.create_image(0, 0, image=self._photoimg, anchor='nw')


    def get_subimage(self, event):
        assert self.selectbox
        rect = self.canvas.coords(self.selectbox)
        img = self.images.get_subimage(*rect)

        img.save('img.jpg')

    def next_page(self):
        self.images.next_page()
        self.show_img()

    def prev_page(self):
        self.images.prev_page()
        self.show_img()


