
import numpy as np
import pandas as pd
import math

def GOS_Erlang(C,A):
    num = (A**float(C))/float(math.factorial(C))
    sum =0
    for k in range(C+1):
        sum+= (A**k)/float(math.factorial(k))
    GOS = num/sum
    return GOS

'''E_Erlang function computes the capacity in Erlang for a given Grade of Service and number of channel.
The function uses the GOS_Erlang and perform a binary search for the capacity '''

def E_Erlang(GOS,channel):
    a_test= float(0)
    b_test = float(channel)
    c_test= (a_test+b_test)/2
    GOS_a = GOS_Erlang(channel,a_test)
    GOS_b = GOS_Erlang(channel,b_test)
    GOS_c = GOS_Erlang(channel,c_test)
    while(math.fabs(GOS-GOS_c) >.000001):
        if(GOS_c<GOS):
            a_test=c_test
        else:
            b_test=c_test
        c_test= (a_test+b_test)/2
        GOS_c = GOS_Erlang(channel,c_test)
    return c_test




city_size = 450
Number_of_user_per_KM = 30
total_number_of_users = Number_of_user_per_KM * city_size
landa = 10 / (24 * 60)
E_x = 1
Total_chanel = 125
max_numb_of_chanel_per_cell = 50
blocking_prob = 0.5/100
sectoring = [10, 120, 180, 360]
data = pd.read_csv("Erlang_Table.csv")
reuse_factor=[1,3,4,7,9,12,13,16]
interferance_first_sector=[1,1,1,1,1,1,1,1]
interferance_second_sector=[2,3,2,2,2,3,2,2]
interferance_third_sector=[3,4,3,3,3,4,3,3]
interferance_fourth_sector=[6,6,6,6,6,6,6,6]
C_over_I=7





h=0
for m in sectoring:
   # print(m)
    max_numb_of_cells = 0
    best_reuse = 0
    best_sector = 0
    if(m==10):
        sector=interferance_first_sector
    if (m == 120):
        sector = interferance_second_sector
    if (m == 180):
        sector = interferance_third_sector
    if (m == 360):
        sector = interferance_fourth_sector
    #print(sector)
    p=0
    while(p<len(sector)):
       # print(C_over_I)
       # print(reuse_factor[p])
      #  print(sector[p])
        if(C_over_I<=3*(reuse_factor[p]/sector[p])):

            best_sector=sector[p]
            best_reuse=reuse_factor[p]
            break
        p=p+1

    temp = 360 / m

    trunk = math.floor(Total_chanel / best_reuse)
    trunk = trunk / temp
    trunk=math.floor(trunk)
    if (trunk <= max_numb_of_chanel_per_cell):
        erlang_per_user = landa * E_x

        blocking = blocking_prob
        print("trunk ",trunk,"blocking of ",blocking)
        erlang_per_cell = E_Erlang(blocking,trunk) # we need to get the dic in python
        subs_per_cell = math.floor(erlang_per_cell * temp / erlang_per_user)
        nb_of_cells = math.ceil(total_number_of_users / subs_per_cell)


    print("max number of users per cell is ", nb_of_cells, "for reuse factor of ", best_reuse, " and sectoring of ",
      sectoring[h])
    h=h+1
