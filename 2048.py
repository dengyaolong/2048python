#!/usr/bin/env python
# coding=utf-8
#********************************************************
# > OS     : Linux 3.2.0-60-generic #91-Ubuntu
#	> Author : yaolong
#	> Mail   : dengyaolong@yeah.net
#	> Time   : 2014年06月01日 星期日 13:13:39
#********************************************************
import random
import copy

def display(mtrx): #output function
    a = ("┌", "├", "├", "├", "└")
    b = ("┬", "┼", "┼", "┼", "┴")
    c = ("┐", "┤", "┤", "┤", "┘")
    for i in range(4):
        print a[i] + ("─" * 5 + b[i]) * 3 + ("─" * 5 + c[i])
        for j in range(4):
            print "│%4s" % (mtrx[i][j] if mtrx[i][j] else ' '),
        print "│"
    print a[4] + ("─" * 5 + b[4]) * 3 + ("─" * 5 + c[4])

def init(): #initial of matrix
    mtr = [[0 for i in range(4)] for j in range(4)]  
    ran_pos = random.sample(range(16), 2)
    mtr[ran_pos[0]/4][ran_pos[0]%4] = mtr[ran_pos[1]/4][ran_pos[1]%4] = 2
    return mtr

def go_on(mtr, score):#check for the game is over ?
    if 2048 in mtr: #2048 and win 
        print "Great!You win!Your score is ", score
        raw_input("Press any key to continue...")
        exit()
    if 0 in mtr: #can insert number！
        return True
    for i in range(4): 
        for j in range(4):   #can merge number!
            if i < 3 and mtr[i][j] == mtr[i + 1][j]:
                return True
            if j < 3 and mtr[i][j] == mtr[i][j + 1]:
                return True
    print "Gameover!"
    return False

def move(mtr, dirct):#the core code!move by the four direction
    score = 0
    visit = []
    if dirct == 0:  # left
        for i in range(4):
            for j in range(1, 4):
                for k in range(j,0,-1):
                    if mtr[i][k - 1] == 0 :
                        mtr[i][k - 1] = mtr[i][k]
                        mtr[i][k] = 0
                    elif mtr[i][k - 1] == mtr[i][k] and 4 * i + k - 1 not in visit and 4 * i + k not in visit:
                        mtr[i][k - 1] *= 2
                        mtr[i][k] = 0
                        score += mtr[i][k - 1]
                        visit.append(4 * i + k)
                        visit.append(4 * i + k - 1)
    elif dirct == 1:  # down
        for j in range(4):
            for i in range(3, 0, -1):
                for k in range(0,i):
                   if mtr[k+1][j] == 0:
                      mtr[k+1][j] = mtr[k][j]
                      mtr[k][j]=0
                   elif mtr[k+1][j]==mtr[k][j] and (4 *(k+1)+j) not in visit and (4*k+j) not in visit:
                      mtr[k+1][j]*=2
                      mtr[k][j]=0
                      score=mtr[k+1][j]
                      visit.append(4*(k)+j)
                      visit.append(4*(k+1)+j)
    elif dirct == 2:  # up
        for j in range(4):
            for i in range(1,4):
                for k in range(i,0,-1):
                    if mtr[k-1][j]==0:
                        mtr[k-1][j]=mtr[k][j]
                        mtr[k][j]=0
                    elif mtr[k-1][j]==mtr[k][j] and (4 *(k-1)+j) not in visit and (4*k+j) not in visit:
                        mtr[k-1][j]*=2
                        mtr[k][j]=0
                        score += mtr[k-1][j]
                        visit.append(4*(k)+j)
                        visit.append(4*(k-1)+j)
    elif dirct == 3:  # right
        for i in range(4):
            for j in range(3, 0, -1):
                for k in range(j):
                   if mtr[i][k+1]  == 0:
                      mtr[i][k+1] = mtr[i][k]
                      mtr[i][k]=0
                   elif mtr[i][k] ==mtr[i][k+1] and 4 * i + k + 1 not in visit and 4 * i + k not in visit:
                      mtr[i][k+1]*=2
                      mtr[i][k]=0
                      score+=mtr[i][k+1]
                      visit.append(4*i+k+1)
                      visit.append(4*i+k)
    return score

def update(mtr):
    ran_pos=[]
    ran_num=[2,4]
    for i in range(4):
        for j in range(4):
            if mtr[i][j]==0:
               ran_pos.append(4*i+j)
    if len(ran_pos)>0:# can insert
        k=random.choice(ran_pos)
        n=random.choice(ran_num)
        mtr[k/4][k%4]=n

declare = "←：a/h  ↓: s/j ↑: w/k →: d/l ,q(uit),b(ack)"
illegal = "Illegal operation!"
noefficient = "This move has no efficient"
score = 0
step = 0
mtr = init()  # init the matrix
mtr_stk = []  # use step for back
scr_stk = []
tmp = copy.deepcopy(mtr)
mtr_stk.append(tmp) #push the init matrix ensure the stack is not empty
scr_stk.append(0)
display(mtr)
if __name__ == '__main__':
    while go_on(mtr, score):
        dirct = raw_input("Step :%d Score :%d (%s):" % (step, score, declare))
        dirct = dirct.lower()#ensure the direction operation is lower
        # map 0 left,1 down,2 up ,3 right
        if dirct == "q":  #quit
            break
        elif dirct == "a" or dirct == "h":#normal mode and the vim mode
            dirct = 0
        elif dirct == "s" or dirct == "j":
            dirct = 1
        elif dirct == "w" or dirct == "k":
            dirct = 2
        elif dirct == "d" or dirct == "l":
            dirct = 3
        elif dirct == "b":
            if len(mtr_stk) == 1: #step one
                print "Can't Back.."
            else:
                mtr_stk.pop()   #pop up 
                scr_stk.pop()   
                step -= 1       #step back
                mtr = copy.deepcopy(mtr_stk[-1]) #matrix back
                score = scr_stk[-1]
            continue        #no move
        else:
            print illegal    #not in the operation set
            continue         #has no move
        tmp = copy.deepcopy(mtr)   #use to compare the move is efficient ?
        op_scr = move(mtr, dirct)
        if tmp != mtr:
            score = score + op_scr  #the move gains
            update(mtr) #insert a number values of 2 or 4
            tmp = copy.deepcopy(mtr)  #need to deep copy..
            mtr_stk.append(tmp)  # use to back
            scr_stk.append(int(score))  
            step +=1  #step++
            display(mtr)  #output the matrix
        else:
            print noefficient
print "Your score is :",score
