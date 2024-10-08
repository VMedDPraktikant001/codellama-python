'''
PDF_zu_CSV_Konvertierer
Author: PVH

Takes an input pdf from a user selection and converts it into a CSV with the VMedD GMBH format and outputs this into a given folder titled with the date and patient number
'''


# importing functions and installed programs and defining global variables
import csv
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os
from tkinter import *
from tkinter import ttk
import pandas as pd
import pdfplumber

#defines global variables including the first line, empty lists to contain each CSV column and, the first line of the csv and working directory
firstline = ["Timestamp", "Heartrate", "Breathingrate"]
time_list = []
breathingrate_list = []
heartrate_list = []
workingdir = os.getcwd()
datelist = []

print("Software Version: 1.8")

def csv_reformat(): #Creates a temporary CSV (firstcsv.csv) and then outputs the final CSV named "date" "patientnumber
    #opens the pdf and then creates a csv called first csv (firstcsv.csv) using pdfplumber module, this csv is temporary and still in the same format as the pdf
    lines = []
    for item in pdfdirlist:
        with pdfplumber.open(item) as pdf:
            pages = pdf.pages
            for page in pdf.pages:
                text = page.extract_text()
                # text = text.replace(" ", ", ")
                for line in text.split('\n'):
                    line = line.split()
                    lines.append(line)
                    print(line)
    df = pd.DataFrame(lines)
    df.to_csv('firstcsv.csv')

    # defines location of the temporary csv and sets time_list to global
    global time_list
    csvlocation = workingdir + r"\firstcsv.csv"
    #opens the temporary csv (firstcsv.csv) and creates a variable called reader, this variable contains the entire temporary csv line for line
    f = open(csvlocation, encoding="utf-8")
    reader = csv.reader(f, delimiter=",")
    startzeit_rememberer_happened = False
    #goes through each line in the csv and runs the associated appender or other function
    for line in reader:
            line = line[1:]
            if (linedeterminer(line) == "Startzeit line"):
                startzeit_rememberer(line)
            if linedeterminer(line) == "Time line":
                time_list_appender(line)
            if linedeterminer(line) == "HF line":
                heartrate_list_appender(line)
            if linedeterminer(line) == "AF line":
                breathingrate_list_appender(line)
    f.close()
    #opens and creates a new final csv named using the date and patientnumber
    with open(f"{targetdir}\\Pat_{patientnumbersaved}_{sorted(datelist)[0]}.csv", "w", newline = "", errors="ignore") as csvfile:
    #debugging prints lists and lengths of lists
        print("opened")
        print(time_list)
        print(heartrate_list)
        print(breathingrate_list)
        print(len(time_list))
        print(len(heartrate_list))
        print(len(breathingrate_list))
        # creates a count used to write into the new csv and writes the firstline containing the header then writes the other lines, closes the final csv and removes temporary csv
        count = (len(heartrate_list) - 1)
        for item in firstline:
            csvfile.write(item+"; ")
        csvfile.write("\n")
        finallist = []
        count = 0
        for item in time_list:
            finallist.append(item + "; " + heartrate_list[count] + "; " + breathingrate_list[count])
            count += 1
        finallist = sorted(finallist)
        for item in finallist:
            csvfile.write(item)
            csvfile.write("\n")
    os.remove(workingdir + r"\firstcsv.csv")

    print("DONE")

def dateadder(time_temp): #adds the date to the time_list
    time_temp = date[0:10] + "_" + time_temp +":00"
    time_list_temp.append(time_temp)

def linedeterminer(line): #determines whether the line input contains Heartfrequency, starting time and date, Breathing Frequency, Time, or is otherwise unimporant
    if "Start" in line[0]  or "tart" in line[0]:
        return "Startzeit line"
    if ":" in (line[0] or line[1] or line[2] or line[3]) and "Start" not in line[0]:
        return "Time line"
    if "HF" in str(line[0]):
        return "HF line"
    if "AF" in str(line[0]):
        return "AF line"
    else:
        return "Unimportant line"

