import imghdr
import tkinter as tk
import sqlite3

from tkinter import * 
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox, ttk
from tkinter.messagebox import * 

root = Tk()
root.title("DigiGrip: Digital Hand Dynamometer")
root.geometry("700x500")  
root.config(bg="skyblue")

#new window for new patient
class NewWindow(Toplevel):
    def __init__(self, root = None):
        super().__init__(root)
        self.geometry("500x300")

        menuLabel = Label(self, text = "Enter Patient Information Below")
        menuLabel.place(relx = 0.5, rely = 0.1, anchor = "center")

        uploadFileButton = tk.Button(self, text = "Enter", command = UploadFile)
        uploadFileButton.place(relx = 0.5, rely = 0.9, anchor = "center")

        self.PatientLastName()
        self.PatientFirstName()
        self.PatientDateOfBirth()
        self.PatientAge()
        self.PatientSex()
        self.DaysSinceStroke()
    
    def PatientLastName(self, root = None):
        self.patientLastNameLabel = Label(self, text = "Patient's Last Name")
        self.patientLastNameLabel.place(relx = 0.40, rely = 0.25, anchor = "center")
        self.patientLastNameEntry = Entry(self, bd = 5)
        self.patientLastNameEntry.place(relx = 0.65, rely = 0.25, anchor = "center")

    def PatientFirstName(self, root = None):
        patientFirstNameLabel = Label(self, text = "Patient's First Name")
        patientFirstNameLabel.place(relx = 0.4, rely = 0.35, anchor = "center")
        self.patientFirstNameEntry = Entry(self, bd = 5)
        self.patientFirstNameEntry.place(relx = 0.65, rely = 0.35, anchor = "center")

    def PatientDateOfBirth(self, root = None):
        patientDOBLabel = Label(self, text = "Patient's Date of Birth (MM/DD/YYYY)")
        patientDOBLabel.place(relx = 0.30, rely = 0.45, anchor = "center")
        self.patientDOBEntry = Entry(self, bd = 5)
        self.patientDOBEntry.place(relx = 0.65, rely = 0.45, anchor = "center")

    def PatientAge(self, root = None):
        self.patientAgeLabel = Label(self, text = "Age")
        self.patientAgeLabel.place(relx = 0.48, rely = 0.55, anchor = "center")
        self.patientAgeEntry = Entry(self, bd = 5)
        self.patientAgeEntry.place(relx = 0.65, rely = 0.55, anchor = "center")

    def PatientSex(self, root = None):
        self.patientSexLabel = Label(self, text = "Sex")     
        self.patientSexLabel.place(relx = 0.48, rely = 0.65, anchor = "center")
        self.patientSexEntry = tk.StringVar()

        self.sexOptions = ttk.Combobox(self, width = 18, textvariable = self.patientSexEntry) 
        self.sexOptions['values'] = ('Male', 'Female', 'Other')
        self.sexOptions.place(relx = 0.65, rely = 0.65, anchor = "center")
        self.sexOptions.current()
    
    def DaysSinceStroke(self, root = None):
        self.DaysSinceStrokeLabel = Label(self, text = "Days Since Stroke")
        self.DaysSinceStrokeLabel.place(relx = 0.41, rely = 0.75, anchor = "center")
        self.DaysSinceStrokeEntry = Entry(self, bd = 5)
        self.DaysSinceStrokeEntry.place(relx = 0.65, rely = 0.75, anchor = "center")

        label.pack()

    def AddPatientInformation(self):
        patientValue = (self.patientLastNameEntry.get(), 
                        self.patientFirstNameEntry.get(), 
                        self.patientDOBEntry.get(),
                        self.patientAgeEntry.get(),
                        self.patientSexEntry.get(), 
                        self.DaysSinceStrokeEntry.get())
        conn = sqlite3.connect("Patient Log.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO patients (last_name, first_name, dob, age, sex, days_since_stroke) VALUES (?, ?, ?, ?, ?, ?)", patientValue)
        conn.commit()
        conn.close()

#new window for existing patient
class PatientWindow(Toplevel):
    def __init__(self, root = None):
        super().__init__(root)
        self.title("Patient Log")
        self.geometry("700x500")
        label = Label(self, text = "Select Patient")
        label.pack() 

        #column headers
        self.tree= ttk.Treeview(self, column=("column1", "column2", "column3", "column4", "column5"), show='headings')
        self.tree.heading("#1", text="LAST NAME",)
        self.tree.heading("#2", text="FIRST NAME")
        self.tree.heading("#3", text="DOB")
        self.tree.heading("#4", text="SEX")
        self.tree.heading("#5", text="DAYS SINCE STROKE")
        
        #column width
        self.tree.column("#1", width = 150)
        self.tree.column("#2", width = 150)
        self.tree.column("#3", width = 150)
        self.tree.column("#4", width = 70)
        self.tree.column("#5", width = 150)
        self.tree.pack()

        viewDataButton = tk.Button(self, text="view data", command=self.View)
        viewDataButton.pack()

    def View(self):
        conn = sqlite3.connect("Patient Log.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM profile")
        rows = cur.fetchall()
        for row in rows:
            print(row) 
            self.tree.insert("", tk.END, values=row)
        conn.close()    

#connect function to database
def connect():
    conn = sqlite3.connect("Patient Log.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS patients(id INTEGER PRIMARY KEY, last_name TEXT, first_name TEXT, dob TEXT, age INT, sex TEXT, days_since_stroke INT)")
    conn.commit()
    conn.close()

connect()  

#exit button function         
def Close():
    root.destroy()

#upload file function
def UploadFile(event = None):
    fileName = filedialog.askopenfilename()
    print("Selected:", fileName)

#starting menu buttons
newPatient = Button(root, text = "New Patient")
existingPatient = Button(root, text = 'Patient Files')
exit = Button(root, text = "Exit", command = Close)

#binding button function to left click
newPatient.bind("<Button>", lambda e:NewWindow(root))
existingPatient.bind("<Button>", lambda e:PatientWindow(root))

#button spacing 
newPatient.place(relx = 0.5, rely = 0.55, anchor = "center")
existingPatient.place(relx = 0.5, rely = 0.65, anchor = "center")
exit.place(relx = 0.5, rely = 0.75, anchor = "center")

#menu text
menuText = Label(root, 
    text = "DigiGrip: Patient Log", 
    font = ("Lucida", 40),
    bd = 1, bg = "skyblue",
    justify = "center")

#menu text positioning 
menuText.place(relx = 0.5, rely = 0.35, anchor = "center")

#adding the logo 
from PIL import ImageTk, Image
img = Image.open("C:\\Users\\00000\\Desktop\\BIM110\\ucde_logo.png") #need to change computer from computer 
imgResize = img.resize((400, 70), Image.LANCZOS)

pic = ImageTk.PhotoImage(imgResize)
label = Label(image = pic)
label.place(relx = 0.5, rely = 0.075, anchor = "center") 

#click me check
# def toggled():
#     print("The check button works.")

# # Example of how to arrange Checkbutton widget using pack
# var = IntVar()  # Variable to check if checkbox is clicked, or not
# check = Checkbutton(root, text="Click me", bg="skyblue", command=toggled, variable=var)
# check.pack(side="bottom")
root.mainloop()