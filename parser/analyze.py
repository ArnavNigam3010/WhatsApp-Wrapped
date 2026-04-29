import numpy as np
import re
from datetime import datetime
import json

n=0 # number of people
dc={} # dictionary with index for each person 
day1=0 # first day (0 indexed)
daylast=0 # last day
numline=0 # line number
def num(): #number of people and stores index of person in dc
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
count=[0 for _ in range(n)] # messages per person
print(count)
words=[0 for _ in range(n)] # words per person
nightMsg=[0 for _ in range(n)] # night messages per person
tprs=[0 for _ in range(n)] # stores sum of times of direct replies by each person
cprs=[0 for _ in range(n)] # stores number of direct replies by each person
tRep=np.array([]) # Stores all reply times
editCount=[0 for _ in range(n)] # edits per person
maxT=0 # longest silence
convoStart=[0 for _ in range(n)] # conversations started per person
longVocabArr=[0 for _ in range(n)] # long words used per person
totalMsg=0 # total number of messages
lineprev="" # stores prev line as string, initialised to empty for first line
d={} # ?????????????????
maxFri=0 # maximum number of messages between any two people
I=0 # index of best friend 1
J=0 # index of best friend 2
emojiL=[{} for _ in range(n)] # list of count per emoji per person
top3_emoji=[] # top 3 emojis of each person
tprsbycprs=[0 for _ in range(n)] # average response time of each person
pairFrd=np.zeros((n,n)) # 2D array for message count between each pair of people
emoji_pattern = re.compile( # to check for emojis
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport
    "\U0001F1E0-\U0001F1FF"  # flags
    "]+",
    flags=re.UNICODE
)
def contains_emoji(text): # checks if text contains emojis
    return bool(emoji_pattern.search(text))
with open("chat.txt", "r", encoding="utf-8") as f: # reads chat line by line
    for line in f:
        numline+=1
        lengthLine=line.strip().split()
        numSplitCol=len(line.strip().split(":"))
        wordsNum=0
        LongVocCheck=0
        for i in range(2,numSplitCol):
            wordsNum+=len(line.strip().split(":")[i].strip().split())
            for j in line.strip().split(":")[i].strip().split():
                if (len(j)>=12): # check for long vocab
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
        time = fields[1]
        count[per]+=1
        words[per]+=wordsNum
        h=int(time.split(":")[0])
        if (h>=0 and h<=3):
            nightMsg[per]+=1
        if (lineprev!=""): # checks factors which depend on previous line
            fieldprev=lineprev.strip().split()
            t1=datetime.strptime(fieldprev[0]+" "+fieldprev[1], "%d-%m-%y, %H:%M")
            t2=datetime.strptime(fields[0]+" "+fields[1], "%d-%m-%y, %H:%M")
            diff=t2-t1
            maxT=max(maxT,diff.total_seconds())

            if(lineprev.strip().split("-")[3].strip().split(":")[0].strip()!=person):
                if (diff.total_seconds()>960 and int(time.split(":")[0])>3):
                    convoStart[per]+=1
                elif (diff.total_seconds()>2880 and int(time.split(":")[0])<=3):
                    convoStart[per]+=1
                tprs[per]+=diff.total_seconds()
                cprs[per]+=1
                tRep=np.append(tRep,diff.total_seconds())
                pairFrd[per][dc[lineprev.strip().split("-")[3].strip().split(":")[0].strip()]]+=1
        if fields[0].split(",")[0] in d:
            d[fields[0].split(",")[0]]+=1
        else:
            d[fields[0].split(",")[0]]=1
        if ("EDITED" in line):
            editCount[per]+=1
            words[per]-=4
        lineprev=line # end of file reading
with open ("chat.txt","r",encoding="utf-8") as file: # to find first and last day
    linect=1
    for line in file:
        if (linect==1):
            day1=line.strip().split(",")[0]
        if (linect==numline):
            daylast=line.strip().split(",")[0]
        linect+=1
date_format = "%d-%m-%y"
# datetime obj defined
start_date = datetime.strptime(day1, date_format)
end_date = datetime.strptime(daylast, date_format)
numdays = abs(end_date - start_date).days
numdays+=1
print(numdays)
toddarr=[[[0 for _ in range(12)] for _ in range(numdays)] for _ in range(n)] # stores data for heatmap
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
#find maxFri
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
avgRespTimenumpy=(1/60)*np.median(tRep)
print("Average numpy respT: ", avgRespTimenumpy)
print("Longest silence = ",maxT," sec")
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

for i in range(n):
    tprsbycprs[i]=(tprs[i]/cprs[i])

for i in range(len(emojiL)):
    emojiL[i]=dict(sorted(emojiL[i].items(),key=lambda a:-a[1]))
    c=0

    elt=[]
    for j in emojiL[i]:
        if c!=3:
            elt.append(j)
            c+=1
        else:
            break
    top3_emoji.append(elt)

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
conver=0
ghost=0

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

#print(toddarr[1])

nightowl=cMax(nightMsg,nightowl,"nightowl")
conver=cMax(convoStart,conver,"conver")
ghost=cMin(cprs,ghost,"ghost")
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
#LongVocab_DONE
#Editor_DONE
#Bestfrd1_DONE
#Bestfrd2_DONE
#Global Stats to be shown too_DONE