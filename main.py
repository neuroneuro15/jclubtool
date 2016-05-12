import jclubtool as jclub
import tkinter as tk
import appdirs
import os
from os import path
import shutil
from glob import glob
from PIL import Image

# appname = 'jclubtool'


# _cache_dir = appdirs.user_cache_dir(appname=appname)


# Delete everything in cache directory
jclub.create_cache()
jclub.clear_cache()


# Copy pdf over to the cache directory
pdf_name = path.join('samples', '416.full.pdf')
new_pdf_name = path.join(jclub.cache_dir, path.basename(pdf_name))
jclub.copy_file_to_cache(pdf_name)



# Convert PDF to a series of jpgs
print('Converting PDF to jpgs...', end='')
jclub.convert_pdf_to_jpg(new_pdf_name, path.join(jclub.cache_dir, 'img'), resolution=100)
img_names = jclub.get_jpg_filenames_from_cache()
print('...Complete.')

# Load up Tkinter
root = tk.Tk()
root.title(jclub.appname)
root.resizable(True, True)

# Create AppImageCollection (warning: Must come after tk.Tk()!!)
images = [Image.open(name) for name in img_names]
# images = jclub.AppImageCollection(img_names)

app = jclub.Application(images=images, master=root,
                        save_dir=path.dirname(pdf_name))


# Keyboard Shortcuts
root.bind('<Escape>', lambda event: root.quit())
root.bind('<Left>', lambda event: app.prev_page())
root.bind('<Right>', lambda event: app.next_page())


def debug_print(event=None):
    print("Hello World")

menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open", command=app.load_pdf)


root.config(menu=menubar)



app.mainloop()