def time_list_appender(line): #Appends the global time_list with the times from the input line
    #creates a temporary list into which the contents of the input line is read into and then appends the global time_list with the temporary list created from the line
    global time_list_temp
    time_list_temp = []
    for item in line:
        item = str(item)
        #checks for doubled items (two numbers being in one entry of the list), splits them and adds them by themselves to the temporary list
        if " " in item:
            tempsplitlist = item.split(" ")
            for entry in tempsplitlist:
                time_list_temp.append(entry)
        elif item != "":
            time_list_temp.append(item)
    time_list_temp2 = time_list_temp
    time_list_temp = []
    for item in time_list_temp2:
        dateadder(item)
    #appends global time list with the temporary time list
    for item in time_list_temp:
        time_list.append(item)

def heartrate_list_appender(line): #Appends the global heartrate_list with the times from the input line
    #creates a temporary list into which the contents of the input line is read into and then appends the global heartrate_list with the temporary list created from the line
    line = line[1:] #The first entry in the line is removed as it contains "HF", marking it as a heartfrequency line
    heartrate_list_temp = []
    for item in line:
        item = str(item)
        if " " in item:
            #checks for doubled items (two numbers being in one entry of the list), splits them and adds them by themselves to the temporary list
            tempsplitlist = item.split(" ")
            for entry in tempsplitlist:
                    #checks whether the entry contains a number and appends it if there is (excludes misreads)
                    if num_there(entry) == True:
                        heartrate_list_temp.append(entry)
                    #checks for question marks in entry and appends if it is there. Question marks are included in "-?-" entries which stand for unknown or empty entries and should be added to the final CSV
                    elif questionmark_finder(entry) == True and entry != "HF":
                        heartrate_list_temp.append(entry)
        elif item != "":
            heartrate_list_temp.append(item)
    #appends global heartrate_list with the temporary time list
    for item in heartrate_list_temp:
        heartrate_list.append(item)

def breathingrate_list_appender(line): #Appends the global breathingrate_list with the times from the input line
    #creates a temporary list into which the contents of the input line is read into and then appends the global breathingrate_list with the temporary list created from the line
    line = line[1:] #The first entry in the line is removed as it contains "AF", marking it as a breathingfrequency line
    breathingrate_list_temp = []
    for item in line:
        item = str(item)
        if " " in item:
            #checks for doubled items (two numbers being in one entry of the list), splits them and adds them by themselves to the temporary list
            tempsplitlist = item.split(" ")
            for entry in tempsplitlist:
                #checks whether the entry contains a number and appends it if there is (excludes misreads)
                if num_there(entry) == True:
                    breathingrate_list_temp.append(entry)
                #checks for question marks in entry and appends if it is there. Question marks are included in "-?-" entries which stand for unknown or empty entries and should be added to the final CSV
                elif questionmark_finder(entry) == True and entry  != "AF":
                    breathingrate_list_temp.append(entry)
        elif item != "":
            breathingrate_list_temp.append(item)
    #appends global breathingrate_list with the temporary time list
    for item in breathingrate_list_temp:
        breathingrate_list.append(item)

def firstnumberfinder(string): #Returns the position of the first number in a string
    count = 0
    for letter in string:
        if letter.isdigit():
            return count
        count += 1

def startzeit_rememberer(line): #Saves the date from a "Startzeit" line into the global date variable
    #creates a long string out of all the list entries in a line, finds the first number and uses this number in order to save the date which is of fixed length
    # (the reason for this convulted approach is for redundancy sake in the case that the pdf is misread or items are misread)
    global startzeitstring
    startzeitstring = ""
    for item in line:
        startzeitstring += item
        startzeitstring += " "
    indexofstartdate = firstnumberfinder(startzeitstring)
    global date
    date = startzeitstring[indexofstartdate:(indexofstartdate + 19)].replace(".", "_")
    date = date.replace(":", "_")
    date = date.replace(" ", "_")
    date = date[6:10] + "-" + date[3:5] + "-" + date[0:2] + "-" + date[11: ]
    datelist.append(date)

def num_there(s): #Returns True is there are numbers in a given string
    return any(i.isdigit() for i in s)

def questionmark_finder(phrase): #returns true if there is a questionmark (?) in a given string
    for i in phrase:
        if i == "?" or '?':
            return True

