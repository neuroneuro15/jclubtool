from tkinter import *
from PIL import Image, ImageTk
root = Tk()
root.geometry('1000x1000')

width = 1000
height = 1000
canvas = Canvas(root, width=width, height=height)
canvas.pack()


orig_photo = Image.open("img-9.jpg")


scale = orig_photo.size[1] / width
print(scale)
_photo_size = orig_photo.size
shown_photo = orig_photo.resize((int(_photo_size[0] // scale), int(_photo_size[1] // scale)))

photoimg = ImageTk.PhotoImage(image=shown_photo)


imgsprite = canvas.create_image(width // 2, height // 2, image=photoimg)

# photo_label = Label(image=photo)
# photo_label.photo = photo
# photo_label.photoimg = photoimg
# photo_label.pack()

# text = Label(text="Text") # included to show background color
# text.grid()

import ipdb
ipdb.set_trace()

# root.mainloop()