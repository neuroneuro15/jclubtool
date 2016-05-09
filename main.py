import jclubtool as jclub
import tkinter as tk
import appdirs
import os
from os import path
import shutil
from glob import glob


appname = 'jclubtool'

_cache_dir = appdirs.user_cache_dir(appname=appname)

# Delete everything in cache directory
for name in os.listdir(_cache_dir):
    file_path = path.join(_cache_dir, name)
    if path.isfile(file_path):
        os.unlink(file_path)


# Copy pdf over to the cache directory
pdf_name = path.join('samples', '416.full.pdf')
new_pdf_name = path.join(_cache_dir, path.basename(pdf_name))
shutil.copy(pdf_name, new_pdf_name)

# Convert PDF to a series of jpgs
print('Converting PDF to jpgs...', end='')
jclub.convert_pdf_to_jpg(new_pdf_name, path.join(_cache_dir, 'img'), resolution=50)
img_names = glob(path.join(_cache_dir, '*.jpg')) #filedialog.askopenfilenames()
jclub.sort_jpg_pages(img_names)
print('...Complete.')

# Load up Tkinter
root = tk.Tk()
root.title(appname)

# Create AppImageCollection (warning: Must come after tk.Tk()!!)
images = jclub.AppImageCollection(img_names)

app = jclub.Application(images=images, master=root)

app.mainloop()