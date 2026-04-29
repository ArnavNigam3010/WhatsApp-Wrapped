import sys
import numpy as np
from numpy import random
import random
import re
from datetime import datetime,timedelta

#code cleanup, comments filtering, removing unnecessar code, but still need the previous portions of the code for detailing in the challenges
"""
1. Vectorization - converting to numpy
2. HTML/CSS Multi
3. Saare ek jagah
4. Slideshow
5. NLTK
6. Comparison slides - graphs for several stuff in one/subplots
"""
""""
Merge commit: NLTK
"""
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
#Best friends 1 and 2
#editor most


#Probability of each person messaging at time t and the message too
#Prev message, person who sent prev msg, time of prev msg
#who, kya, time delay, time randomness
#who -> prev person, time of the day (wrt person being night owl or not)
#kya -> personality (emoji/lamba vocab/chhota msg)
#time delay -> rand (weighted wrt time of the day), prev msg time

with open("chat.txt", "w", encoding="utf-8"):
    pass

tokens = [] #stores the words in the vocabulary

with open(sys.argv[1], "r", encoding="utf-8") as file:
    for line in file:
        parts=line.strip().split(",")
        tokens.extend(parts) #storing words

vocab={} #converting tokens to numbers for orderly access
for word in tokens:
    if word not in vocab:
        vocab[word]=len(vocab) #Ensures only unique words are taken

numwords=len(vocab)

#print("Tokens: ", tokens)
#print("Vocab: ", vocab)
#print("Words: ", word)


inv_vocab = {i: w for w,i in vocab.items()} #stores word corresponding to a number
#print(inv_vocab)

#0 LongMsg
#1 NightOwl
#2 ConvoStarter
#3 Ghost
#4 Emoji
#5 HypePer
#6 LongVocab
#7 Editor
#8 BestFrd 1
#9 BestFrd 2

#global var
ttime=0
players=[0,1,2,3,4,5,6,7,8,9]
playerName=["Arnav Nigam","Sanidhya Saraf","Sahil Deo","Vishad Jain","Parth Vartak","Garv Pahwa","Ujjwal Kesari","Chirayu Jain","Kahan Atara","Piusa Das"]
prob=np.array([0.105,0.105,0.075,0.034,0.105,0.29,0.106,0.106,0.037,0.037]) #probability distribution array for chat corresponding to each person
tmin=1                      #message interval lower bound while picking randomly
tmax=1200                   #message interval upper bound while picking randomly
tap=0                       #Time of message After Previous msg (basically time interval between two messages)
prev=-1                     #index of previous person initialised to -1 to prevent ambiguities
emojis=[]
longvocabs=[]
d = datetime(2026, 7, 1, 0, 0) #startdate and time
def pMod(i,s): #Skews the probability in favour of one person selectively
    global prob
    prob[i]*=s
    prob=prob/prob.sum()
def is_LongVocab(token): #Checks long word
    return bool(len(token)>=12)
emoji_pattern = re.compile( #checks emoji
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport
    "\U0001F1E0-\U0001F1FF"  # flags
    "]+",
    flags=re.UNICODE
)
def contains_emoji(text): #checks if text contains emoji
    return bool(emoji_pattern.search(text))
def LongVocabArr(): #array of long words
    global longvocabs
    for i in range(numwords-1):
        s=inv_vocab[i]
        if((not contains_emoji(s)) and is_LongVocab(s)):
            longvocabs.append(i)
LongVocabArr()
def EmojiArr(): #array of emojis
    global emojis
    for i in range(numwords-1):
        s=inv_vocab[i]
        if (contains_emoji(s)):
            #print(s)
            emojis.append(i)
EmojiArr()
#print(emojis)
def LongVocab(): #returns a string containing proportionally higher long words
    z=np.random.randint(1,18)
    s=""
    while(z>0):
        x=np.random.rand()
        if (x<=0.70):
            y=np.random.choice(longvocabs)
            s+=inv_vocab[y]+" "
        else:
            y1=np.random.randint(0,numwords-1)
            s+=inv_vocab[y1]+" "
        z-=1
    return s
def EmojiTalker():#returns a string containing proportionally higher number of emojis
    z=np.random.randint(1,18)
    s=""
    while(z>0):
        x=np.random.rand()
        if (x<=0.10):
            y=np.random.choice(emojis)
            s+=inv_vocab[y]+" "
        else:
            y1=np.random.randint(0,numwords-1)
            s+=inv_vocab[y1]+" "
        z-=1
    return s
