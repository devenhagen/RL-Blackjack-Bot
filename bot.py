import random
import copy

cards = {
    2:2,
    3:3,
    4:4,
    5:5,
    6:6,
    7:7,
    8:8,
    9:9,
    10:10,
    "J":10,
    "Q":10,
    "K":10,
    "A":1
}


q = dict()
for i in range(12,21):
    for j in range(1,11):
            state1 = [True,i,j]
            state2 = [False,i,j]
            q[(tuple(state1), "h")] = [0,0]
            q[(tuple(state2), "h")] = [0,0]
            q[(tuple(state1), "s")] = [0,0]
            q[(tuple(state2), "s")] = [0,0]

def game(exc, print_bool):
    state = [False,0,0]
    pc = random.choices(list(cards.keys()), k=2)
    dc = [random.choice(list(cards.keys()))]
    dcace = False
    if "A" in pc:
        state[0] = True
        state[1] += 10
    state[1] += cards[pc[0]] + cards[pc[1]]
    state[2] += cards[dc[0]]
    slist = []
    if print_bool:
        print("Player")
    while True:
        if print_bool:
            print(state[1])
        if state[1]>21 and not state[0]:
            for t in slist:
                q[t][0] = (q[t][0]*q[t][1]-1)/(q[t][1]+1)
                q[t][1]+=1
            return -1
        if state[1]>21 and state[0]:
            state[0] = False
            state[1] -=10
        if state[1] == 21:
            break
        if state[1]<12:
            i = random.choice(list(cards.keys()))
            if i == "A" and state[1]<11:
                state[0] = True
                state[1] += 10
            pc.append(i)
            state[1] += cards[pc[-1]]
            continue
        myp = random.random()
        if myp<exc:
            o = random.random()
            if o<0.5:
                kmal = copy.deepcopy(state)
                slist.append((tuple(kmal),"h"))
                pc.append(random.choice(list(cards.keys())))
                state[1] += cards[pc[-1]]
                continue
            else:
                kmal = copy.deepcopy(state)
                slist.append((tuple(kmal),"s"))
                break
        else:
            mval = ""
            if q[(tuple(state),"h")][0]>q[(tuple(state),"s")][0]:
                mval = "h"
            else:
                mval = "s"
            if mval == "h":
                kmal = copy.deepcopy(state)
                slist.append((tuple(kmal),"h"))
                pc.append(random.choice(list(cards.keys())))
                state[1] += cards[pc[-1]]
                continue
            else:
                kmal = copy.deepcopy(state)
                slist.append((tuple(kmal),"s"))
                break
    if print_bool:
        print("Dealer")
    if "A" in dc:
        dcace = True
        state[2] += 10
    while state[2]<17:
        if print_bool:
            print(state[2])
        i = random.choice(list(cards.keys()))
        if i=="A" and state[2]<11:
            dcace = True
            state[2]+=10
        dc.append(i)
        state[2] += cards[dc[-1]]
        if state[2]>21 and dcace:
            dcace = False
            state[2]-=10
    if print_bool:
        print(state[2])
    if state[2]>21:
        for t in slist:
            q[t][0] = (q[t][0]*q[t][1]+1)/(q[t][1]+1)
            q[t][1]+=1
        return 1
    if state[1]>state[2]:
        for t in slist:
            q[t][0] = (q[t][0]*q[t][1]+1)/(q[t][1]+1)
            q[t][1]+=1
        return 1
    if state[1] == state[2]:
        for t in slist:
            q[t][0] = (q[t][0]*q[t][1])/(q[t][1]+1)
            q[t][1]+=1
        return 0
    for t in slist:
        q[t][0] = (q[t][0]*q[t][1]-1)/(q[t][1]+1)
        q[t][1]+=1
    return -1

def greedy_game():
    state = [False,0,0]
    pc = random.choices(list(cards.keys()), k=2)
    dc = [random.choice(list(cards.keys()))]
    dcace = False
    if "A" in pc:
        state[0] = True
        state[1] += 10
    state[1] += cards[pc[0]] + cards[pc[1]]
    state[2] += cards[dc[0]]
    while True:
        if state[1]>21 and not state[0]:
            return -1
        if state[1]>21 and state[0]:
            state[0] = False
            state[1] -=10
        if state[1] == 21:
            break
        if state[1]<12:
            i = random.choice(list(cards.keys()))
            if i == "A" and state[1]<11:
                state[0] = True
                state[1] += 10
            pc.append(i)
            state[1] += cards[pc[-1]]
            continue
        mval = ""
        if q[(tuple(state),"h")][0]>q[(tuple(state),"s")][0]:
            mval = "h"
        else:
            mval = "s"
        if mval == "h":
            pc.append(random.choice(list(cards.keys())))
            state[1] += cards[pc[-1]]
            continue
        else:
            break
    if "A" in dc:
        dcace = True
        state[2] += 10
    while state[2]<17:
        i = random.choice(list(cards.keys()))
        if i=="A" and state[2]<11:
            dcace = True
            state[2]+=10
        dc.append(i)
        state[2] += cards[dc[-1]]
        if state[2]>21 and dcace:
            dcace = False
            state[2]-=10
    if state[2]>21:
        return 1
    if state[1]>state[2]:
        return 1
    if state[1] == state[2]:
        return 0
    return -1


rew = 0
for i in range(10000000):
    rew+=game(0.1, False)
#print(rew)

#rew = 0
#for i in range(1000000):
#    rew += greedy_game()
#print(rew)


print("Smallest stick values without a usable ace")
for c in cards:
    val = 0
    for i in range(12,21):
        if q[((False, i, cards[c]),"h")][0]<q[((False, i, cards[c]),"s")][0]:
            val = i
            break
    print("Dealer's card val is", str(c) + ":", val)
print()
print("Smallest stick values with a usable ace")
for c in cards:
    val = 0
    for i in range(12,21):
        if q[((True, i, cards[c]),"h")][0]<q[((True, i, cards[c]),"s")][0]:
            val = i
            break
    print("Dealer's card val is", str(c) + ":", val)
