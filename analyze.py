import numpy as np
import re
from datetime import datetime
import json
#BestFrds and Editor code to be added
#Ghost direct reply
n=0
dc={}
day1=0
daylast=0
numline=0
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
#heatmap=[[[0 for _ in range(n)] for _ in range(12)] for _ in range(days)]
count=[0 for _ in range(n)]
print(count)
words=[0 for _ in range(n)]
nightMsg=[0 for _ in range(n)]
#dirRep=np.array([0,0,0,0,0,0,0])#Number of direct replies received by the person
tprs=[0 for _ in range(n)]#stores sum of times of direct replies by each person
cprs=[0 for _ in range(n)]#stores number of direct replies by each person
tRep=np.array([])#Stores all reply times
editCount=[0 for _ in range(n)]
maxT=0
convoStart=[0 for _ in range(n)]
longVocabArr=[0 for _ in range(n)]
totalMsg=0
line1=""
d={}
maxFri=0
I=0
J=0
emojiL=[{} for _ in range(n)]
top3_emoji=[]
tprsbycprs=[0 for _ in range(n)]
pairFrd=np.zeros((n,n))
print("shape: ",pairFrd.shape)
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
        numline+=1
        #if ("[THIS MESSAGE WAS EDITED]" in line):
        lengthLine=line.strip().split()
        numSplitCol=len(line.strip().split(":"))
        wordsNum=0
        LongVocCheck=0
        for i in range(2,numSplitCol):
            wordsNum+=len(line.strip().split(":")[i].strip().split())
            for j in line.strip().split(":")[i].strip().split():
                if (len(j)>=12):
                    LongVocCheck+=1
        person = line.strip().split("-")[3].strip().split(":")[0].strip()
        per=dc[person]
        longVocabArr[per]+=LongVocCheck
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
        words[per]+=wordsNum
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
                tRep=np.append(tRep,diff.total_seconds())
                pairFrd[per][dc[line1.strip().split("-")[3].strip().split(":")[0].strip()]]+=1
        if fields[0].split(",")[0] in d:
            d[fields[0].split(",")[0]]+=1
        else:
            d[fields[0].split(",")[0]]=1
        if ("EDITED" in line):
            editCount[per]+=1
            words[per]-=4
        line1=line #end
with open ("chat.txt","r",encoding="utf-8") as file:
    linect=1
    for line in file:
        if (linect==1):
            day1=line.strip().split(",")[0]
        if (linect==numline):
            daylast=line.strip().split(",")[0]
        linect+=1
date_format = "%d-%m-%y"
start_date = datetime.strptime(day1, date_format)
end_date = datetime.strptime(daylast, date_format)
numdays = abs(end_date - start_date).days
numdays+=1
print(numdays)
toddarr=[[[0 for _ in range(12)] for _ in range(numdays)] for _ in range(n)]
with open ("chat.txt","r",encoding="utf-8") as file:
    for line in file:
        day=line.strip().split(",")[0]
        time=int(line.strip().split(",")[1].strip().split(":")[0])
        day_int=(datetime.strptime(day, date_format) - start_date).days
        time_int = int(time/2)
        person0 = line.strip().split("-")[3].strip().split(":")[0].strip()
        per0=dc[person0]
        toddarr[per0][day_int][time_int]+=1
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
np.sort(tRep)
l=len(tRep)
#avgRepT=(1/60)*(tRep[int(l/2)]+tRep[int((l-1)/2)])/2
avgRespTimenumpy=(1/60)*np.median(tRep)
print("Average numpy respT: ", avgRespTimenumpy)
print("Longest silence = ",maxT," sec")
#print("Avg Resp Time = ",avgRepT, " min")
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
print("longvocarray: ",longVocabArr)
#print("dirRep: ",dirRep)
#print("tRep: ",tRep)
for i in range(n):
    tprsbycprs[i]=(tprs[i]/cprs[i])
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
longMsgPer=0
#print(f"wordslong/countlong={words[longMsgPer]/count[longMsgPer]}")
for i in range(n):
    #print(f"words{i}/count{i}: {words[i]/count[i]}")
    if ((words[i]/count[i])>(words[longMsgPer]/count[longMsgPer])):
        longMsgPer=i
