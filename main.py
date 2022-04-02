from tkinter import *
from tkinter import messagebox
import datetime
import math
import serial
import time
from VolTracker import *
volSyr=float(volSyr)

#Change syringe diameter (last two numbers)
step_vol = 2 * 1.8 / 4 / 360 * (math.pi) / 4 * 2.3 * 2.3 #quarter steps
print(step_vol)

arduino = serial.Serial(port='com8', baudrate=9600, timeout=0.1)
time.sleep(3)

root = Tk()
#e is the bulk solution concentration
#inputs in Ci and mL and outputs is in uL

#Password

def PassScreen():
    Pframe = Frame(root)
    Pframe.pack()
    PLab=Label(Pframe, text="Please enter the Password")
    PLab.pack()
    PEnt=Entry(Pframe, bd=5)
    PEnt.pack(side=TOP)
    def Password():  # Check if password entered is correct
        PEntered = PEnt.get()
        if PEntered == "MIE491": #CHANGE PASSWORD HERE
            mainScreen()
            Pframe.destroy()
        else:
            messagebox.showinfo(message="Wrong Password! Please Try Again")
            PassScreen()
            Pframe.destroy()
    EBut=Button(Pframe, text="Enter", command=Password)
    EBut.pack(side=BOTTOM)

def Refill (): #How much to fill syringe
    topFrame.destroy()
    RefillFrame=Frame(root)
    RefillFrame.pack()
    LA = Label(RefillFrame, text="How much would you like to refill in uL?")
    LA.pack(side=TOP)
    RefEnt=Entry(RefillFrame, bd=5)
    RefEnt.pack(side=TOP)

    def RefillTop ():
        # global volSyr
        # fillAm=230-volSyr
        # stepR = fillAm / step_vol
        # remainderF = fillAm % step_vol
        # volR = fillAm + volSyr
        # volSyr = volR
        # if remainderF / step_vol >= 0.5:
        #     stepR = stepR + 1
        # A = 'c'  # activate syringe motor- c means opposite direction of d
        # stepR=int(stepR) #make whole number- number of quarter steps in total
        # WholeStep=int(stepR / 4) #number of whole steps
        # HalfStep=int((stepR % 4)/2)
        # QuarterStep=stepR-(WholeStep*4)-(HalfStep*2)
        # # BStep=5 #number of puncture motor steps
        # #send above to Arduino
        # f = open("VolTracker.py", "w")
        # f.write("volSyr= " +str(volR))
        # f.close()
        # messagebox.showinfo("Refilling", "You are refilling a volume of " + str(fillAm) + " uL")
        # RefillFrame.destroy()
        # mainScreen()

        global volSyr
        A = 'y'
        messagebox.showinfo("Dispensing", "You are refilling a volume of " + str(volSyr) + " uL")
        volT = 230

        motor = str(A) # direction, down/up -> punture (p/o), dispenser (d/c), rotary(r/q)
        fullSteps=str(200) # need to add info on dir for Arduino
        halfSteps =str(0) # also need to modify Varun's code to stop for both switches
        quarterSteps =str(0)
        send = motor + fullSteps + ";"+ halfSteps + ";"+ quarterSteps + ";k"
        arduino.write(send.encode())
        time.sleep(1)

        f = open("VolTracker.py", "w")
        f.write("volSyr= " + str(volT))
        f.close()



    def RefillCalc ():
        global volSyr
        RefAmount=float(RefEnt.get())
        print (RefAmount)
        #If too much volume entered
        if (RefAmount + volSyr) > 230:
            LToo=Label(RefillFrame, text="Too much volume entered.")
            LToo.pack()
            Refill()

        #If enough volume entered
        else:
            # Calculate number of steps
            stepN = RefAmount/ step_vol #steps the syringe motor does
            remainder = RefAmount % step_vol
            volT= RefAmount+volSyr
            volSyr= volT
            if remainder / step_vol >= 0.5:
                stepN = stepN + 1
            stepN=int(stepN)
            #SEND BELOW INTO ARDUINO
            A='c' #activate motor for syringe
            WholeStep = int(stepN / 4)  # number of whole steps
            HalfStep = int((stepN % 4) / 2)
            QuarterStep = stepN - (WholeStep * 4) - (HalfStep * 2)
            print(WholeStep)
            print(HalfStep)
            print(QuarterStep)

            motor = str(A) # direction, down/up -> punture (p/o), dispenser (d/c), rotary(r/q)
            fullSteps=str(WholeStep) # need to add info on dir for Arduino
            halfSteps =str(HalfStep) # also need to modify Varun's code to stop for both switches
            quarterSteps =str(QuarterStep)
            send = motor + fullSteps + ";"+ halfSteps + ";"+ quarterSteps + ";k"
            arduino.write(send.encode())
            time.sleep(1)

            #BStep=5 #NEED TO FIGURE OUT HOW MANY STEPS TO PUNCTURE
            #At this point stepN, A, B, Bstep would be sent to Arduino code
            print(stepN)
            f = open("VolTracker.py", "w")
            f.write("volSyr= " +str(volT))
            f.close()
            RefillFrame.destroy()
            mainScreen()

    RefBut= Button(RefillFrame, text="Enter", command=RefillCalc)
    RefBut.pack()
    FillTop = Button(RefillFrame, text="Refill to Top", fg="red", command=RefillTop)
    FillTop.pack()