def LongMsg():#returns a long message whose length is skewed towards a higher number of words using array p
    arr=np.arange(10)
    p1=np.array([0,0.01,0.01,0.002,0.01,0.01,0.01,0.2,0.3,0.286])
    p1=p1/p1.sum()
    z=np.random.choice(arr,p=p1)
    x2 = np.random.randint(1030, size=np.random.randint(5*z+1,5*z+6))
    s1=""
    for i in x2:
        s1+=(inv_vocab[i]+" ")
    #s1="LongMsg: "+s1
    #print(s1)
    return s1
#LongMsg()
def printer():#general message generator for personalities whose effect doesn't come on their message length
    x3 = np.random.randint(1030, size=np.random.randint(1,18))
    s1=""
    for i in x3:
        s1+=(inv_vocab[i]+" ")
    #s1=str(h)+":"+str(m)+" NightOwl: "+s1
    #s1="NightOwl: "+s1
    #print(s1)
    return s1
#NightOwl()
def NightOwl():#Modifies the time bounds to make messages sparse at night
    global tmin
    global tmax
    if (ttime%86400>0 and ttime%86400<14400):
        tmin=600
        tmax=3600
        pMod(1,10)
    else:
        tmin=1
        tmax=1200
def ConvoStarter():#When the time interval crosses a particular bound it increases the probability of the convoStart person to initiate the convo
    if(tap>0.8*tmax):
        pMod(2,3)
def Ghost():#When previous message is by Ghost, increases prob of Ghost messaging again, going on a messaging spree, thus messaging in sparse clusters
    if(prev==3):
        pMod(3,50)
def HypePer():#Effectively makes the tap to tap/3 for HypePerson
    global ttime
    ttime-=2*tap/3
def bestFrds():#Alternate messaging higher prob between best friends
    if (prev==8):
        pMod(9,35)
    elif (prev==9):
        pMod(8,35)
def ChatGen():
    global ttime
    global prob
    global players
    global tmin
    global tmax
    global tap
    global prev
    orig=prob.copy()#creates a copy of prob array, to be modified, so that original array is not lost
    #print(orig, "ORIG")
    orig=orig/orig.sum()#normalisation
    while (ttime<=8400000):
        NightOwl()
        tap=np.random.randint(tmin,tmax)#randomly choses a time interval betweeen two messages
        ConvoStarter()
        Ghost()
        bestFrds()
        #call all functions here after modifying probabilities
        #HypePer() to be called only when HypePer is the chosen per
        prob = prob/prob.sum()
        x=int(np.random.choice(players,p=prob))
        ttime+=tap#updates the time of current message
        if (x==0):#LongMsg
            s=playerName[x]+": "+LongMsg()
            prev=0
        elif (x==1):#NightOwl
            s=playerName[x]+": "+printer()
            prev=1
        elif (x==2):#ConvoStarter
            s=playerName[x]+": "+printer()
            prev=2
        elif (x==3):#Ghost
            s=playerName[x]+": "+printer()
            prev=3
        elif (x==4):#EmojiTalker
            s=playerName[x]+": "+EmojiTalker()
            prev=4
        elif (x==5):#HypePer
            HypePer()
            s=playerName[x]+": "+printer()
            prev=5
        elif (x==6):#LongVocab
            s=playerName[x]+": "+LongVocab()
            prev=6
        elif (x==7):#editor
            prev=7
            s=playerName[x]+": "+printer()
        elif (x==8):#bestFrd1
            prev=8
            s=playerName[x]+": "+printer()
        elif (x==9):#bestFrd2
            prev=9
            s=playerName[x]+": "+printer()
        delta = timedelta(seconds=ttime) #convert the current ttime to a datetime obj
        result=d+delta #datetime obj of current message time updated using the initial reference time (d)
        result=result.strftime("%d-%m-%y, %H:%M ")#formatting
        tday=ttime%86400
        h=int(tday/3600)
        m=int((tday%3600)/60)
        with open ("chat.txt", "a", encoding="utf-8") as f:#writing into chat.txt line by line
            f.write(str(result)+"- ")
            f.write(s)
            f.write(" ")
            x1=np.random.rand()#probabilistic determination of the message being edited
            if (x==7):
                if (x1>0.5):
                    f.write("[THIS MESSAGE WAS EDITED]")
            else:
                if (x1>0.95):
                    f.write("[THIS MESSAGE WAS EDITED]")
            f.write("\n")
        prob=orig.copy()#updating prob
ChatGen()