print("longMsgPer: ",longMsgPer)
nightowl=0
'''for i in range(n):
    if ((nightMsg[i])>(nightMsg[nightowl])):
        nightowl=i
print("nightowl: ",nightowl)'''
conver=0
'''for i in range(n):
    if ((convoStart[i])>(convoStart[nightowl])):
        conver=i
print("conver: ",conver)'''
ghost=0
'''for i in range(n):
    if ((cprs[i])<(cprs[ghost])):
        ghost=i
print("ghost: ",ghost)'''
def cMax(arr,var,str):
    for i in range(n):
        if (arr[i]>arr[var]):
            var=i
    print(f"{str}: ",var)
    return var
def cMin(arr,var,str):
    for i in range(n):
        if (arr[i]<arr[var]):
            var=i
    print(f"{str}: ",var)
    return var
print(toddarr[1])
nightowl=cMax(nightMsg,nightowl,"nightowl")
conver=cMax(convoStart,conver,"conver")
ghost=cMin(cprs,ghost,"ghost")
#cMax(EmojiaRR)
hypeper=0
hypeper=cMax(count,hypeper,"hypeper")
print(hypeper)
editorP=0
editorP=cMax(editCount,editorP,"editorP")
avgRespTime=int(avgRespTimenumpy)
sum=np.zeros(n)
for i in range(n):
    for x in emojiL[i]:
        sum[i]+=emojiL[i][x]
emojiTalk=0
emojiSum=list(sum)
emojiTalk=cMax(sum,emojiTalk,"emojiTalk")
longVocaber=0
longVocaber=cMax(longVocabArr,longVocaber,"longVocaber")
bf1="Best Friends with "+inv_dc[J]
bf2="Best Friends with "+inv_dc[I]
#bf1="Best Friend 1"
#bf2="Best Friend 2"
totalWords=np.array(words)
TotalWords=int(np.sum(totalWords))
chat_stats = {
    "dict": dc,
    "inv_dict": inv_dc,
    "Long Messager": longMsgPer,
    "Night Owl": nightowl,
    "Conversation Starter": conver,
    "Ghost": ghost,
    "Hype Person": hypeper,
    "Message Editor": editorP,
    "Long Vocabulary User": longVocaber,
    "total_messages_arr": count,
    "total_words_arr": words,
    "night_msg_arr": nightMsg,
    "count_rep_arr": cprs,
    "convoStart_arr": convoStart,
    "emoji_arr": emojiL,
    "Emoji Talker": emojiTalk,
    "total_emoji_per_person": emojiSum,
    "top3_emoji_arr": top3_emoji,
    "busiest_day_arr": busiest,
    "longest_silence": maxT,
    "average_resp_time": avgRespTime,
    "tprsbycprs_arr": tprsbycprs,
    "totalMsg": totalMsg,
    "totalwords": TotalWords,
    "editCounter": editCount,
    "maxFriend": maxFri,
    bf1: I,
    bf2: J,
    "bestFriends": (I,J),
    "length": n,
    "longvocarray": longVocabArr,
    "todd": toddarr,
    "number_of_days": numdays
}
with open('data.json', 'w') as f:
    json.dump(chat_stats, f, indent=4)

print("Data successfully exported to data.json")
print(emojiL)
#LongMsg_DONE
#NightOwl_DONE
#ConvoStarter_DONE
#Ghost_DONE
#EmojiTalker_DONE
#HypePer_DONE
#LongVocab_TBD
#Editor_DONE
#Bestfrd1_DONE
#Bestfrd2_DONE
#Global Stats to be shown too