def patient_number_entry(): #creates a GUI that asks the user to enter the Patientnumber, this number is used and saved into the title of the final converted CSV into a global variable (patientnumbersaved)
    #(the reason for the GUI not returning the value and instead saving to a global variable, as with a lot of functions on this program is that it creates problems with the way Tkinter works, resulting
    # in the program being stuck in a loop (this can probably be fixed))

    #creates the top frame and creates patientnumber variable which is later used in the button and output
    frame = Toplevel()
    frame.title("Bitte Patienten Nummer Eingeben")
    mainframe = ttk.Frame(frame, padding="4", width=30, height=30)
    mainframe.pack()
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
    patientnumber = StringVar()
    patientnumberentry = Entry(mainframe, width=24, textvariable=patientnumber)
    patientnumberentry.grid(column=2, row=2, sticky=(N))

    #Label that tells the user what to do
    ttk.Label(mainframe, text="Patienten Nummer Eingeben").grid(column=2, row=1, sticky=(N))

    # Save function which saves the
    def save(*args):
        try:
            value = str(patientnumber.get()) #for some reason an empty value is saved here, basically ""
            global patientnumbersaved
            patientnumbersaved = value
            frame.destroy()
            frame.quit()
        except ValueError:
            pass

    #creates the "OK" button which when clicked starts the save command
    ttk.Button(mainframe, text="OK", command=save).grid(column=2, row=3, sticky=(W, E))

    # pads all of the buttons and labels in the mainframe (subframe of "frame")
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)
    patientnumberentry.focus()

    #binds enter so the save function
    frame.bind("<Return>", save)

    #starts the mainloop of the window
    frame.mainloop()

def pdfFinderGUI(): #Lets the user select the PDF and saves its location into the global variable "pdfdir" and the name into the global variable "pdffilename"
    Tk().withdraw()
    pdfdirectory = askdirectory(title="Bitte wählen sie den Ordner mit den Dateien aus die sie Konvertieren möchten")
    global pdffilelist
    pdffilelist = os.listdir(pdfdirectory)
    global pdfdirlist
    pdfdirlist = []
    for item in pdffilelist:
        if "pdf" in item:
            pdfdirlist.append(os.path.join(pdfdirectory.replace("/", ("\\")), item))

def targetfolderGUI(): #Lets the user select the target folder of the Final Saved CSV and saves it in the global variable "targetdir"
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askdirectory(title= "Bitte wählen sie den Ort wo die Konvertierte Datei Gespeichert werden soll") # show an "Open" dialog box and return the path to the selected file
    global targetdir
    targetdir = filename.replace(os.path.sep, ('\\')) #saves the target directory, replacing the default returned seperator with "\\" to ensure proper interpreting by other modules

def explainerGUI(): #Tells the User what has happened outputting when the PDF has been succesfully converted and telling the user which PDF was converted and where it was saved to
    #cretes the toplevel frame
    topframe = Toplevel()
    topframe.title = ("Datei Erfolgreich Konvertiert")
    #creates the mainframe within the toplevel frame
    mainframe = ttk.Frame(topframe, padding="4", width=100, height=60)
    mainframe.pack()
    topframe.columnconfigure(0, weight=1)
    topframe.rowconfigure(0, weight=1)
    #adds labels which tell the user important info listed above
    ttk.Label(mainframe, text="Datei Erfolgreich Konvertiert").grid(column=2, row=1, sticky=(N))
    ttk.Label(mainframe, text=f"""Die Datei oder Dateien wurden erfolgreich konvertiert und unter "{targetdir}" gespeichert""").grid(column=2,row=2, sticky=(N))
    #defines the ok function which destorys the window and quits the mainloop
    def ok(*args):
        topframe.destroy()
        topframe.quit()

    #makes an "OK" button which is then bound to the "ok" function
    ttk.Button(mainframe, text=f"OK", command=ok).grid(column=2,row=3, sticky=(W,E))

    #binds the enter button to the ok function
    topframe.bind("<Return>", ok)

    # starts the mainloop
    topframe.mainloop()

pdfFinderGUI()
patient_number_entry()
targetfolderGUI()
csv_reformat()
explainerGUI()