import jclubtool as jclub
import tkinter as tk


root = tk.Tk()
root.title('jclubtool')

from glob import glob
img_names = glob('samples/*.jpg') #filedialog.askopenfilenames()
jclub.sort_jpg_pages(img_names)

images = jclub.AppImageCollection(img_names)

app = jclub.Application(images=images, master=root)

app.mainloop()