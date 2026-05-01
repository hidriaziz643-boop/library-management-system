from tkinter import *
from PIL import Image, ImageTk
import pyocr
import pyocr.builders
import json
import threading

class librarycontroller:
    def __init__(self,model,view):
        self.model=model
        self.view=view
        self.view.button1.config(command=lambda:self.listbooks())
        self.view.button2.config(command=lambda:self.addbook())
        self.view.button3.config(command=lambda:self.deletebook())
        self.view.button4.config(command=lambda:self.sortbooks())
        self.view.button5.config(command=lambda:self.searchbook())
        self.view.button6.config(command=lambda:self.upload_image_thread())
        self.view.button7.config(command=lambda:self.do_updatestatus())
        self.view.button8.config(command=self.do_lent_out)

    def listbooks(self):
        self.view.updatelistbox(self.model.content)

    def addbook(self):
        try :
            t=self.view.entrytitle.get()
            a=self.view.entryauthor.get()
            y=int(self.view.entryyear.get()) 
            if not(self.model.checkbyall(t,a,y)):
                b={}
                b["Title"],b["Author"],b["Year"],b["Status"]=t,a,y,"Available"
                self.model.content.update({t:b})
                self.model.savelib(self.model.content,self.model.filepath)
                color="green"
                msg="Book successfully added!"
            else:
                color="red"
                msg="This book already exists!"
        except ValueError:
            color="red"
            msg="Invalid! Please check the values."
        self.view.showmsg(color,msg)


    def deletebook(self):
        try :
            t=self.view.entrytitle.get()
            a=self.view.entryauthor.get()
            y=int(self.view.entryyear.get())
            if self.model.checkbyall(t,a,y):
                self.model.content=self.model.updatestatus("Deleted",t,a,y)
                self.model.savelib(self.model.content,self.model.filepath)
                color="green"
                msg="Book successfully deleted!"
            else:
                color="red"
                msg="This book doesn't exist here yet!"
        except:
            color="red"
            msg="Invalid! Please check the values."
        self.view.showmsg(color,msg)
    
    def sortbooks(self):
        try :
            match int(self.view.selected_option.get()):
                case 1:
                    self.model.content=dict(sorted(self.model.content.items(), key=lambda x: x[1]["Title"]))
                case 2:
                    self.model.content=dict(sorted(self.model.content.items(), key=lambda x: x[1]["Author"]))
                case 3:
                    self.model.content=dict(sorted(self.model.content.items(), key=lambda x: x[1]["Year"]))
            self.model.savelib(self.model.content,self.model.filepath)
            color="green"
            msg="Library successfully sorted!"
        except ValueError:
            color="red"
            msg="Invalid! Please select an option."
        self.view.showmsg(color,msg)

    def searchbook(self):
        try:
            t=self.view.entrytitle.get()
            a=self.view.entryauthor.get()
            y=int(self.view.entryyear.get())
            if self.model.checkbyall(t,a,y) :
                self.view.updatelistboxonebook(self.model.searchbook(t,a,y))
                color="green"
                msg="Book found!"
            else:
                color="red"
                msg="Book doesn't exist here yet" 
        except:
            color="red"
            msg="Invalid! Please check the values."
        self.view.showmsg(color,msg)
        
    def do_uploadimage(self):
        try:
            self.view.canvas.delete("all")
            self.view.uploadimage(self.view.entrypath.get())
           
        except:
            color="red"
            msg="Invalid! Please make sure that path exists."
            self.view.showmsg(color,msg)
            
    def upload_image_thread(self):
        thread=threading.Thread(target=self.do_uploadimage)
        thread.daemon=True
        thread.start()
        print("processing...")

    def do_updatestatus(self):
        try:
            t=self.view.entrytitle.get()
            a=self.view.entryauthor.get()
            y=int(self.view.entryyear.get())
            s=self.view.entrystatus.get()
            if self.model.checkbyall(t,a,y) :
                if s not in {"Deleted", "Available", "Lent out", "Missing"} :
                    color="red"
                    msg="Invalid! Please check the entered status."
                else:
                    self.model.content=self.model.updatestatus(s,t,a,y)
                    self.model.savelib(self.model.content,self.model.filepath)
                    color="green"
                    msg="Status successfully updated!"
        except:
            color="red"
            msg="Invalid! Please check the values."
        self.view.showmsg(color,msg)
        
    def do_lent_out(self,event=None):
        try:
            self.listbooks()
            t=self.view.selected_title
            if not t:
                raise ValueError(" you have to select a ligne that starts with Book >> ")
            s="Lent out"
            book=self.model.searchbooktitle(t)
            if book :
                a=book["Author"]
                y=book["Year"]
                self.model.content=self.model.updatestatus(s,t,a,y)
                self.model.savelib(self.model.content,self.model.filepath)
                color="green"
                msg="Book successfully lent out!"
            else:
                color="red"
                msg="Book doesn't exist."
        except:
            color="red"
            msg="Invalid! Please check the values."
        self.view.showmsg(color,msg)

#Aziz Hidri: aziz.hidri@stud.th-deg.de
#Mouheb jounaidi:mouheb.jounaidi@stud.th-deg.de
#Takoua Askri:takoua.askri@stud.th-deg.de