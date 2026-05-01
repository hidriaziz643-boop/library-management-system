from tkinter import *
from view import librarywindow
from model import library
from controller import librarycontroller

if __name__=="__main__":
    root = Tk()
    root.title("Mouheb_Takwa_Aziz")
    root.geometry("1100x600")
    model=library()
    view=librarywindow(root,model)
    controller=librarycontroller(model,view)

    root.mainloop()