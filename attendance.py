import tkinter as tk
from tkinter import *
from tkinter import messagebox as mess
from tkinter import ttk
import tkinter.simpledialog as tsd
import os
import cv2
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

#Functions===========================================================

#AskforQUIT
def on_closing():
    if mess.askyesno("Quit", "You are exiting from the system. Do you want to continue?"):
        window.destroy()

#clearbutton
def clear():
    txt.delete(0, 'end')
    txt2.delete(0, 'end')
    res = "1) Take Images  ===> 2) Save Profile"
    message1.configure(text=res)

#Check for correct Path
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

#check for haarcascade file
def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='file missing', message='some file is missing.')
        window.destroy()

#$$$$$$$$$$$$$
def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.05, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, Id, name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)
########################################################################################
#$$$$$$$$$$$$$
def TrainImages():
    check_haarcascadefile()
    assure_path_exists("Pass_Train/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("Pass_Train\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

############################################################################################3
#$$$$$$$$$$$$$
def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empty face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################
#$$$$$$$$$$$$$
def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tb.get_children():
        tb.delete(k)
    msg = ''
    i = 0
    j = 0
    attendances = set()
    attendance = []
    col_names = ['Id','Name', 'Date', 'In Time', 'Out Time']

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')

    file_name = "Attendance\Attendance_" + date + ".csv"
    if not os.path.exists(file_name):
        dataframe = pd.DataFrame(columns=col_names)
        dataframe.to_csv(file_name, index=False)

    data = pd.read_csv("Attendance\Attendance_" + date + ".csv")

    for index, row in data.iterrows():
        attendances = data.values.tolist()
 
    recognizer =cv2.face.LBPHFaceRecognizer_create() 
    exists3 = os.path.isfile("Pass_Train\Trainner.yml")
    if exists3:
        recognizer.read("Pass_Train\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), bb, str(date), str(timeStamp), str(timeStamp)]                
            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (0, 251, 255), 2)
            add = True
            if(attendances!=None):
                for att in attendances:
                    if(attendance!=None and att!=None and len(attendance) > 0 and attendance[0] == att[0]):
                        add = False
                        break
            if(add and attendance!=None and len(attendance) > 0):
                present = False
                for att in attendances:
                    if(att[0] == attendance[0]):
                        present = True
                        break
                if(present == False):
                    attendances.add(tuple(attendance))
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'w') as csvFile1:
            writer = csv.writer(csvFile1)
            for att in attendances:
                writer.writerow(att)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'w') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            for att in attendances:
                writer.writerow(att)
        csvFile1.close()
    # with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
    #     reader1 = csv.reader(csvFile1)
    #     for lines in reader1:
    #         i = i + 1
    #         if (i > 1):
    #             if (i % 2 != 0):
    #                 iidd = str(lines[0]) + '   '
    #                 tb.insert('', 0, text=iidd, values=(str(lines[1]), str(lines[2]), str(lines[3]), str(lines[4])))
    tb.insert("", tk.END, values=attendances)
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()

#Front End===========================================================

window = tk.Tk()
window.title("Face Recognition Based Attendance System")
window.geometry("1280x720")
window.resizable(True,True)
window.configure(background='#355454')

#main window------------------------------------------------
message3 = tk.Label(window, text="Face Recognition Based Attendance System" ,fg="white",bg="#355454" ,width=60 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10,relwidth=1)

#frames-------------------------------------------------
frame1 = tk.Frame(window, bg="white")
frame1.place(relx=0.11, rely=0.15, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="white")
frame2.place(relx=0.51, rely=0.15, relwidth=0.39, relheight=0.80)

#frame_headder
fr_head1 = tk.Label(frame1, text="Register New Student", fg="white",bg="black" ,font=('times', 17, ' bold ') )
fr_head1.place(x=0,y=0,relwidth=1)

fr_head2 = tk.Label(frame2, text="Mark Student's Attendance", fg="white",bg="black" ,font=('times', 17, ' bold ') )
fr_head2.place(x=0,y=0,relwidth=1)

#registration frame
lbl = tk.Label(frame1, text="Enter ID",width=20  ,height=1  ,fg="black"  ,bg="white" ,font=('times', 17, ' bold ') )
lbl.place(x=0, y=55)

txt = tk.Entry(frame1,width=32 ,fg="black",bg="#e1f2f2",highlightcolor="#00aeff",highlightthickness=3,font=('times', 15, ' bold '))
txt.place(x=55, y=88,relwidth=0.75)

