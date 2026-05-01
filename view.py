from tkinter import *
from PIL import Image, ImageTk
import pyocr
import threading

class librarywindow:
    def __init__(self, root ,model):
        #the main window
        self.model=model
        self.root = root
        self.label_1=Label(self.root,text="LIBRARY",relief="ridge", bd=3,fg="red",font=("Arial",30))
        self.label_1.grid(row=0,column=2,columnspan=3)
        #Buttons
        self.labelerror=Label(self.root)
        self.button1=Button(self.root, text="List all books")
        self.button1.grid(row=1,column=0,padx=10,pady=10)
        self.button2=Button(self.root, text="Add a book")
        self.button2.grid(row=1,column=1,padx=10,pady=10)
        self.button3=Button(self.root, text="Delete a book")
        self.button3.grid(row=1,column=2,padx=10,pady=10)
        self.button4=Button(self.root, text="Sort books")
        self.button4.grid(row=1,column=3,padx=10,pady=10)
        self.button5=Button(self.root, text="Search a book")
        self.button5.grid(row=1,column=4,padx=10,pady=10)
        self.button6=Button(self.root, text="Upload Image")
        self.button6.grid(row=1,column=5,padx=10,pady=10)
        self.button7=Button(self.root, text="Update Status")
        self.button7.grid(row=1,column=6,padx=10,pady=10)
        self.button8=Button(self.root, text="Lent out")
        self.button8.grid(row=1,column=7,padx=10,pady=10)
        #Menu
        self.menu=Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu=Menu(self.menu)
        self.menu.add_cascade(label="file",menu=self.filemenu)
        self.filemenu.add_command(label="new",command=self.model.new_file)
        self.filemenu.add_command(label="open...",command=self.model.open_file)
        self.filemenu.add_command(label="Generate 1M books",command=self.generate)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="exit",command=self.root.quit)
        self.helpmenu=Menu(self.menu)
        self.menu.add_cascade(label="help",menu=self.helpmenu)
        self.helpmenu.add_command(label="about")
        #Entries and their labels
        self.fr1=Frame(self.root)
        self.fr1.grid(row=2,column=0,columnspan=2)
        self.fr2=Frame(self.root)
        self.fr2.grid(row=2,column=2,columnspan=2)
        self.fr3=Frame(self.root)
        self.fr3.grid(row=2,column=4,columnspan=2)
        self.fr4=Frame(self.root)
        self.fr4.grid(row=2,column=6,columnspan=2)
        self.fr7=Frame(self.root)
        self.fr7.grid(row=2,column=8)
        self.fr5=Frame(self.root)
        self.fr5.grid(row=5,column=0,columnspan=4)
        self.fr6=Frame(self.root)
        self.fr6.grid(row=5,column=5,columnspan=4)
        title=Label(self.fr1,text="Title: ")
        title.pack(side=LEFT,padx=5)
        author=Label(self.fr2,text="Author:")
        author.pack(side=LEFT,padx=5)
        year=Label(self.fr3,text="Year:")
        year.pack(side=LEFT,padx=5)
        path=Label(self.fr4,text="Image Path: ")
        path.pack(side=LEFT,padx=5)
        status=Label(self.fr7,text="Status: ")
        status.pack(side=LEFT,padx=5)
        self.entrytitle=Entry(self.fr1)
        self.entrytitle.pack()
        self.entryauthor=Entry(self.fr2)
        self.entryauthor.pack()
        self.entryyear=Entry(self.fr3)
        self.entryyear.pack()
        self.entrypath=Entry(self.fr4)
        self.entrypath.pack()
        self.entrystatus=Entry(self.fr7)
        self.entrystatus.pack()
        #image canva
        self.canvas = Canvas(self.fr6, width=420, height=340)
        self.label = Label(self.fr6, font=("Helvetica", 8))
        self.text_label = Label(self.fr6, font=("Helvetica", 8))
        self.rect_id= None
        #Scrollbar and Listbox
        self.scrollbar=Scrollbar(self.fr5)
        self.scrollbar.pack(side=RIGHT,fill="y")
        self.lb=Listbox(self.fr5,yscrollcommand=self.scrollbar.set,bg="lightblue",font=("Arial",10),width=60,height=20)
        self.lb.pack(side=LEFT,expand=True)
        self.scrollbar.config(command=self.lb.yview)
        #Options for sort and search
        self.selected_option = StringVar()
        self.selected_option.set(None)
        self.rb1 = Radiobutton(self.root, text="By titles", variable=self.selected_option, value="1")
        self.rb1.grid(row=4,column=0,columnspan=2)
        self.rb2 = Radiobutton(self.root, text="By authors", variable=self.selected_option, value="2")
        self.rb2.grid(row=4,column=2,columnspan=2)
        self.rb3 = Radiobutton(self.root, text="By year", variable=self.selected_option, value="3")
        self.rb3.grid(row=4,column=4,columnspan=2)
        #selected book
        self.selected_title=""
        self.lb.bind("<<ListboxSelect>>", self.on_select)
    #generating 1 million books
    def generate(self):
        global stop_flag
        stop_flag=False
    #showing messages 
    def showmsg(self,color,message):
        self.labelerror.config(fg=color,text=message)
        self.labelerror.grid(row=3,column=2,columnspan=3)
    #updating the Listbox
    def updatelistbox(self,content):
        self.lb.delete(0,END)
        for key,value in content.items():
            self.lb.insert(END,f"Book >> {key}")
            for key0,value0 in value.items() :
                self.lb.insert(END,f"{key0}:{value0}.")
            self.lb.insert(END,'\n')

    def updatelistboxonebook(self,book):
        self.lb.delete(0,END)
        for key,value in book.items():
            self.lb.insert(END,f"{key}:{value}.")

    
    def recognize_text_in_rectangle(self, x1, y1, x2, y2):
        # Koordinaten normalisieren
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        # Auf Bildgröße begrenzen
        img_w, img_h = self.image.size
        x1 = max(0, min(x1, img_w))
        x2 = max(0, min(x2, img_w))
        y1 = max(0, min(y1, img_h))
        y2 = max(0, min(y2, img_h))

        # Leere Selektion abfangen
        if x1 == x2 or y1 == y2:
            return

        cropped_image = self.image.crop((x1, y1, x2, y2))
        recognized_text = self.tool.image_to_string(cropped_image, lang='eng', builder=pyocr.builders.TextBuilder())
        self.text_label.config(text=f"Recognized Text: {recognized_text.strip()}")

        if self.model.checkbytitle(recognized_text.strip()):
            color="green"
            msg="Book found!"
            self.updatelistboxonebook(self.model.searchbooktitle(recognized_text.strip()))
        else:
            color="red"
            msg="Book doesn't exist here yet! You can resume adding it."
            self.entrytitle.delete(0, END)
            self.entrytitle.insert(0, recognized_text.strip())
        self.showmsg(color, msg)
    
    def on_button_press(self, event):
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)
        self.rect_id = self.rect

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
        width = abs(event.x - self.start_x)
        height = abs(event.y - self.start_y)
        self.label.config(text=f"Dimensions: {width} x {height}")

    def on_button_release(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
        width = abs(event.x - self.start_x)
        height = abs(event.y - self.start_y)
        self.label.config(text=f"Dimensions: {width} x {height}")
        self.recognize_text_in_rectangle(self.start_x, self.start_y, event.x, event.y)

    def uploadimage(self,image_path):
        try:
            self.image_path = image_path
            #self.canvas.delete("all")
        # Load the image
            self.image = Image.open(image_path)
            self.image = self.image.resize((400, 400))
            self.image_tk = ImageTk.PhotoImage(self.image)
        # Display the image on the canvas
            self.canvas.delete("all")
            
            self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)
            self.image_tk_ref = self.image_tk
        # Variables to track mouse position and rectangle drawing
            self.start_x = None
            self.start_y = None
            self.rect = None
            self.rect_id = None
            self.label.config(text="Dimensions: Width x Height")
            self.label.pack(side=TOP,pady=10)
            self.text_label.config( text="Recognized Text: ")
            self.text_label.pack(side=BOTTOM,pady=10,padx=5)
            # Set up OCR tool (pyocr)
            tools = pyocr.get_available_tools()
            if len(tools) == 0:
                raise Exception("No OCR tool found")
            self.tool = tools[0]  # Using the first available OCR tool (usually Tesseract)
            self.canvas.pack(side=RIGHT)
            self.canvas.bind("<ButtonPress-1>", self.on_button_press)
            self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        except:
            self.showmsg("red","Invalid! Please make sure that the path exists.")

    def on_select(self, event): 
        s = self.lb.curselection()
        if s:
            index = s[0]
            selected_book = self.lb.get(index)
            print(f"Selected book: {selected_book}")  
            if selected_book.startswith("Book >> "):
                title = selected_book.split(">> ")[1].strip()
                self.selected_title = title
                print(f"Selected title: {self.selected_title}")
            else:
                self.selected_title = ""
                print(title)
                
#Aziz Hidri: aziz.hidri@stud.th-deg.de
#Mouheb jounaidi:mouheb.jounaidi@stud.th-deg.de
#Takoua Askri:takoua.askri@stud.th-deg.de