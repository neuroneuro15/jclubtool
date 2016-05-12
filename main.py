import jclubtool as jclub
import tkinter as tk
import appdirs
import os
from os import path
import shutil
from glob import glob
from PIL import Image

appname = 'jclubtool'

_cache_dir = appdirs.user_cache_dir(appname=appname)
try:
    os.makedirs(_cache_dir)
except OSError:
    pass

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
jclub.convert_pdf_to_jpg(new_pdf_name, path.join(_cache_dir, 'img'), resolution=100)
img_names = glob(path.join(_cache_dir, '*.jpg')) #filedialog.askopenfilenames()
jclub.sort_jpg_pages(img_names)
print('...Complete.')

# Load up Tkinter
root = tk.Tk()
root.title(appname)
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

app.mainloop()