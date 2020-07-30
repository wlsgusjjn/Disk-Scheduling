'''
Seek Speed = 199 tracks/ 90 ms
RPM = 7200 RPM

'''

from tkinter import*
import random
import copy
import turtle

A = [] # set of header's present track and sector
adp = 0 # amount of all data's positions
B = {}  # dictionary of each data's track position 
C = {}  # dictionary of each data's start sector position
D = {}  # dictionary of each data's end sector position
E = {}  # dictionary of track's amounts of sectors
F = {}  # transmission time of each data

def setting():
    A.clear()
    B.clear()
    C.clear()
    D.clear()
    E.clear()
    sp1.delete(0,END)
    dq1.delete(0,END)
    set()
    i = len(B)-1
    sp1.insert(0,A[0])
    
    while i >= 0:
        if(i != len(B) - 1):
            dq1.insert(0,", ")
        dq1.insert(0,B[i])
        i -= 1

def run():
    z = sp1.get()
    A[0] = int(z)
    order_clear()
    total_time["text"] = "Total time : "
    result1["text"] = " "
    result2["text"] = " "
    x = va.get()
    if x == "SSTF":
        SSTF()
    elif x == "SCAN":
        SCAN()
    elif x == "C-LOOK":
        C_LOOK()


def Turtle_set(x):
    t.reset()
    t.color("white")
    t.speed(10)
    t.sety(160)
    t.setx(-275)
    t.forward(x * 2.7)
    t.clear()
    t.color("black")
    t.speed("normal")

def set():
    hpt = random.randint(0,199)
    hps = random.randint(0,359)
    A.append(hpt)
    A.append(hps)

    adp = random.randint(15,20)
    A.append(adp)
    transmission_time = 0
    dt = 0 # track of each data
    ds = 0 # sector of each data
    i = 0
    while i < adp:
        enable = 1
        while True:
            dt = random.randint(0,199)
            if dt not in E:
                E[dt] = 360
                break
            elif E[dt] != 0:
                break
        while True:
            ds = random.randint(0,359)
            dl = random.randint(1,E[dt])
            if ds + dl >= 360:
                de = ds + dl - 360
            else:
                de = ds + dl
                
            for j in range(i):
                if B[j] == dt:
                    if ((D[j] <= ds) and (C[j] <= de) and (D[j] <= de)) or ((C[j] > ds) and (C[j] >= de)) or ((D[j] <= ds) and ((D[j] < de) or (C[j] >= de))) or ((C[j] > ds) and (C[j] >= de) and (D[j] <= ds) and (D[j] < de)) :
                        enable = 1
                    else:
                        enable = 0
                        break
            if enable == 1:
                break   

        B[i] = dt
        C[i] = ds
        D[i] = de
        E[dt] -= dl
        transmission_time += dl
        F[i] = dl
        i += 1
    A.append(transmission_time)

def SSTF():
    Turtle_set(A[0])
    t.write(A[0])
    Z = copy.deepcopy(B)
    ZZ=[]
    y = len(Z)
    present_track = A[0]
    present_sector = A[1]
    seek_time = 0
    rotational_latency_time = 0
    total_response_time = 0
    transmission_time = 0
    variance = 0
    pre = 0
    k = 0
    while k < y:
        next_distance = 199
        next_rotational_distance = 360
        for j in Z:
            if present_track < Z[j]:
                distance = Z[j] - present_track
            else:
                distance = present_track - Z[j]

            if next_distance > distance:
                wb_sector = present_sector + (distance*90/199) * (360/8.3)
                if wb_sector > 359:
                    wb_sector %= 360
                if wb_sector <= C[j]:
                    radian = C[j] - wb_sector
                else:
                    radian = 360 - (wb_sector - C[j])
                if next_rotational_distance > radian:
                    next_sector = D[j]
                    next_rotational_latency_time = radian
                    next_track = Z[j]
                    next_distance = distance
                    next_position = j

        if present_track <= next_track:
            if pre == 0:
                t.right(15)
            elif pre == -1:
                t.left(150)
            pre = 1
            t.forward(next_distance*2.8)
            t.write(next_track)
        elif present_track > next_track:
            if pre == 0:
                t.right(165)
            elif pre == 1:
                t.right(150)
            pre = -1
            t.forward(next_distance*2.8)
            t.write(next_track)

        seek_time += (next_distance*90/199)
        rotational_latency_time += ((next_rotational_latency_time/360)*8.3)
        response_time = seek_time + rotational_latency_time
        ZZ.append(response_time)
        total_response_time += seek_time + rotational_latency_time
        present_track = next_track
        present_sector = next_sector
        Z[next_position] = 400

        Label(w,width=7,height=1,text=k).grid(row=3+k,column=5)
        Label(w,width=7,height=1,text=present_track).grid(row=3+k,column=6)
            
        k += 1
        
    for a in range(len(ZZ)):
        deviation = (total_response_time/y) - ZZ[a]
        variance += deviation**2



    total_time["text"] = "Total time : " + str(int(seek_time + rotational_latency_time)) + "ms"
    result1["text"] = "Average Seek Time : " + str(int((seek_time/y)*100)/100) + "ms         Average Rotaional Latency Time : " + str(int((rotational_latency_time/y)*100)/100) + "ms"
    result2["text"] = "Transmission Time : " + str(int(((A[3]/360)*8.3)*100)/100) + "ms   Variance of Response Times  : " + str(int((variance/y)*100)/100) + " (ms)^2     Throughput : " + str(int((A[2]/(seek_time + rotational_latency_time))*100)/100) + " request/ms"


