import json
from tkinter import filedialog
import os


class library:
    def __init__(self):
        self.filepath=os.path.join(os.path.dirname(__file__),"books.json") # if you want to run the code you have to put your own path
        self.content=self.readlib(self.filepath)

    #open a file
    def open_file(self):
        filepath=filedialog.askopenfilename(filetypes=[("JSON Files","*.json"),])
        if not filepath:
            return
        self.content=self.readlib(filepath)
        self.filepath=filepath

    #create a new file
    def new_file(self):
        filepath=filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("JSON Files","*.json"),])
        if not filepath:
            return
        with open(filepath,'w') as f:
            self.filepath=filepath
            json.dump({},f,indent=4)
            self.content=self.readlib(filepath)
            print(self.content)

    #load the library
    def readlib(self,filepath):
        with open(filepath,"r") as lib :
            content=lib.read()
            if not content.strip():
                return {}
            else:
                return json.loads(content)
            
    #save changes in the library
    def savelib(self,content,filepath):
        with open(filepath,"w") as lib :
            json.dump(content,lib,indent=4)

    #check if a book exists by all elements
    def checkbyall(self,title,author,year):
        content=self.readlib(self.filepath)
        for key,value in content.items():
            if value["Title"]==title and value["Author"]==author and value["Year"]==year:
                return True
        return False
    
    #check if a book exists by title
    def checkbytitle(self,title):
        content=self.readlib(self.filepath)
        for key,value in content.items():
            if value["Title"]==title:
                return True
        return False
    
    def updatestatus(self,status,t,a,y):
        content=self.readlib(self.filepath)
        for key,value in content.items():
            if value["Title"]==t and value["Author"]==a and value["Year"]==y:
                value["Status"]=status
                break
        return content
    
    def searchbook(self,t,a,y):
        content=self.readlib(self.filepath)
        for key,value in content.items():       
            if value["Title"]==t and value["Author"]==a and value["Year"]==y:
                return value
            
    def searchbooktitle(self,t):
        content=self.readlib(self.filepath)
        for key,value in content.items():       
            if value["Title"]==t:
                return value
            
#Aziz Hidri: aziz.hidri@stud.th-deg.de
#Mouheb jounaidi:mouheb.jounaidi@stud.th-deg.de
#Takoua Askri:takoua.askri@stud.th-deg.de