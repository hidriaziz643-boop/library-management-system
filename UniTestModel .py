import unittest
from model import library
import json
import os

class unitesting(unittest.TestCase):
    def setUp(self):
        #create library to test on
        self.testfile="testlib.json"
        with open(self.testfile,"w") as file:
            json.dump({
                "La vie en rose":{

                "Title":"La vie en rose",
                "Author":"Titi",
                "Year":2004,
                "Status":"Available"
                },

                "Micky Mouse":
                {
                "Title":"Micky Mouse",
                "Author":"Skodi",
                "Year":2001,
                "Status":"Lent Out"
                }

                },file,indent=4)
            self.lib=library()
            self.lib.filepath=self.testfile

    #Testing the search function
    def testsearch(self):
        #Test if it returns the correct book by title,author and year
        book=self.lib.searchbook("La vie en rose","Titi",2004)
        self.assertIsNotNone(book)
        self.assertEqual(book["Title"],"La vie en rose")
        self.assertEqual(book["Author"],"Titi")
        self.assertEqual(book["Year"],2004)


    def testcheckbyall(self):
        book=self.lib.checkbyall("La vie en rose", "Titi",2004)
        self.assertTrue(book)

     #Testing the updatedstatus function
    def testupdatedstatus(self):
        updated=self.lib.updatestatus("Available","La vie en rose","Titi",2004)
        updatedbook=updated["La vie en rose"]

        self.assertEqual(updatedbook["Status"],"Available")

        with open(self.testfile,"r") as file:
            content=json.load(file)

        self.assertEqual(content["La vie en rose"]["Status"],"Available")

        with open(self.testfile,"w") as file:
            json.dump(content,file,indent=4)
            
    def tearDown(self):
        if os.path.exists(self.testfile):
            os.remove(self.testfile)

   

if __name__=="__main__":
    unittest.main()


        
     
#Aziz Hidri: aziz.hidri@stud.th-deg.de
#Mouheb jounaidi:mouheb.jounaidi@stud.th-deg.de
#Takoua Askri:takoua.askri@stud.th-deg.de