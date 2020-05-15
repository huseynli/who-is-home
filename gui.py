#! /usr/bin/python3
from tkinter import *
import os

def recreate_right_content():
    global rightcontents
    rightcontents.destroy()
    rightcontents = Frame(rightarea)
    rightcontents.pack(side="left", fill=BOTH, expand=True)

def show(filename): #to show various files
    recreate_right_content()
    try:
        with open (filename, "r") as fhand:
            instructions = fhand.read()
    except:
        instructions = filename+" file has not been yet created. If this is the first time you are using this application, after editing configurations file click \"Perform scan\" button.\n\nIf not, click \"Click empty devices list\" and start from beginning."
    contents = Text(rightcontents, wrap=WORD)
    contents.insert(INSERT, instructions)
    contents.pack(fill=BOTH, expand=True)

def edit(filename): #edit various files
    recreate_right_content()
    try:
        with open (filename, "r") as fhand:
            placeholder = fhand.read()
        noexist = 0
    except:
        noexist = 1
        placeholder = filename+" file has not been yet created. If this is the first time you are using this application, after editing configurations file click \"Perform scan\" button.\n\nIf not, click \"Click empty devices list\" and start from beginning."
    usr_inp = Text(rightcontents, wrap=WORD)
    usr_inp.insert(INSERT, placeholder)
    usr_inp.pack(fill=BOTH, expand=True)
    if noexist ==0:
        savebtn = Button(rightcontents, text = "Save changes", command= lambda: filesaver(filename, usr_inp.get("1.0","end-1c"))).pack(side="bottom", pady=30)

def filesaver(filename, content):#save any changes made to various text files.
    with open (filename, "w") as fhand:
        fhand.write(content)
def scan():
    recreate_right_content()
    waitlabel = Label(rightcontents, text = "This will take some time, please wait until scans are complete...\nIf this is first scan ever, or after deletion of files, this will take some extra time.")
    waitlabel.pack()
    waitlabel.update_idletasks()
    os.system("python3 areyouthere.py")
    #time.sleep(5)
    show("log.txt")

def burntheworld():
    if os.path.isfile("1list.txt") == False or os.path.isfile("2list.txt") == False or os.path.isfile("alldevices.txt") == False or os.path.isfile("spieddevices.txt") == False or os.path.isfile("log.txt") == False or os.path.isfile("lastsent.txt") == False or os.path.isfile("lastread.txt") == False:
        recreate_right_content()
        nofilelabel = Label(rightcontents, text = "All files have allready been deleted. Perform scan to populate them again.")
        nofilelabel.pack()
    else:
        recreate_right_content()
        waitlabel = Label(rightcontents, text = "Deleting files. Please wait.")
        waitlabel.pack()
        waitlabel.update_idletasks()
        os.remove("1list.txt")
        os.remove("2list.txt")
        os.remove("alldevices.txt")
        os.remove("spieddevices.txt")
        os.remove("log.txt")
        os.remove("lastsent.txt")
        os.remove("lastread.txt")
        os.remove("unknowndevices.txt")
        waitlabel.configure(text = "Files have been deleted. To populate them again, click \"Perform scan\"")
        

root = Tk()
root.title("Who is there ?")
root.geometry("800x600")
#a frame to hold all buttons on the left side
leftarea = LabelFrame(root, text="Options")
leftarea.pack(side="left", fill="y", expand=False, padx=5, pady=5, ipadx=5, ipady=5)
#multipurpose frame ont he left side to show/edit text
rightarea = LabelFrame(root, text="Multipurpose panel")
rightarea.pack(side="left", fill=BOTH, expand=True, padx=5, pady=5, ipadx=5, ipady=5)
#a frame inside rightarea that will be destroyed and renewed by recreate_right_content() so that new widgets replace old ones.
rightcontents = Frame(rightarea)
rightcontents.pack(side="left", fill=BOTH, expand=True)

readmebtn = Button(leftarea, text = "Read Me", command = lambda: [show("READ_ME.txt"), rightarea.configure(text="Read Me")], width = 15).pack()
clibtn = Button(leftarea, text = "CLI Instructions", command = lambda: [show("cli_instructions.txt"), rightarea.configure(text="CLI Instructions")], width = 15).pack()
guibtn = Button(leftarea, text = "GUI Instructions", width = 15, command = lambda: [show("gui_instructions.txt"), rightarea.configure(text="GUI Instructions")]).pack()
confbtn = Button(leftarea, text = "Edit configurations", width = 15, command = lambda: [edit("emailconf.py"), rightarea.configure(text="Edit configurations file")]).pack()
scanbtn = Button(leftarea, text = "Perform scan", width = 15, command = lambda: [scan(), rightarea.configure(text="Scanning/Initialization")]).pack()
kdevicesbtn = Button(leftarea, text = "Edit known devices", width = 15, command = lambda: [edit("alldevices.txt"), rightarea.configure(text="Edit list of known devices.(update 3rd column with device name)")]).pack()
sdevicesbtn = Button(leftarea, text = "Edit spied devices", width = 15, command = lambda: [edit("spieddevices.txt"), rightarea.configure(text="Edit list of spied devices.(update 3rd column with device name, add or delete devices)")]).pack()
udevicesbtn = Button(leftarea, text = "Edit unknown devices", width = 15, command = lambda: [edit("unknowndevices.txt"), rightarea.configure(text="Edit list of unknown devices.(Copy to known/spied devices upon identification)")]).pack()
reportbtn = Button(leftarea, text = "Latest report", width = 15, command = lambda: [edit("log.txt"), rightarea.configure(text="Latest scan results")]).pack()
scratchbtn = Button(leftarea, text = "Empty devices list\nStart from scratch", width = 15, command = lambda: [burntheworld(), rightarea.configure(text="Empty devices list")]).pack()



root.mainloop()