#How to reset the volume tracker
def Recon():
    topFrame.destroy()
    ReconFrame=Frame(root)
    ReconFrame.pack()
    LB = Label(ReconFrame, text="How much volume does the syringe have in uL?")
    LB.pack(side=TOP)
    RecEnt=Entry(ReconFrame, bd=5)
    RecEnt.pack(side=TOP)
    def ReconGet ():
        global volSyr
        RecAmount=float(RecEnt.get())
        volSyr=RecAmount
        f = open("VolTracker.py", "w")
        f.write("volSyr= " + str(RecAmount))
        f.close()
        volSyr= RecAmount
        ReconFrame.destroy()
        mainScreen()
    RecBut= Button(ReconFrame, text="Enter", command=ReconGet)
    RecBut.pack(side=BOTTOM)

def DispenseManual(): #Manually input volume to dispense
    topFrame.destroy()
    Man=Frame(root)
    Man.pack()
    MA = Label(Man, text="How much would you like to dispense in uL?")
    MA.pack(side=TOP)
    MEnt=Entry(Man, bd=5)
    MEnt.pack(side=TOP)

    def ManCalc():
        global volSyr
        MAmount=float(MEnt.get())
        if MAmount>volSyr: #If there is not enough volume in syringe
            messagebox.showinfo("Need Refill", "There is not enough liquid in syringe. Please refill")
            mainScreen()
            Man.destroy()
        else: #There is enough volume in syringe
            MStep=MAmount/step_vol
            remainder=(MStep % step_vol)
            if remainder / step_vol >= 0.5:
                Mstep = MStep + 1
            MStep=int(MStep)
            WholeStep = int(MStep / 4)  # number of whole steps
            HalfStep = int((MStep % 4) / 2)
            QuarterStep = MStep - (WholeStep * 4) - (HalfStep * 2)
            A='d' #activate motor for syringe

            motor = str(A) # direction, down/up -> punture (p/o), dispenser (d/c), rotary(r/q)
            fullSteps=str(WholeStep) # need to add info on dir for Arduino
            halfSteps =str(HalfStep) # also need to modify Varun's code to stop for both switches
            quarterSteps =str(QuarterStep)
            send = motor + fullSteps + ";"+ halfSteps + ";"+ quarterSteps + ";k"
            arduino.write(send.encode())
            time.sleep(1)

            #BStep=5 #NEED TO FIGURE OUT HOW MANY STEPS TO PUNCTURE
            #At this point stepN, A, B, Bstep would be sent to Arduino code
            f = open("VolTracker.py", "w")
            volT=volSyr-MAmount
            volSyr=volT
            f.write("volSyr= " +str(volT))
            f.close()
            messagebox.showinfo("Dispensing", "You are dispensing a volume of " + str(MAmount) + " uL")
            Man.destroy()
            mainScreen()

    ManBut= Button(Man, text="Enter", command=ManCalc)
    ManBut.pack()

