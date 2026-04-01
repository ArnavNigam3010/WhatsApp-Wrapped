import numpy as np
import re
from datetime import datetime

#Ghost direct reply

count=np.array([0,0,0,0,0,0,0])
words=np.array([0,0,0,0,0,0,0])
nightMsg=np.array([0,0,0,0,0,0,0])
dirRep=np.array([0,0,0,0,0,0,0])#Number of direct replies received by the person
tprs=np.array([0,0,0,0,0,0,0])#stores sum of times of direct replies by each person
cprs=np.array([0,0,0,0,0,0,0])#stores number of direct replies by each person
tRep=np.array([])#Stores all reply times
totalMsg=0
line1=""
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        fields = line.strip().split()   # default: splits by whitespace
        
        #dayNum = fields[1]
        time = fields[1]
        per = int(fields[2])
        count[per]+=1
        words[per]+=len(fields)-3
        h=int(time.split(":")[0])
        if (h>=0 and h<=3):
            nightMsg[per]+=1
        if (line1!=""):
            field1=line1.strip().split()
            if(int(field1[2])!=per):
                t1=datetime.strptime(field1[0]+" "+field1[1], "%d-%m-%y %H:%M")
                t2=datetime.strptime(fields[0]+" "+fields[1], "%d-%m-%y %H:%M")
                dirRep[int(field1[2])]+=1
                #print("per purana: ",field1[2]," per naya: ", per)
                diff=t2-t1
                tprs[per]+=diff.total_seconds()
                cprs[per]+=1
                tRep=np.append(tRep,diff.total_seconds())
        line1=line #end
print("Count arr = ",count)
print("Words arr = ",words)
print("Night msg = ",nightMsg)
totalMsg=count.sum()
print("Total Msg = ",totalMsg)
print("tprs: ",tprs)
print("cprs: ",cprs)
print("dirRep: ",dirRep)
#print("tRep: ",tRep)
for i in range(7):
    if cprs[i]!=0:
        print("tprs/cprs of ",i," : ",tprs[i]/cprs[i])
    else:
        print("cprs of ",i," is 0")