def SCAN():
    Turtle_set(A[0])
    t.write(A[0])
    Z = copy.deepcopy(B)
    ZZ=[]
    y = len(Z)
    present_track = A[0]
    present_sector = A[1]
    seek_time = 0
    rotational_latency_time = 0
    total_response_time = 0
    transmission_time = 0
    variance = 0
    k = 0
    l = 0
    m = 0
    adod = 0
    if present_track >= 100:
        direction = 1
        for z in range(y):
            if Z[z] >= present_track:
                adod += 1
    else:
        direction = -1
        for z in range(y):
            if Z[z] <= present_track:
                adod += 1


    while m < 2:
        if direction == -1:
            if m == 0:
                t.right(165)
            else:
                t.right(150)
            while k < adod:
                next_distance = 199
                next_rotational_distance = 360
                for j in range(y):
                    distance = present_track - Z[j]
                    if distance >= 0:
                        if next_distance >= distance:
                            wb_sector = present_sector + (distance*90/199) * (360/8.3)
                            if wb_sector > 359:
                                wb_sector %= 360
                            if wb_sector <= C[j]:
                                radian = C[j] - wb_sector
                            else:
                                radian = 360 - (wb_sector - C[j])
                            if next_rotational_distance > radian:
                                next_track = Z[j]
                                next_sector = D[j]
                                next_distance = distance
                                next_rotational_latency_time = radian
                                next_position = j

                t.forward(next_distance*2.8)
                t.write(next_track)
                                
                seek_time += (next_distance*90/199)
                rotational_latency_time += ((next_rotational_latency_time/360)*8.3)
                response_time = seek_time + rotational_latency_time
                ZZ.append(response_time)
                total_response_time += seek_time + rotational_latency_time
                present_track = next_track
                present_sector = next_sector
                Z[next_position] = 400
                if m == 0:
                    Label(w,width=7,height=1,text=k).grid(row=3+k,column=5)
                    Label(w,width=7,height=1,text=present_track).grid(row=3+k,column=6)
                else:
                    Label(w,width=7,height=1,text=l+k).grid(row=4+l+k,column=5)
                    Label(w,width=7,height=1,text=present_track).grid(row=4+l+k,column=6)
                
                k += 1
            adod = len(Z) - adod
            direction = 1
            if m == 0:
                t.forward(present_track*2.8)
                seek_time += (present_track*90/199)
                present_sector += (present_track*10/199) * (360/8.3)
                if present_sector > 359:
                    present_sector %= 360
                present_track = 0
                t.write(present_track)
                Label(w,width=7,height=1,text="-").grid(row=3+k,column=5)
                Label(w,width=7,height=1,text=present_track).grid(row=3+k,column=6)
            m += 1
            l = k
            k = 0
            
        elif direction == 1:
            if m == 0:
                t.right(15)
            else:
                t.left(150)
            while k < adod:
                next_track = 199
                next_distance = 199
                next_rotational_distance = 360
                for j in range(y):
                    distance = Z[j] - present_track
                    if distance >= 0:
                        if next_distance >= distance:
                            wb_sector = present_sector + (distance*90/199) * (360/8.3)
                            if wb_sector > 359:
                                wb_sector %= 360
                            if wb_sector <= C[j]:
                                radian = C[j] - wb_sector
                            else:
                                radian = 360 - (wb_sector - C[j])
                            if next_rotational_distance > radian:
                                next_track = Z[j]
                                next_sector = D[j]
                                next_distance = distance
                                next_rotational_latency_time = radian
                                next_position = j

                t.forward(next_distance*2.8)
                t.write(next_track)
                                
                seek_time += (next_distance*90/199)
                rotational_latency_time += ((next_rotational_latency_time/360)*8.3)
                response_time = seek_time + rotational_latency_time
                ZZ.append(response_time)
                total_response_time += seek_time + rotational_latency_time
                present_track = next_track
                present_sector = next_sector
                Z[next_position] = 400
                if m == 0:
                    Label(w,width=7,height=1,text=k).grid(row=3+k,column=5)
                    Label(w,width=7,height=1,text=present_track).grid(row=3+k,column=6)
                else:
                    Label(w,width=7,height=1,text=l+k).grid(row=4+l+k,column=5)
                    Label(w,width=7,height=1,text=present_track).grid(row=4+l+k,column=6)
                
                k += 1
            adod = len(Z) - adod
            direction = -1
            if m == 0:
                next_distance = 199 - present_track
                t.forward(next_distance*2.8)
                seek_time += (next_distance*90/199)
                present_sector += (next_distance*10/199) * (360/8.3)
                if present_sector > 359:
                    present_sector %= 360
                present_track = 199
                t.write(present_track)
                Label(w,width=7,height=1,text="-").grid(row=3+k,column=5)
                Label(w,width=7,height=1,text=present_track).grid(row=3+k,column=6)
            m += 1
            l = k
            k = 0


    for a in range(len(ZZ)):
        deviation = (total_response_time/y) - ZZ[a]
        variance += deviation**2


    total_time["text"] = "Total time : " + str(int(seek_time + rotational_latency_time)) + "ms"
    result1["text"] = "Average Seek Time : " + str(int((seek_time/y)*100)/100) + "ms       Average Rotaional Latency Time : " + str(int((rotational_latency_time/y)*100)/100) + "ms"
    result2["text"] = "Transmission Time : " + str(int(((A[3]/360)*8.3)*100)/100) + "ms   Variance of Response Times  : " + str(int((variance/y)*100)/100) + " (ms)^2     Throughput : " + str(int((A[2]/(seek_time + rotational_latency_time))*100)/100) + " request/ms"