def EmptySyringe():
    global volSyr
    A='x'
    messagebox.showinfo("Dispensing", "You are dispensing a volume of " + str(volSyr) + " uL")
    volT = 0

    motor = str(A) # direction, down/up -> punture (p/o), dispenser (d/c), rotary(r/q)
    fullSteps=str(200) # need to add info on dir for Arduino
    halfSteps =str(0) # also need to modify Varun's code to stop for both switches
    quarterSteps =str(0)
    send = motor + fullSteps + ";"+ halfSteps + ";"+ quarterSteps + ";k"
    arduino.write(send.encode())
    time.sleep(1)

    f = open("VolTracker.py", "w")
    f.write("volSyr= " + str(volT))
    f.close()


def mainScreen(): #Main screen of commands
    global topFrame
    A=0
    B=0
    topFrame = Frame(root)
    topFrame.pack()
    CleanB = Button(topFrame, text="Clean Syringe", fg="red")
    FillB = Button(topFrame, text="Refill Syringe", fg="red", command=Refill)
    DispenseB = Button(topFrame, text="Dispense Liquid", fg="red", command=dosagefun)
    ReconB = Button(topFrame, text="Reconfigure Syringe Volume", fg="red", command=Recon)
    DispM= Button(topFrame, text="Manually Dispense", fg="red",command=DispenseManual)
    Empty=Button(topFrame, text="Empty Syringe", fg="red",command=EmptySyringe)
    CleanB.pack()
    FillB.pack()
    DispenseB.pack()
    ReconB.pack()
    DispM.pack()
    Empty.pack()
    LAmount=Label(topFrame,text="Current Syringe Volume in uL= " + str(volSyr))
    LAmount.pack()
    if volSyr <5:
        LC = Label(topFrame, text="Filling Syringe Recommended")
        LC.pack(side=BOTTOM)


