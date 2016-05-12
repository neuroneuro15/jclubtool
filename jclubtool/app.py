import tkinter as tk
from PIL import Image, ImageTk
from .pages import PageCollection
from .guitools import SelectionBox
from tkinter import filedialog, messagebox
import os
from os import path

class Application(tk.Frame):

    def __init__(self, images, master=None, save_dir=None):

        tk.Frame.__init__(self, master=master)
        self.images = PageCollection(images)

        self.pack()
        self._createWidgets()
        if save_dir:
            self.img_dirname.set(save_dir)
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

        self.img_dirname_label = tk.Label(self, text='Save Dir:')
        self.img_dirname_label.pack(side='top')

        self.img_dirname = tk.StringVar()
        self.img_dirname.set(os.getcwd())
        self.img_dirname_entry = tk.Entry(self, textvariable=self.img_dirname)
        self.img_dirname_entry.pack(side='top')

        self.img_dirname_btn = tk.Button(self, text='...', command=self.display_path_dialog)
        self.img_dirname_btn.pack(side='top')

        self.img_basename_label = tk.Label(self, text='Image Filename:')
        self.img_basename_label.pack(side='top')

        self.img_filename = tk.StringVar()
        self.img_filename.set("img01.jpg")
        self.img_basename = tk.Entry(self, textvariable=self.img_filename)
        self.img_basename.pack(side='top')

        # Make the main Canvas, where most everything is drawn
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack(side='right')
        self.canvas.update()


        # Set up selection rectangle functionality
        self.canvas.bind("<Button-1>", self.selectbox_create)
        self.canvas.bind("<B1-Motion>", self.selectbox_update)
        self.canvas.bind("<Button-3>", self.get_subimage)
        self.canvas.bind("<Configure>", self.on_resize)

    def display_path_dialog(self):
        dir_name = filedialog.askdirectory(title="Select a Save Directory")
        self.img_dirname.set(dir_name)

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
        save_filename = path.join(self.img_dirname.get(), self.img_basename.get())
        if path.exists(save_filename):
            resp = messagebox.askyesno(parent=self,
                                       title="Overwrite File",
                                       message="This will overwrite file {}.  Are you sure you want to continue?".format(self.img_filename.get()))
            if not resp:
                return
        img.save(save_filename)
        self.increment_save_filename()

    def increment_save_filename(self):
        pass

    def next_page(self):
        self.images.next_page()
        self.show_img()

    def prev_page(self):
        self.images.prev_page()
        self.show_img()


