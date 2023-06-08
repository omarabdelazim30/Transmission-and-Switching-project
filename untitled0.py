import math
import numpy as np
def blockprobab(l, ch):
    L = (l ** ch) / math.factorial(ch)
    sum_ = 0
    for n in range(ch + 1): 
        sum_ += (l ** n) / math.factorial(n)
    p=L / sum_
    return p
ReuseSector=list()
def Find_N():
    for i in range(1,6):
        for j in range(0,i+1):
            N = i*i + i*j + j*j
            ReuseSector.append([N,i,j,0,0,0])
    ReuseSector.sort()
    for l in ReuseSector:  
        if(l[1]==l[2]):
            l[3]=1
            l[4]=3
            l[5]=4
        else:
            l[3]=1
            l[4]=2
            l[5]=3
    print(ReuseSector)        

def No_of_Cells(city_size,city_pop,lamda,avg_duration,channels,channels_cell,Pb,sectoring,CperI,slot_ratio):
   users_city=math.floor(city_size*city_pop)
   #print(str(lamda)+" "+str(avg_duration))
   a_user = (lamda/(24*60))*avg_duration
   cells = 1
   Pb=Pb/100
   if (sectoring==360):                                
       N=channels/channels_cell
       channels_cell=math.floor(channels_cell*slot_ratio)
       a_cell=0
       p=0
       #print(channels_cell)
       while (True):
           a_cell+=0.01
           p=blockprobab(a_cell,channels_cell)
           if(p>=Pb):
               break
           
       #print(str(p)+" "+str(a_cell)+" "+str(a_user)+" "+str(users_city))   
       if(a_cell/a_user>=1):
           users_cell=math.floor(a_cell/a_user)
           cells=math.ceil(users_city/users_cell)
       else:
           print("cannot devide by zero")
   else:
       sectors=360/sectoring
       if (sectoring==10):
         x=3
       elif(sectoring==120):
         x=4
       elif(sectoring==180):
         x=5    
       for i in range(len(ReuseSector)):
            N=ReuseSector[i][0]
            n=ReuseSector[i][x]
            if ((3*N/n)>=CperI):
                break
      # print("N= "+str(N))         
       channels_cell =  (channels/N )*slot_ratio
     #  channels_sector=channels_cell/sectors
       a_sector=0
       p=0
       channels_sector=math.ceil(channels_cell/sectors)
       #print(channels_sector)
       while (True):
           a_sector+=0.01
           p=blockprobab(a_sector,channels_sector)
           if(p>=Pb):
               break
       if(a_sector*sectors/a_user>=1):
         users_cell=math.floor(a_sector*sectors/a_user)
         cells=math.ceil(users_city/users_cell)
       else:
           print("cannot devide by zero")  
   return cells            
Find_N()
city_size=eval(input("Enter the size of the city in km2 \n"))
city_pop=eval(input("Enter the population of the city (number of users per km2) \n"))
lamda=eval(input("Enter number of calls per day \n"))
avg_duration=eval(input("Enter average call duration \n"))
channels=eval(input("Enter number of channels available for the service provider \n")) 
channels_cell=eval(input("Enter number of channels per cell \n"))
blocking_prob=eval(input("Enter blocking probability \n"))
CperI=eval(input("Enter C/I \n"))
slot_ratio=eval(input("Enter slot ratio \n"))
Sectoring=[360,10,120,180]
out=list()
out.append(No_of_Cells(city_size, city_pop, lamda,avg_duration, channels, channels_cell, blocking_prob, 360 , CperI, slot_ratio)) 
print("No sectoring : Cells = "+str(out[0])+'\n')
out.append(No_of_Cells(city_size, city_pop, lamda,avg_duration, channels, channels_cell, blocking_prob, 10 , CperI, slot_ratio)) 
print("10 deg sectoring : Cells = "+str(out[1])+'\n')
out.append(No_of_Cells(city_size, city_pop, lamda,avg_duration, channels, channels_cell, blocking_prob, 120 , CperI, slot_ratio)) 
print("120 deg sectoring : Cells = "+str(out[2])+'\n')
out.append(No_of_Cells(city_size, city_pop, lamda,avg_duration, channels, channels_cell, blocking_prob, 180 , CperI, slot_ratio)) 
print("180 deg sectoring : Cells = "+str(out[3])+'\n')
m=np.max(out)
i=out.index(m)
print("The best secctoring is "+str(Sectoring[i])+ " Degree " + " Cells = "+str(m))