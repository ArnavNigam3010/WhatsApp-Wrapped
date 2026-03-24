import numpy as np
from numpy import random
import random
import re

#Night Owl
#Ghost
#Convo Starter
#Hype Person
#Emoji talker
#Chhota msg
#Lamba vocab user
#Best friends
#3rd day talker

#Probability of each person messaging at time t and the message too
#Prev message, person who sent prev msg, time of prev msg
#who, kya, time delay, time randomness
#who -> prev person, time of the day (wrt person being night owl or not)
#kya -> personality (emoji/lamba vocab/chhota msg)
#time delay -> rand (weighted wrt time of the day), prev msg time

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
def LongMsg():
    p=[0,0.01,0.01,0.002,0.01,0.01,0.01,0.2,0.3,0.286]
    cump=[0,0,0,0,0,0,0,0,0,0]
    prev=0
    for i in range(0,10):
        cump[i]=prev+p[i]
        prev=cump[i]
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
    s1="LongMsg: "+s1
    #print(s1)
    return s1
LongMsg()
def NightOwl():
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
    s1="NightOwl: "+s1
    #print(s1)
    return s1
NightOwl()
def ChatGen():
    ttime=0
    players=[0,1,2,3,4,5,6]
    prob=[0.14,0.14,0.14,0.14,0.14,0.15,0.15]
    cprob=[0,0,0,0,0,0,0]
    for i in range(0,7):
        if (i==0):
            cprob[i]=prob[i]
        cprob[i]=cprob[i-1]+prob[i]
    while (ttime<=420000):
        tmin=1
        tmax=1200
        if (ttime%86400>0 and ttime%86400<14400):
            tmin=600
            tmax=3600
            prob[1]=0.5
            for i in {0,2,3,4,5,6}:
                prob[i]=prob[i]-0.06
            cprob1=[0,0,0,0,0,0,0]
            for i in range(0,7):
                if (i==0):
                    cprob1[i]=prob[i]
                cprob1[i]=cprob1[i-1]+prob[i]
        else:
            cprob1=cprob
        tap=np.random.randint(tmin,tmax)
        per=np.random.rand()
        #print(cprob1)
        #print("Per: ",per)
        person=0
        for i in range(0,7):
            if (per<cprob1[i]):
                person=i
                break
        #print("Person: ", person)
        ttime+=tap
        tday=ttime%86400
        h=int(tday/3600)
        m=int((tday%3600)/60)
        if (person==0):
            s="Day "+str(int(ttime/86400))+" "+str(h)+":"+str(m)+" "+str(person)+" "+LongMsg()
            with open ("data.txt", "a", encoding="utf-8") as f:
                f.write(s)
                f.write("\n")
            #print(s)
        elif (person==1):
            s="Day "+str(int(ttime/86400))+" "+str(h)+":"+str(m)+" "+str(person)+" "+NightOwl()
            with open ("data.txt", "a", encoding="utf-8") as f:
                f.write(s)
                f.write("\n")
            #print(s)
        else:
            s="Day "+str(int(ttime/86400))+" "+str(h)+":"+str(m)+" "+str(person)+" Person: "+str(person)+" "+LongMsg()
            with open ("data.txt", "a", encoding="utf-8") as f:
                f.write(s)
                f.write("\n")
            #print(s)
ChatGen()