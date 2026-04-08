import numpy as np
from numpy import random
import random
import re
from datetime import datetime,timedelta

'''
IDEAS
1) instead of calling each function in loop together define probabilities of each function being called based on tap.
2) defining states based on tap value and tap value will be biased based on time ranges
3) maybe function to change the tap probability distribution over time ranges
4) boolean marker for end of convo(maybe last message of ghost) and change tap prob distribution after this
5 Functions classify into classes so that modularity is maintained here too
'''

'''
STUFF TBD
1 Classifying emojis and lamba vocab
2 Classify chhota msg
3 3rd day talker -> probs have to be such that probs don't become negative
4 !!!!!!! change ttime and tap it should come after if else as tap may change for Hype
5 !!! f.write() seedhe end mein karna hai
'''

'''
NEXT TBD
1 Number of people has to first be found by parsing the file
'''

#Night Owl
#Ghost
#Convo Starter
#Hype Person
#Emoji talker///
#Chhota msg
#Lamba vocab user///
#Best friends
#3rd day talker
#editor most


#Probability of each x[0] messaging at time t and the message too
#Prev message, x[0] who sent prev msg, time of prev msg
#who, kya, time delay, time randomness
#who -> prev x[0], time of the day (wrt x[0] being night owl or not)
#kya -> x[0]ality (emoji/lamba vocab/chhota msg)
#time delay -> rand (weighted wrt time of the day), prev msg time

with open("chat.txt", "w", encoding="utf-8"):
    pass

tokens = []

with open("vocabulary.txt", "r", encoding="utf-8") as file:
    for line in file:
        parts=line.strip().split(",")
        tokens.extend(parts)

vocab={}
for word in tokens:
    if word not in vocab:
        vocab[word]=len(vocab)

arr=np.array([vocab[word] for word in tokens])

#print("Tokens: ", tokens)
#print("Vocab: ", vocab)
#print("Words: ", word)
#print("Array: ", arr)


inv_vocab = {i: w for w,i in vocab.items()}
#print(inv_vocab)

#0 LongMsg
#1 NightOwl
#2 ConvoStarter
#3 Ghost
#4 Emoji
#5 HypePer
#6 LongVocab
'''Using re lib seems like the work done is the same only in both the cases


tokens1 = []

with open("vocabulary.txt", "r", encoding="utf-8", errors="ignore") as file:
    for line in file:'''
        #parts=re.findall(r'\b\w+\b', line.lower())
        #tokens1.extend(parts)

'''vocab1={}

for word in tokens1:
    if word not in vocab1:
        vocab1[word]=len(vocab1)

token_ids = np.array([vocab1[word] for word in tokens1], dtype=np.int32)

print("Tokens: ", tokens1)
print("Vocab: ", vocab1)
print("Token IDs: ", token_ids)'''
#NLP Track Trigram word use
'''x = np.random.randint(1030, size=np.random.randint(1,11))
#print(x)
s=""
for i in x:
    s+=(inv_vocab[i]+" ")
print(s)'''
ttime=0
players=[0,1,2,3,4,5,6,7,8,9]
playerName=["Arnav Nigam","Sanidhya Saraf","Sahil Deo","Vishad Jain","Parth Vartak","Garv Pahwa","Ujjwal Kesari","Chirayu Jain","Kahan Atara","Piusa Das"]
prob=np.array([0.105,0.105,0.075,0.034,0.105,0.29,0.106,0.106,0.037,0.037])
tmin=1
tmax=1200
tap=0
prev=-1
emojis=[]
longvocabs=[]
d = datetime(2026, 7, 1, 0, 0)
def pMod(i,s):
    global prob
    prob[i]*=s
    prob=prob/prob.sum()
def is_LongVocab(token):
    return bool(len(token)>=12)
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
def LongVocabArr():
    global longvocabs
    for i in range(arr.size-1):
        s=inv_vocab[i]
        if((not contains_emoji(s)) and is_LongVocab(s)):
            longvocabs.append(i)
LongVocabArr()
def EmojiArr():
    global emojis
    for i in range(arr.size-1):
        s=inv_vocab[i]
        if (contains_emoji(s)):
            #print(s)
            emojis.append(i)
EmojiArr()
#print(emojis)
def LongVocab():
    global ttime
    global prob
    global players
    global tmin
    global tmax
    global tap
    global emojis
    global longvocabs
    z=np.random.randint(1,18)
    s=""
    while(z>0):
        x=np.random.rand()
        if (x<=0.70):
            y=np.random.choice(longvocabs)
            s+=inv_vocab[y]+" "
        else:
            y1=np.random.randint(0,arr.size-1)
            s+=inv_vocab[y1]+" "
        z-=1
    return s
def EmojiTalker():
    global ttime
    global prob
    global players
    global tmin
    global tmax
    global tap
    global emojis
    z=np.random.randint(1,18)
    s=""
    while(z>0):
        x=np.random.rand()
        if (x<=0.50):
            y=np.random.choice(emojis)
            s+=inv_vocab[y]+" "
        else:
            y1=np.random.randint(0,arr.size-1)
            s+=inv_vocab[y1]+" "
        z-=1
    return s