def dosagefun(): #Calculates the number of steps needed to dispense that volume
    topFrame.destroy()
    dosageFrame=Frame(root)
    dosageFrame.pack(side=TOP)
    #Ask for concentration
    L1 = Label(dosageFrame, text="Please input the concentration of bulk solution and the time it was that concentration in Ci/uL")
    L1.pack(side=TOP)
    edosage=Entry(dosageFrame, bd=5) #concentration of bulk solution in
    edosage.pack(side=TOP)
    dateFrame=Frame(root) #New frame to put date values in to go side by side
    dateFrame.pack(side=TOP)
    #Ask for input date and time of when it was that concentration
    # date and time of bulk solution at the specified concentration
    FL2 = Label(dosageFrame, text="What is the date and time of the specified bulk solution concentration??")
    FL2.pack(side=TOP)
    # date and time entries
    FL3 = Label(dosageFrame, text="Year")
    Fdat = Entry(dosageFrame, bd=5)
    FL4 = Label(dosageFrame, text="Month")
    Fmonth = Entry(dosageFrame, bd=5)
    FL5 = Label(dosageFrame, text="day")
    Fday = Entry(dosageFrame, bd=5)
    FL6 = Label(dosageFrame, text="hour")
    Fhour = Entry(dosageFrame, bd=5)
    FL7 = Label(dosageFrame, text="minute")
    Fminute = Entry(dosageFrame, bd=5)
    # Pack date and time entries
    FL3.pack(side=LEFT)
    Fdat.pack(side=LEFT)
    FL4.pack(side=LEFT)
    Fmonth.pack(side=LEFT)
    FL5.pack(side=LEFT)
    Fday.pack(side=LEFT)
    FL6.pack(side=LEFT)
    Fhour.pack(side=LEFT)
    FL7.pack(side=LEFT)
    Fminute.pack(side=LEFT)
    #Ask for prescribed dose
    L8=Label(dateFrame, text="What is the prescribed dosage in mCi?")
    L8.pack(side=TOP)
    dos=Entry(dateFrame, bd=5)
    dos.pack(side=TOP)
    #date and time of consumption
    L2=Label(dateFrame, text="What is the date and time of consumption?")
    L2.pack(side=TOP)
    #date and time entries
    L3=Label(dateFrame, text="Year")
    dat=Entry(dateFrame, bd=5)
    L4=Label(dateFrame, text="Month")
    month=Entry(dateFrame, bd=5)
    L5=Label(dateFrame, text= "day")
    day=Entry(dateFrame, bd=5)
    L6=Label(dateFrame,text="hour")
    hour=Entry(dateFrame, bd=5)
    L7=Label(dateFrame, text="minute")
    minute=Entry(dateFrame, bd=5)
    #Pack date and time entries
    L3.pack(side=LEFT)
    dat.pack(side=LEFT)
    L4.pack(side=LEFT)
    month.pack(side=LEFT)
    L5.pack(side=LEFT)
    day.pack(side=LEFT)
    L6.pack(side=LEFT)
    hour.pack(side=LEFT)
    L7.pack(side=LEFT)
    minute.pack(side=LEFT)

    def calcDose():
        global volSyr
        e=edosage.get() #gets initial concentration
        e=float(e)

        # First Get date, time etc.
        Fdat_val = Fdat.get()
        Fmonth_val = Fmonth.get()
        Fday_val = Fday.get()
        Fhour_val = Fhour.get()
        Fminute_val = Fminute.get()
        Fdat_val = int(Fdat_val)
        Fmonth_val = int(Fmonth_val)
        Fday_val = int(Fday_val)
        Fhour_val = int(Fhour_val)
        Fminute_val = int(Fminute_val)


        # Second Get date, time etc.
        dat_val=dat.get()
        month_val=month.get()
        day_val=day.get()
        hour_val=hour.get()
        minute_val=minute.get()
        dos_val=dos.get()
        e=float(e)
        dos_val=float(dos_val)
        dat_val=int(dat_val)
        month_val=int(month_val)
        day_val=int(day_val)
        hour_val=int(hour_val)
        minute_val=int(minute_val)

        #Calculation:
        #time:
        first=datetime.datetime(Fdat_val,Fmonth_val,Fday_val,Fhour_val,Fminute_val)
        second=datetime.datetime(dat_val,month_val,day_val,hour_val,minute_val)
        t=second-first
        t=t/datetime.timedelta(hours=1)
        vol=dos_val/(e*(math.exp(-1*0.693/8.01*(t/24))))
        print(vol)
        #Calculate number of steps
        stepNum=vol/step_vol
        remainder=vol % step_vol
        volMic=vol #can delete but would have to be consistent, originally thought this converted to uL
        #Update volume remaining in syringe
        volTemp=volSyr-volMic #in uL
        print(volTemp)
        if volTemp<5: #If there is not enough volume in syringe
            messagebox.showinfo("Need Refill", "There is not enough liquid in syringe. Please refill")
            mainScreen()
            dosageFrame.destroy()
            dateFrame.destroy()
            enterFrame.destroy()
        else: #If there is enough volume in syringe
            volSyr=volTemp
            messagebox.showinfo("Dispensing", "You are dispensing a volume of " +str(vol) + " uL")
            f=open("VolTracker.py", "w")
            f.write("volSyr= " + str(volTemp))
            f.close()
        #Round step vol to find the number steps
            if remainder/step_vol >= 0.5:
                stepNum=stepNum+1
            stepNum=int(stepNum)
            WholeStep = int(stepNum / 4)  # number of whole steps
            HalfStep = int((stepNum % 4) / 2)
            QuarterStep = stepNum - (WholeStep * 4) - (HalfStep * 2)
            A = 'd'  # activate syringe motor

            motor = str(A) # direction, down/up -> punture (p/o), dispenser (d/c), rotary(r/q)
            fullSteps=str(WholeStep) # need to add info on dir for Arduino
            halfSteps =str(HalfStep) # also need to modify Varun's code to stop for both switches
            quarterSteps =str(QuarterStep)
            send = motor + fullSteps + ";"+ halfSteps + ";"+ quarterSteps + ";k"
            arduino.write(send.encode())
            time.sleep(1)

            # BStep=5 #number of puncture motor steps
            #send above to Arduino code
            #get rid of windows and go back to main window
            dosageFrame.destroy()
            dateFrame.destroy()
            enterFrame.destroy()
            mainScreen()

    enterFrame=Frame(root)
    enterFrame.pack(side=TOP)
    But=Button(enterFrame,text="Enter", command=calcDose)
    But.pack(side=TOP)

PassScreen()
#mainScreen()
# This is to test
#TEST = Button(topFrame, text="TEST", fg="red", command=lambda: print(e))
#TEST.pack()

root.mainloop()
