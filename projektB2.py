#!/usr/bin/env python
# coding: utf-8

import numpy as np
import random
import time
import matplotlib.pyplot as plt
import scipy.stats as scs
import seaborn as sns
sns.set()

def krok(p):
    a=np.random.rand()
    if a<p:
        return 1
    else:
        return -1

def podrB2(n,il,p,pocz):
    mok=0
    zost_par=np.full([n+1,1],False)
    mam_par=True
    miejsce=pocz
    i=0
    
    while(il>i):
        k=krok(p)
        if k == -1:
            if mam_par:
                zost_par[miejsce]=True
                mam_par=False
        if k == 1:
            if zost_par[miejsce] or mam_par:
                zost_par[miejsce]=False
                mam_par=True
            else:
                mok=mok+1
                
        miejsce_pop=miejsce
        while(miejsce==miejsce_pop):
            miejsce=random.randrange(1,n+1)
        i=i+1
    return mok/il

def zycieB2(il_pow,m,n,p):
    wyn=[]
    for i in range(il_pow):
        pocz=random.randrange(1,n+1)
        sym=podrB2(n,m,p,pocz)
        wyn.append(sym)
    return wyn

def symulacjaB2(il_pow,m,n,p):
    start = time.time()
    print("Symulacja dla parametrów n =",n,"p =",p,"m = ",m)
    wsp=(p*(n-1)*(1-p))/(1+(n-1)*(1-p))
    sym=zycieB2(il_pow,m,n,p)
    pvalks=round(scs.kstest(sym,'norm',args=(np.mean(sym),np.std(sym)))[1],4)
    pvalts=round(scs.ttest_1samp(sym,wsp)[1],4)
    if pvalks>1-poz_uf:
        print("Przyjmujemy hipoteze zerową w teście normalności Kołmogorowa-Smirnova. Rozkład jest normalny.")
        print("pvalue wyniosło",pvalks)
        if pvalts>1-poz_uf:
            print("Przyjmujemy hipoteze zerową w teście t-Studenta. Wartość średnia jest naszą wartością oczekiwaną.")
            print("pvalue wyniosło",pvalts)
            tekst = """
            Symulacja dla parametrów n = {n}, p = {p:5.2f}, m = {m}
            Przyjmujemy hipoteze zerową w teście normalności Kołmogorowa-Smirnova. Rozkład jest normalny.
            pvalue wyniosło {pvalks}
            Przyjmujemy hipoteze zerową w teście t-Studenta. Wartość średnia jest naszą wartością oczekiwaną.
            pvalue wyniosło {pvalts}
            Różnica pomiędzy średnią a wartością oczekiwaną wynosi {roz}            
            """ 
            zmienne = {
             "n":n, 
             "p":p,
             "m":m,
             "pvalks": pvalks,
             "pvalts" : pvalts,
             "roz" : abs(np.mean(sym)-wsp)
             } 
            with  open('symB2.txt','a',encoding="utf-8") as myfile:
                myfile.write(tekst.format(**zmienne))
        else:
            print("Odrzucamy hipoteze zerową w teście t-Studenta. Wartość średnia nie jest naszą wartością oczekiwaną.")
            print("pvalue wyniosło",pvalts)
            tekst = """
            Symulacja dla parametrów n = {n}, p = {p:5.2f}, m = {m}
            Przyjmujemy hipoteze zerową w teście normalności Kołmogorowa-Smirnova. Rozkład jest normalny.
            pvalue wyniosło {pvalks}
            Odrzucamy hipoteze zerową w teście t-Studenta. Wartość średnia nie jest naszą wartością oczekiwaną.
            pvalue wyniosło {pvalts}
            Różnica pomiędzy średnią a wartością oczekiwaną wynosi {roz}
            """ 
            zmienne = {
             "n":n, 
             "p":p,
             "m":m,
             "pvalks": pvalks,
             "pvalts" : pvalts,
             "roz" : abs(np.mean(sym)-wsp)
             }
            with  open('symB2.txt','a',encoding="utf-8") as myfile:
                myfile.write(tekst.format(**zmienne))
    else:
        print("Odrzucamy hipoteze zerową w teście normalności Kołmogorowa-Smirnova. Rozkład nie jest normalny.")
        print("pvalue wyniosło",pvalks)
        tekst = """
        Symulacja dla parametrów n = {n}, p = {p:5.2f}, m = {m}
        Odrzucamy hipoteze zerową w teście normalności Kołmogorowa-Smirnova. Rozkład nie jest normalny.
        pvalue wyniosło {pvalks}
        Różnica pomiędzy średnią a wartością oczekiwaną wynosi {roz}        
        """ 
        zmienne = {
            "n":n, 
            "p":p,
            "m":m,
            "pvalks": pvalks,
             "roz" : abs(np.mean(sym)-wsp)
            }
        with  open('symB2.txt','a',encoding="utf-8") as myfile:
            myfile.write(tekst.format(**zmienne))        
    print("")
    end = time.time()
    print("Symulacja wykonana w",end - start,"sekund")
    return sym

il_pow=10000
n=1000
m=[100,1000,10000,100000]
p=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
poz_uf=0.95

fig,axes = plt.subplots(len(m),len(p),figsize=(32,16))
for i in range(len(m)):
    for j in range(len(p)):
        sym=symulacjaB2(il_pow,m[i],n,p[j])
        sns.distplot(sym,ax=axes[i,j]).set_title("p = " + str(p[j]) + ", m = " + str(m[i]))
plt.savefig("symB2n2.png")
plt.show()

il_pow=10000
n=10000
m=[100,1000,10000,100000]
p=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
poz_uf=0.95

fig,axes = plt.subplots(len(m),len(p),figsize=(32,16))
for i in range(len(m)):
    for j in range(len(p)):
        sym=symulacjaB2(il_pow,m[i],n,p[j])
        sns.distplot(sym,ax=axes[i,j]).set_title("p = " + str(p[j]) + ", m = " + str(m[i]))
plt.savefig("symB2.png")
plt.show()

il_pow=10000
n=100000
m=[100,1000,10000,100000]
p=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
poz_uf=0.95

fig,axes = plt.subplots(len(m),len(p),figsize=(32,16))
for i in range(len(m)):
    for j in range(len(p)):
        sym=symulacjaB2(il_pow,m[i],n,p[j])
        sns.distplot(sym,ax=axes[i,j]).set_title("p = " + str(p[j]) + ", m = " + str(m[i]))
plt.savefig("symB2n3.png")
plt.show()