#print(np.random.choice(emojis))
def LongMsg():
    p=[0,0.01,0.01,0.002,0.01,0.01,0.01,0.2,0.3,0.286]
    cump=[0,0,0,0,0,0,0,0,0,0]
    prev1=0
    for i in range(0,10):
        cump[i]=prev1+p[i]
        prev1=cump[i]
    y=np.random.rand()
    #print(y)
    z=0
    for i in range(0,10):
        if (y<cump[i]):
            z=i
            break
    x2 = np.random.randint(1030, size=np.random.randint(5*z+1,5*z+6))
    s1=""
    for i in x2:
        s1+=(inv_vocab[i]+" ")
    #s1="LongMsg: "+s1
    #print(s1)
    return s1
#LongMsg()
def printer():
    '''time=[0.3,0.3,0.01,0.01,0.01,0.1,0.1,0.05,0.05,0.03,0.03,0.01]
    ctime=[0,0,0,0,0,0,0,0,0,0,0,0]
    prev=0
    for i in range(0,12):
        ctime[i]=prev+time[i]
        prev=ctime[i]
    y=np.random.rand()
    print(y)
    z=0
    for i in range(0,12):
        if (y<ctime[i]):
            z=i
            break
    h=np.random.randint(z,z+2)
    m=np.random.randint(60)'''
    x3 = np.random.randint(1030, size=np.random.randint(1,18))
    s1=""
    for i in x3:
        s1+=(inv_vocab[i]+" ")
    #s1=str(h)+":"+str(m)+" NightOwl: "+s1
    #s1="NightOwl: "+s1
    #print(s1)
    return s1
#NightOwl()
def NightOwl():
    global ttime
    global prob
    global players
    global tmin
    global tmax
    global tap
    if (ttime%86400>0 and ttime%86400<14400):
        tmin=600
        tmax=3600
        pMod(1,10)
    else:
        tmin=1
        tmax=1200
def ConvoStarter():
    global ttime
    global prob
    global players
    global tmin
    global tmax
    global tap
    global prev
    if(tap>0.8*tmax):
        pMod(2,3)
def Ghost():
    global ttime
    global prob
    global players
    global tmin
    global tmax
    global tap
    global prev
    if(prev==3):
        pMod(3,50)
def HypePer():
    global ttime
    global prob
    global players
    global tmin
    global tmax
    global tap
    global prev
    ttime-=2*tap/3
def bestFrds():
    global prev
    global prob
    global players
    if (prev==8):
        pMod(9,30)
    elif (prev==9):
        pMod(8,30)
def ChatGen():
    global ttime
    global prob
    global players
    global tmin
    global tmax
    global tap
    global prev
    '''
    cprob=[0,0,0,0,0,0,0]
    for i in range(0,7):
        if (i==0):
            cprob[i]=prob[i]
        cprob[i]=cprob[i-1]+prob[i]

    '''
    orig=prob.copy()
    #print(orig, "ORIG")
    orig=orig/orig.sum()
    while (ttime<=4200000):
        NightOwl()
        tap=np.random.randint(tmin,tmax)
        #print("wgsf ",prob)
        #print("ORIG ", orig)
        ConvoStarter()
        Ghost()
        bestFrds()
        #call all functions here after modifying probabilities
        #HypePer() to be called only when HypePer is the chosen per
        #prob=np.array(prob)
        prob = prob/prob.sum()
        #print(prob)
        x=int(np.random.choice(players,p=prob))
        #print(x)
        
        #else:
            #cprob1=cprob
        #print(prob)
        #per=np.random.rand()
        #print(cprob1)
        #print("Per: ",per)
        '''x[0]=0
        for i in range(0,7):
            if (per<cprob1[i]):
                x[0]=i
                break
        '''
        #print("x[0]: ", x[0])
        ttime+=tap
        if (x==0):#LongMsg
            s=playerName[x]+": "+LongMsg()
            prev=0
            #print(s)
        elif (x==1):#NightOwl
           # NightOwl()
            s=playerName[x]+": "+printer()
            prev=1
            #print(s)
        elif (x==2):#ConvoStarter
            #ConvoStarter()
            s=playerName[x]+": "+printer()
            prev=2
            #print(s)
        elif (x==3):#Ghost
            #Ghost()
            s=playerName[x]+": "+printer()
            prev=3
            #print(s)
        elif (x==4):#EmojiTalker
            s=playerName[x]+": "+EmojiTalker()
            prev=4
            #print(s)
        elif (x==5):#HypePer
            HypePer()
            s=playerName[x]+": "+printer()
            prev=5
            #print(s)
        elif (x==6):#LongVocab
            s=playerName[x]+": "+LongVocab()
            prev=6
            #print(s)
        elif (x==7):#editor
            prev=7
            s=playerName[x]+": "+printer()
        elif (x==8):#bestFrd1
            prev=8
            s=playerName[x]+": "+printer()
        elif (x==9):#bestFrd2
            prev=9
            s=playerName[x]+": "+printer()
        delta = timedelta(seconds=ttime)
        result=d+delta
        result=result.strftime("%d-%m-%y, %H:%M ")
        tday=ttime%86400
        h=int(tday/3600)
        m=int((tday%3600)/60)
        with open ("chat.txt", "a", encoding="utf-8") as f:
            f.write(str(result)+"- ")
            f.write(s)
            f.write(" ")
            x1=np.random.rand()
            if (x==7):
                if (x1>0.5):
                    f.write("[THIS MESSAGE WAS EDITED]")
            else:
                if (x1>0.95):
                    f.write("[THIS MESSAGE WAS EDITED]")
            f.write("\n")
        prob=orig.copy()
ChatGen()