lbl2 = tk.Label(frame1, text="Enter Name",width=20  ,fg="black"  ,bg="white" ,font=('times', 17, ' bold '))
lbl2.place(x=0, y=140)

txt2 = tk.Entry(frame1,width=32 ,fg="black",bg="#e1f2f2",highlightcolor="#00aeff",highlightthickness=3,font=('times', 15, ' bold ')  )
txt2.place(x=55, y=173,relwidth=0.75)

message0=tk.Label(frame1,text="Follow the steps...",bg="white" ,fg="black"  ,width=39 ,height=1,font=('times', 16, ' bold '))
message0.place(x=7,y=275)

message1 = tk.Label(frame1, text="1) Take Images ===> 2) Save Profile" ,bg="white" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
message1.place(x=7, y=300)

message = tk.Label(frame1, text="" ,bg="white" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=7, y=500)
#Attendance frame
lbl3 = tk.Label(frame2, text="Attendance Table",width=20  ,fg="black"  ,bg="white"  ,height=1 ,font=('times', 17, ' bold '))
lbl3.place(x=100, y=115)

#Display total registration----------
res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations : '+str(res))

#BUTTONS----------------------------------------------

clearButton = tk.Button(frame1, text="Clear", command=clear, fg="white", bg="#13059c", width=11, activebackground = "white", font=('times', 12, ' bold '))
clearButton.place(x=55, y=230,relwidth=0.29)

takeImg = tk.Button(frame1, text="Take Images", command=TakeImages, fg="black", bg="#00aeff", width=34, height=1, activebackground = "white", font=('times', 16, ' bold '))
takeImg.place(x=30, y=350,relwidth=0.89)

trainImg = tk.Button(frame1, text="Save Profile", command=TrainImages, fg="black", bg="#00aeff", width=34, height=1, activebackground = "white", font=('times', 16, ' bold '))
trainImg.place(x=30, y=430,relwidth=0.89)

trackImg = tk.Button(frame2, text="Take Attendance", command=TrackImages, fg="black", bg="#00aeff", height=1, activebackground = "white" ,font=('times', 16, ' bold '))
trackImg.place(x=30,y=60,relwidth=0.89)

quitWindow = tk.Button(frame2, text="Quit", command=window.destroy, fg="white", bg="#13059c", width=35, height=1, activebackground = "white", font=('times', 16, ' bold '))
quitWindow.place(x=30, y=450,relwidth=0.89)

#Attandance table----------------------------
style = ttk.Style()
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
style.configure("mystyle.Treeview.Heading",font=('times', 13,'bold')) # Modify the font of the headings
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
tb= ttk.Treeview(frame2,height =13,columns = ('name','date','intime','outtime'),style="mystyle.Treeview")
tb.column('#0',width=70)
tb.column('name',width=100)
tb.column('date',width=100)
tb.column('intime',width=100)
tb.column('outtime',width=100)
tb.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tb.heading('#0',text ='ID')
tb.heading('name',text ='NAME')
tb.heading('date',text ='DATE')
tb.heading('intime',text ='IN TIME')
tb.heading('outtime',text ='OUT TIME')

attendances = set()

col_names = ['Id', 'Name', 'Date', 'In Time', 'Out Time']

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')

file_name = "Attendance\Attendance_" + date + ".csv"
if not os.path.exists(file_name):
    dataframe = pd.DataFrame(columns=col_names)
    dataframe.to_csv(file_name, index=False)

data = pd.read_csv("Attendance\Attendance_" + date + ".csv")

for index, row in data.iterrows():
    attendances = data.values.tolist()

tb.insert("", tk.END, values=attendances)
# i = 0
# date = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y')
# with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
#         reader1 = csv.reader(csvFile1)
#         for lines in reader1:
#             i = i + 1
#             if (i > 1):
#                 if (i % 2 != 0):
#                     iidd = str(lines[0]) + '   '
#                     tb.insert('', 0, text=iidd, values=(str(lines[1]), str(lines[2]), str(lines[3]), str(lines[4])))
# csvFile1.close()

#SCROLLBAR--------------------------------------------------

scroll=ttk.Scrollbar(frame2,orient='vertical',command=tb.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tb.configure(yscrollcommand=scroll.set)

#closing lines------------------------------------------------
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()