def C_LOOK():
    Turtle_set(A[0])
    t.write(A[0])
    Z = copy.deepcopy(B)
    ZZ=[]
    y = len(Z)
    present_track = A[0]
    present_sector = A[1]
    seek_time = 0
    rotational_latency_time = 0
    total_response_time = 0
    transmission_time = 0
    variance = 0
    k = 0
    l = 0
    m = 0
    adod = 0
    first = 199
    last = 0
    for l in range(y):
        if Z[l] < first:
            first = Z[l]
        if Z[l] > last:
            last = Z[l]
    if present_track >= 100:
        direction = 1
    else:
        direction = -1

    for l in range(y):            
        if direction == 1:
            if Z[l] >= present_track:
                adod += 1
        else:
            if Z[l] <= present_track:
                adod += 1
                
    while m < 2:
        if direction == -1:
            if m == 0:
                t.right(165)
            while k < adod:
                next_distance = 199
                next_rotational_distance = 360
                for j in range(y):
                    distance = present_track - Z[j]
                    if distance >= 0:
                        if next_distance >= distance:
                            wb_sector = present_sector + (distance*90/199) * (360/8.3)
                            if wb_sector > 359:
                                wb_sector %= 360
                            if wb_sector <= C[j]:
                                radian = C[j] - wb_sector
                            else:
                                radian = 360 - (wb_sector - C[j])
                            if next_rotational_distance > radian:
                                next_track = Z[j]
                                next_sector = D[j]
                                next_distance = distance
                                next_rotational_latency_time = radian
                                next_position = j

                t.forward(next_distance*2.8)
                t.write(next_track)
                                
                seek_time += (next_distance*90/199)
                rotational_latency_time += ((next_rotational_latency_time/360)*8.3)
                response_time = seek_time + rotational_latency_time
                ZZ.append(response_time)
                total_response_time += seek_time + rotational_latency_time
                present_track = next_track
                present_sector = next_sector
                Z[next_position] = 400
                if m == 0:
                    Label(w,width=7,height=1,text=k).grid(row=3+k,column=5)
                    Label(w,width=7,height=1,text=present_track).grid(row=3+k,column=6)
                else:
                    Label(w,width=7,height=1,text=l+k).grid(row=3+l+k,column=5)
                    Label(w,width=7,height=1,text=present_track).grid(row=3+l+k,column=6)
                k += 1
            if m == 0:
                next_distance = last - present_track 
                t.left(150)
                t.forward(next_distance*2.8)
                t.right(150)
                adod = len(Z) - adod
                present_track = last
            m += 1
            l = k
            k = 0
            
        elif direction == 1:
            if m == 0:
                t.right(15)
            while k < adod:
                next_distance = 199
                next_rotational_distance = 360
                for j in range(y):
                    distance = Z[j] - present_track
                    if distance >= 0:
                        if next_distance >= distance:
                            wb_sector = present_sector + (distance*90/199) * (360/8.3)
                            if wb_sector > 359:
                                wb_sector %= 360
                            if wb_sector <= C[j]:
                                radian = C[j] - wb_sector
                            else:
                                radian = 360 - (wb_sector - C[j])
                            if next_rotational_distance > radian:
                                next_track = Z[j]
                                next_sector = D[j]
                                next_distance = distance
                                next_rotational_latency_time = radian
                                next_position = j

                t.forward(next_distance*2.8)
                t.write(next_track)
                                
                seek_time += (next_distance*90/199)
                rotational_latency_time += ((next_rotational_latency_time/360)*8.3)
                response_time = seek_time + rotational_latency_time
                ZZ.append(response_time)
                total_response_time += seek_time + rotational_latency_time
                present_track = next_track
                present_sector = next_sector
                Z[next_position] = 400
                if m == 0:
                    Label(w,width=7,height=1,text=k).grid(row=3+k,column=5)
                    Label(w,width=7,height=1,text=present_track).grid(row=3+k,column=6)
                else:
                    Label(w,width=7,height=1,text=l+k).grid(row=3+l+k,column=5)
                    Label(w,width=7,height=1,text=present_track).grid(row=3+l+k,column=6)
                k += 1
            if m == 0:
                next_distance = present_track - first
                t.right(150)
                t.forward(next_distance*2.8)
                t.left(150)
                adod = len(Z) - adod
                present_track = first
            m += 1
            l = k
            k = 0

    for a in range(len(ZZ)):
        deviation = (total_response_time/y) - ZZ[a]
        variance += deviation**2


    total_time["text"] = "Total time : " + str(int(seek_time + rotational_latency_time)) + "ms"
    result1["text"] = "Average Seek Time : " + str(int((seek_time/y)*100)/100) + "ms        Average Rotaional Latency Time : " + str(int((rotational_latency_time/y)*100)/100) + "ms"
    result2["text"] = "Transmission Time : " + str(int(((A[3]/360)*8.3)*100)/100) + "ms   Variance of Response Times  : " + str(int((variance/y)*100)/100) + " (ms)^2     Throughput : " + str(int((A[2]/(seek_time + rotational_latency_time))*100)/100) + " request/ms"

