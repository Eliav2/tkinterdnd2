## TkinterDnD2

[Eliav2/tkinterdnd2](https://github.com/Eliav2/tkinterdnd2) is a fork of the (unmaintained) [pmgagne/tkinterdnd2](https://github.com/pmgagne/tkinterdnd2) which is a python wrapper for [tkdnd](https://github.com/petasis/tkdnd) . 

This repo was originally forked and edited for the purpose of publishing to pypi so one could simply install this package with  `pip install tkinterdnd2`.

This repository is being maintained to ensure availability of `tkinterdnd2` into the future, providing Tkinter native drag and drop support for windows, unix and Mac OSX.


### What is TkDnD2

[tkDnD2](https://github.com/petasis/tkdnd) is a tcl/Tk extension adding native drag and drop support.

### What this repository is about

This repo package TkinterDnD2 and tkdnd2 into a standard python module.

When the extension is imported in python its location will be automatically added to the Tk search path.

This repository contains the compiled binaries from https://github.com/petasis/tkdnd/releases/tag/tkdnd-release-test-v2.9.4. In order to provide support on ARM, we include built binaries from the now defunct [tkinterdnd2-universal](https://pypi.org/project/tkinterdnd2-universal/#files) which added ARM support.


## Install

`python -m pip install tkinterdnd2`

## Usage

```python
import tkinter as tk

from tkinterdnd2 import DND_FILES, TkinterDnD

root = TkinterDnD.Tk()  # notice - use this instead of tk.Tk()

lb = tk.Listbox(root)
lb.insert(1, "drag files to here")

# register the listbox as a drop target
lb.drop_target_register(DND_FILES)
lb.dnd_bind('<<Drop>>', lambda e: lb.insert(tk.END, e.data))

lb.pack()
root.mainloop()
```
![tkinterdnd2 example usage](https://i.stack.imgur.com/jnOWd.png)


see any of the [demos](./demos) for usage examples.

## Framework Integration

If you are using a GUI framework that manages its own Tk root window (such as PySimpleGUI or CustomTkinter), you cannot use `TkinterDnD.Tk()` as the root. Instead, call `TkinterDnD.require()` on the framework's existing root after it has been created. This loads tkdnd into the shared Tcl interpreter, making drag-and-drop available to all widgets in the process.

The following are some simple examples: 

### PySimpleGUI

```python
import PySimpleGUI as sg
from tkinterdnd2 import TkinterDnD, DND_FILES

def on_drop(event):
    window["-FILE-"].update(event.data)

layout = [
    [sg.Text("Drag & Drop a File Here")],
    [sg.Input("", key="-FILE-")],
    [sg.Button("OK"), sg.Button("Cancel")],
]

window = sg.Window("File Drop", layout, finalize=True)

# Inject DnD into PySimpleGUI's own root — no dummy window needed
TkinterDnD.require(window.TKroot)

# Register any widget as a drop target
window["-FILE-"].widget.drop_target_register(DND_FILES)
window["-FILE-"].widget.dnd_bind("<<Drop>>", on_drop)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Cancel"):
        break

window.close()
```

### CustomTkinter

```python
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES

def on_drop(event):
    entry.delete(0, "end")
    entry.insert(0, event.data)

app = ctk.CTk()
app.title("File Drop")

# Inject DnD into CustomTkinter's root
TkinterDnD.require(app)

entry = ctk.CTkEntry(app, width=400, placeholder_text="Drag a file here...")
entry.pack(padx=20, pady=20)

entry.drop_target_register(DND_FILES)
entry.dnd_bind("<<Drop>>", on_drop)

app.mainloop()
```

## pyinstaller

When using `pyinstaller`, you should use the hook-tkinterdnd2.py file included to collect the TkDnD binaries and build them into the project. To use it, copy it into the base directory of your project, then run pyinstaller as follows:

    pyinstaller -F -w myproject/myproject.py --additional-hooks-dir=.
