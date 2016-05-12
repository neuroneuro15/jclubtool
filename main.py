import jclubtool as jclub
import tkinter as tk


# Delete everything in cache directory
jclub.create_cache()

# Load up Tkinter
root = tk.Tk()
root.title(jclub.appname)
root.resizable(True, True)

app = jclub.Application(master=root)


# Keyboard Shortcuts
root.bind('<Escape>', lambda event: root.quit())
root.bind('<Left>', lambda event: app.prev_page())
root.bind('<Right>', lambda event: app.next_page())

menubar = tk.Menu(root)

filemenu = tk.Menu(app, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open", command=app.load_pdf)


root.config(menu=menubar)



app.mainloop()