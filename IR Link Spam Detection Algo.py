"""
Reading the HostGraph and creating the Adjacency Matrix
"""
f=open('/home/shubham/Desktop/spam/src/uk-2007-05.hostgraph_weighted (copy).graph-txt','r')
N=f.readline()
n=int(float(N))

adjacencyMatrix=[[0 for x in range(0,n)] for x in range(0,n)]
for i in range(0,n):
    x=f.readline()
    if(x!='\n'):
        l=x.split()
        for j in range(0,len(l)):
            x=l[j].split(':')
            adjacencyMatrix[i][int(float(x[0]))-1]=int(float(x[1]))

f.close()







"""
Reading the Training Set and creating the BlackList
"""
f=open('/home/shubham/Desktop/spam/src/WEBSPAM-UK2007-SET1-labels (copy).txt','r')
blackList=[]
while 1:
    x=f.readline()
    if not x:
        break
    l=x.split()
    if(l[1]=='spam'):
        blackList.append(int(float(l[0]))-1)
f.close()










"""
========> Reverse Spam Rank Algorithm
"""
I=[]
for i in range(0,n):
    if(i in blackList):
        I.append(1)
    else:
        I.append(0)


lmbd = 0.85
forwardLink=[]
inLink=[]
sumf=0
sumi=0
for i in range(0,n):
    sumf=0
    sumi=0
    for j in range(0,n):
        sumf+=adjacencyMatrix[i][j]
        sumi+=adjacencyMatrix[j][i]
    forwardLink.append(sumf)
    inLink.append(sumi)

def checkConverge(list1,list2):
    flag=1
    for i in range(0,len(list1)):
        if(-0.0001>(list1[i]-list2[i]) or (list1[i]-list2[i])>0.0001):
            flag=0
            break
    return flag

RSR=[]
for i in range(0,n):
    RSR.append(I[i])

rsr=[0 for i in range(0,n)]
ctr=0
for k in range(0,100):
    for i in range(0,n):
        ctr=0
        for j in range(0,n):
            if(inLink[j]!=0):
                ctr=ctr + adjacencyMatrix[i][j]*RSR[j]/inLink[j]
        rsr[i]=((1-lmbd)*I[i])+(lmbd*ctr)

    if(checkConverge(rsr,RSR)==1):
        break
    else:
        for i in range(0,n):
            RSR[i]=rsr[i]








"""
Evaluting and computing Authority/Quality Scaore
"""
f=open('/home/shubham/Desktop/spam/src/WEBSPAM-UK2007-hostnames (copy).txt','r')
gd=[]
for i in range(0,n):
    x=f.readline()
    p=x.split()
    q=p[1].split('.')
    if(q[len(q)-2]=='gov'):
        gd.append(0)
    elif(q[len(q)-2]=='ac'):
        gd.append(0.4)
    elif(q[len(q)-2]=='org'):
        gd.append(0.5)
    elif(q[len(q)-2]=='co'):
        gd.append(0.6)
    else:
        gd.append(0.75)
f.close()







"""
================> R SpamRank + GD Scores
"""
gRSR=[]
for i in range(0,n):
    gRSR.append(RSR[i]+gd[i])

tmpGRSR=[0 for x in range(0,n)]
for i in range(0,n):
    tmpGRSR[i]=gRSR[i]


"""
Sorting gRSR scores to get athreshold value
"""
for i in range(0,n):
    for j in range(i,n):
        if(tmpGRSR[i]<tmpGRSR[j]):
            t=tmpGRSR[i];
            tmpGRSR[i]=tmpGRSR[j];
            tmpGRSR[j]=t;
            

th=tmpGRSR[len(blackList)-1]
print(th)







"""
Finding New States with respect to above calculated threshold
"""
state=[]
for i in range(0,n):
    if(gRSR[i]>=th):
        state.append('spam')
    else:
        state.append('nonspam')











"""
=============> Final Spam Pages using Forward Propogation too
"""
for i in range(0,n):
    for j in range(0,n):
        if(adjacencyMatrix[i][j]==1 and state[i]=='nonspam' and gRSR[i]<0.6):
            state[j]='nonspam'
            

for i in range(0,n):
    print(str(i)+" "+state[i])







"""
Comparing Results with Test Set 1
"""
print()
print("Test Set 1 Results :-") 
f=open('/home/shubham/Desktop/spam/src/WEBSPAM-UK2007-SET2-labels (copy).txt','r')
tp=0
tn=0
fp=0
fn=0
while 1:
    x=f.readline()
    if not x:
        break
    l=x.split()
    if(l[1]=='spam' and state[int(float(l[0]))]=='spam'):
        tp+=1
    elif(l[1]=='spam' and state[int(float(l[0]))]=='nonspam'):
        fn+=1
    elif(l[1]=='nonspam' and state[int(float(l[0]))]=='spam'):
        fp+=1
    elif(l[1]=='nonspam' and state[int(float(l[0]))]=='nonspam'):
        tn+=1
f.close()

print("True Positive : \t"+str(tp))
print("False Positive : \t"+str(fp))
print("True Negative : \t"+str(tn))
print("False Neagtive : \t"+str(fn))
print()








"""
Comparing Results with Test Set 1
"""
print("Test Set 2 Results :-") 
f=open('/home/shubham/Desktop/spam/src/WEBSPAM-UK2007-SET3-labels (copy).txt','r')
tp=0
tn=0
fp=0
fn=0
while 1:
    x=f.readline()
    if not x:
        break
    l=x.split()
    if(l[1]=='spam' and state[int(float(l[0]))]=='spam'):
        tp+=1
    elif(l[1]=='spam' and state[int(float(l[0]))]=='nonspam'):
        fn+=1
    elif(l[1]=='nonspam' and state[int(float(l[0]))]=='spam'):
        fp+=1
    elif(l[1]=='nonspam' and state[int(float(l[0]))]=='nonspam'):
        tn+=1
f.close()

print("True Positive : \t"+str(tp))
print("False Positive : \t"+str(fp))
print("True Negative : \t"+str(tn))
print("False Neagtive : \t"+str(fn))








        

