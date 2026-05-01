import unittest
import tkinter as tk
from controller import librarycontroller
from model import library
from view import librarywindow
import json
import os
#in the system test we are going to test the entire mvc application
#first step: creat a class name systesting with unittest.TestCase as a parameter
class sysTesting(unittest.TestCase):
    def setUp(self):#def setUp is used to creat a clean and consistent test environment before every test start
        self.root = tk.Tk()
        self.model = library()
        self.model.content = {}
        self.view = librarywindow(self.root, self.model)
        self.controller = librarycontroller(self.model, self.view)
        #we have to creat a json file that we are going to use in the test
        self.testingfile = "testingfile.json"
        with open(self.testingfile,"w") as f:
            json.dump({
                "The Pragmatic Programmer": {
                    "Title": "The Pragmatic Programmer: Your Journey to Mastery",
                    "Author": "Andrew Hunt",
                    "Year": 1999,
                    "Status": "Available"
                },
                "You Don't Know JS": {
                    "Title": "You Don't Know JS: Up & Going",
                    "Author": "Kyle Simpson",
                    "Year": 2015,
                    "Status": "Lent out"
                },
                "Clean Code": {
                    "Title": "Clean Code: A Handbook of Agile Software Craftsmanship",
                    "Author": "Robert C. Martingrz",
                    "Year": 2008,
                    "Status": "Available"   
                            } },f
            )
        self.model.filepath = "testingfile.json"
        #now we are going to test the add book by inserting in the entries
    def test_add_list_update(self):
        self.view.entrytitle.insert(0, "testBook")
        self.view.entryauthor.insert(0, "testAuthor")
        self.view.entryyear.insert(0, "2025")
        self.controller.addbook()
        self.assertIn("testBook", self.model.content) #check if the book is successfully added
    #the next step is to list the books and check if the listbox lb is not empty
        self.controller.listbooks()
        self.assertGreaterEqual(len(self.view.lb.get(0, "end")), 1) #check if at least one line is written in the listbox
    #stimulating updatebook
        #clearing the entry field then filling them again and try to delete the inserted book
        self.view.entrytitle.delete(0, "end")
        self.view.entryauthor.delete(0, "end")
        self.view.entryyear.delete(0, "end")
        self.view.entrytitle.insert(0, "testBook")
        self.view.entryauthor.insert(0, "testAuthor")
        self.view.entryyear.insert(0, "2025")
        self.controller.deletebook()
        #check if the status of testBook="Deleted"
        self.assertEqual(self.model.content["testBook"]["Status"], "Deleted")
    #after all the tests we have to delete the testingfile
    def tearDown(self):
        if os.path.exists(self.testingfile ):
            os.remove(self.testingfile )

if __name__ == "__main__":
    unittest.main()





#Aziz Hidri: aziz.hidri@stud.th-deg.de
#Mouheb jounaidi:mouheb.jounaidi@stud.th-deg.de
#Takoua Askri:takoua.askri@stud.th-deg.de