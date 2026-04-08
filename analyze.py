import numpy as np
import re
from datetime import datetime
import json
#BestFrds and Editor code to be added
#Ghost direct reply
n=0
dc={}
def num():
    global n,dc
    s=set()
    with open("chat.txt","r",encoding="utf-8") as f:
        for line in f:
            pers=line.strip().split("-")[3].strip().split(":")[0].strip()
            if(pers not in s):
                dc[pers]=n
                n+=1
                s.add(pers)
num()
count=[0 for _ in range(n)]
print(count)
words=[0 for _ in range(n)]
nightMsg=[0 for _ in range(n)]
#dirRep=np.array([0,0,0,0,0,0,0])#Number of direct replies received by the person
tprs=[0 for _ in range(n)]#stores sum of times of direct replies by each person
cprs=[0 for _ in range(n)]#stores number of direct replies by each person
tRep=[]#Stores all reply times
editCount=[0 for _ in range(n)]
maxT=0
convoStart=[0 for _ in range(n)]
totalMsg=0
line1=""
d={}
maxFri=0
I=0
J=0
emojiL=[{} for _ in range(n)]
top3_emoji=[]
tprsbycprs=[]
pairFrd=[[0 for _ in range(n)] for _ in range(n)]
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport
    "\U0001F1E0-\U0001F1FF"  # flags
    "]+",
    flags=re.UNICODE
)
def contains_emoji(text):
    return bool(emoji_pattern.search(text))
with open("chat.txt", "r", encoding="utf-8") as f:
    for line in f:
        #if ("[THIS MESSAGE WAS EDITED]" in line):
        person = line.strip().split("-")[3].strip().split(":")[0].strip()
        per=dc[person]
        fields = line.strip().split()   # default: splits by whitespace
        for x in fields:
            if contains_emoji(x):
                if x in emojiL[per]:
                    emojiL[per][x]+=1
                else:
                    emojiL[per][x]=1
        #dayNum = fields[1]
        time = fields[1]
        count[per]+=1
        words[per]+=len(line.strip().split(":")[2].strip().split())
        h=int(time.split(":")[0])
        if (h>=0 and h<=3):
            nightMsg[per]+=1
        if (line1!=""):
            field1=line1.strip().split()
            t1=datetime.strptime(field1[0]+" "+field1[1], "%d-%m-%y, %H:%M")
            t2=datetime.strptime(fields[0]+" "+fields[1], "%d-%m-%y, %H:%M")
            #dirRep[int(field1[2])]+=1
            #print("per purana: ",field1[2]," per naya: ", per)
            diff=t2-t1
            maxT=max(maxT,diff.total_seconds())
            #print(maxT)
            if(line1.strip().split("-")[3].strip().split(":")[0].strip()!=person):
                if (diff.total_seconds()>960 and int(time.split(":")[0])>3):
                    convoStart[per]+=1
                elif (diff.total_seconds()>2880 and int(time.split(":")[0])<=3):
                    convoStart[per]+=1
                tprs[per]+=diff.total_seconds()
                #print(fields[1]," ",diff.total_seconds())
                cprs[per]+=1
                tRep.append(diff.total_seconds())
                pairFrd[per][dc[line1.strip().split("-")[3].strip().split(":")[0].strip()]]+=1
        if fields[0].split(",")[0] in d:
            d[fields[0].split(",")[0]]+=1
        else:
            d[fields[0].split(",")[0]]=1
        if ("EDITED" in line):
            editCount[per]+=1
        line1=line #end
m=0
for i in range(n):
    for j in range(i,n):
        if (pairFrd[i][j]+pairFrd[j][i]>maxFri):
            I=i
            J=j
            maxFri=pairFrd[i][j]+pairFrd[j][i]
for t in d:
    m=max(m,d[t])
busiest=[]
for t in d:
    if (d[t]==m):
        busiest.append(t)
print(dc)
print("d = ",d)
print("Busiest: ",busiest)
tRep.sort()
l=len(tRep)
avgRepT=(1/60)*(tRep[int(l/2)]+tRep[int((l-1)/2)])/2
print("Longest silence = ",maxT," sec")
print("Avg Resp Time = ",avgRepT, " min")
print("convoStart = ",convoStart)
print("Count arr = ",count)
print("Words arr = ",words)
print("Night msg = ",nightMsg)
print("pairFrd: ",pairFrd)
inv_dc = {i: w for w,i in dc.items()}
totalMsg=0
for i in range(len(count)):
    totalMsg+=count[i]
print("Total Msg = ",totalMsg)
print("tprs: ",tprs)
print("cprs: ",cprs)
print("Edit Count: ",editCount)
print("I: ",inv_dc[I])
print("J: ",inv_dc[J])
print("maxFri: ",maxFri)
#print("dirRep: ",dirRep)
#print("tRep: ",tRep)
for i in range(n):
    tprsbycprs.append(tprs[i]/cprs[i])
    #print("tprs/cprs of ",i," : ",tprs[i]/cprs[i])
for i in range(len(emojiL)):
    emojiL[i]=dict(sorted(emojiL[i].items(),key=lambda a:-a[1]))
    c=0
    #print(i," ",end="")
    elt=[]
    for j in emojiL[i]:
        if c!=3:
            #print(j, end=" ")
            elt.append(j)
            c+=1
        else:
            break
    top3_emoji.append(elt)
    #print()
#print(inv_dc)
#print(emojiL)
#print(top3_emoji)
chat_stats = {
    "dict": dc,
    "inv_dict": inv_dc,
    "total_messages_arr": count,
    "total_words_arr": words,
    "night_msg_arr": nightMsg,
    "count_rep_arr": cprs,
    "convoStart_arr": convoStart,
    "emoji_arr": emojiL,
    "top3_emoji_arr": top3_emoji,
    "busiest_day_arr": busiest,
    "longest_silence": maxT,
    "average_resp_time": avgRepT,
    "tprsbycprs_arr": tprsbycprs,
    "totalMsg": totalMsg,
    "editCounter": editCount,
    "maxFriend": maxFri,
    "bestFri1": I,
    "bestFri2": J
}
with open('data.json', 'w') as f:
    json.dump(chat_stats, f, indent=4)

print("Data successfully exported to data.json")