def order_clear():
    for z in range(21):
         Label(w,width=7,height=1).grid(row=3+z,column=5)
         Label(w,width=7,height=1).grid(row=3+z,column=6)


w = Tk()

va = StringVar(w)
va.set("SSTF")

pol = Label(w,width=8,text="Policy")
sp = Label(w,width=5,text="start")
dq = Label(w,width=55,text="Disk Queue")
pol1 = OptionMenu(w,va,"SSTF","SCAN","C-LOOK")
pol1.config(width=8)
sp1 = Entry(w,width=5)
dq1 = Entry(w,width=55)
set1 = Button(w,width=5,text="Set",command=setting)
run = Button(w,width=5,text="Run",command=run)
tp = PhotoImage(file="Track.png")
tp1 = Label(w,image=tp,width=570,height=50,bg="white")
canvas = Canvas(w,width=570,height=350,bg="white")
total_time = Label(w,width=15,text="Total time : ",bg="white")
order = Label(w,width=7,height=1,text="Order")
order_track = Label(w,width=7,height=1,text="Track")
order_clear()
result1 = Label(w)
result2 = Label(w)
    

pol.grid(row=0, column=0)
sp.grid(row=0, column=1)
dq.grid(row=0, column=2)
pol1.grid(row=1, column=0)
sp1.grid(row=1, column=1)
dq1.grid(row=1, column=2)
set1.grid(row=1, column=3)
run.grid(row=1, column=4)
total_time.grid(row=1,column=5,columnspan=2)
tp1.place(x=4,y=50)
canvas.place(x=5,y=104)
order.grid(row=2,column=5)
order_track.grid(row=2,column=6)
result1.grid(row=22,column=0,columnspan=4)
result2.grid(row=23,column=0,columnspan=6)

t = turtle.RawTurtle(canvas)
t.ht()

w.mainloop()
