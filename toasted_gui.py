import PySimpleGUI as sgui
import image_convert as ic
import os.path
from tkinter import *
from PIL import Image, ImageDraw, ImageOps

"""
# TODO
Need to work on making it work for all image file types.
Need to work on putting draw in its own module to simplify code.
Correct mainloop
Fix overwritten custom image
"""

file_list = [
    [
        sgui.Text("Image Folder"),
        sgui.In(size=(25, 1), enable_events=True, key="Folder"),
        sgui.FolderBrowse(),
    ],
    [
        sgui.Listbox(
            values=[], enable_events=True, size=(40, 20), key="File List"
        )
    ],
]

image_viewer = [
    [sgui.Text("Choose an image from list on left:")],
    [sgui.Text(size=(40, 1), key="Path")],
    [sgui.Image(key="Image")],
]

layout = [
    [
        sgui.Button("Draw Your Toast"),
        sgui.Column(file_list),
        sgui.VSeperator(),
        sgui.Column(image_viewer),
        sgui.Button("Toast Selected Image")
    ]
]

window = sgui.Window("Toasted GUI", layout)

file = None
while True:
    event, values = window.read()
    if event == "Exit" or event == sgui.WIN_CLOSED:
        break
    # Choose folder name, make a list of files
    if event == "Folder":
        folder = values["Folder"]
        try:
            # Get list of images
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".jpg"))
        ]
        window["File List"].update(fnames)
    elif event == "File List":  # Image chosen
        try:
            filename = os.path.join(
                values["Folder"], values["File List"][0]
            )
            img_name = filename[32:]
            edit_img = Image.open(img_name)
            edit_imgR = edit_img.resize((500, 500))
            edit_imgR.save(img_name)
            window["Path"].update(filename)
            window["Image"].update(filename=filename)
            file = filename
            edit_img.save(img_name)
        except:
            pass
    elif event == "Toast Selected Image": # Run conversion
        try:
            ic.image_convert(file)
            sgui.popup_ok("Conversion Successful")
        except:
            print("Image failed conversion.")
    elif event == "Draw Your Toast": # Pop up window draw
        tk = Tk()
        tk.title("Draw your custom image")
        cvs = Canvas(tk, width = 500, height = 500)
        cvs.pack()

        img = Image.new('RGB', (500, 500), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        mouse_click = False
        last = None
        pen_size = 3

        def press(event):
            global mouse_click
            mouse_click = True

        def release(event):
            global mouse_click
            mouse_click = False

        cvs.bind_all('<ButtonPress-1>', press)
        cvs.bind_all('<ButtonRelease-1>', release)

        def finish():
            img.save('custom.png')
            tk.destroy()
            # For demo
            ex_img = Image.open('custom.png')
            ex_img_inv = ImageOps.invert(ex_img)
            ex_img_inv.save('custom.png')
            ic.image_convert('custom.png')
            img.save('custom.png')
            # End for demo
            sgui.popup_ok("Conversion Successful... Check Text File", title="Notice")

        def restart():
            global cvs, img, draw
            cvs.delete('all')
            img = Image.new('RGB', (500, 500), (255, 255, 255))
            draw = ImageDraw.Draw(img)

        Button(tk, text='Restart', command = restart).pack()
        Button(tk, text='Toast Custom Image', command = finish).pack()

        def move(event):
            global mouse_click, last, pen_size
            x,y = event.x, event.y
            if mouse_click:
                if last is None:
                    last = (x, y)
                    return
                draw.line(((x, y), last), (0, 0, 0), width = pen_size)
                cvs.create_line(x, y, last[0], last[1], width = pen_size)
                last = (x, y)
            else:
                last = (x, y)

        cvs.bind_all('<Motion>', move)
        tk.mainloop()
        
window.close()
