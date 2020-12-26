#!/usr/bin/env python
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

def podrA(n,p):
    mok=0
    mam_par=True
    for i in range(n):
        k=krok(p)
        if k == -1:
            if mam_par:
                mam_par=False
        if k == 1:
            if mam_par:
                continue
            else:
                mok=mok+1
    return (mok/n)

def zycieA(il_pow,n,p):
    wyn=[]
    for i in range(il_pow):
        sym=podrA(n,p)
        wyn.append(sym)
    return wyn

def symulacjaA(il_pow,n,p):
    start = time.time()
    print("Symulacja dla parametrów n =",n,"p =",p)
    wsp=(p*(n-1)*(1-p))/(1+(n-1)*(1-p))
    sym=zycieA(il_pow,n,p)
    pvalks=round(scs.kstest(sym,'norm',args=(np.mean(sym),np.std(sym)))[1],4)
    pvalts=round(scs.ttest_1samp(sym,wsp)[1],4)
    if pvalks>1-poz_uf:
        print("Przyjmujemy hipoteze zerową w teście normalności Kołmogorowa-Smirnova. Rozkład jest normalny.")
        print("pvalue wyniosło",pvalks)
        if pvalts>1-poz_uf:
            print("Przyjmujemy hipoteze zerową w teście t-Studenta. Wartość średnia jest naszą wartością oczekiwaną.")
            print("pvalue wyniosło",pvalts)
            tekst = """
            Symulacja dla parametrów n = {n}, p = {p:5.2f}
            Przyjmujemy hipoteze zerową w teście normalności Kołmogorowa-Smirnova. Rozkład jest normalny.
            pvalue wyniosło {pvalks}
            Przyjmujemy hipoteze zerową w teście t-Studenta. Wartość średnia jest naszą wartością oczekiwaną.
            pvalue wyniosło {pvalts}
            Różnica pomiędzy średnią a wartością oczekiwaną wynosi {roz}
            """ 
            zmienne = {
             "n":n, 
             "p":p,
             "pvalks": pvalks,
             "pvalts" : pvalts,
             "roz" : abs(np.mean(sym)-wsp)
             } 
            with  open('symA.txt','a',encoding="utf-8") as myfile:
                myfile.write(tekst.format(**zmienne))
        else:
            print("Odrzucamy hipoteze zerową w teście t-Studenta. Wartość średnia nie jest naszą wartością oczekiwaną.")
            print("pvalue wyniosło",pvalts)
            tekst = """
            Symulacja dla parametrów n = {n}, p = {p:5.2f}
            Przyjmujemy hipoteze zerową w teście normalności Kołmogorowa-Smirnova. Rozkład jest normalny.
            pvalue wyniosło {pvalks}
            Odrzucamy hipoteze zerową w teście t-Studenta. Wartość średnia nie jest naszą wartością oczekiwaną.
            pvalue wyniosło {pvalts}
            Różnica pomiędzy średnią a wartością oczekiwaną wynosi {roz}
            """ 
            zmienne = {
             "n":n, 
             "p":p,
             "pvalks": pvalks,
             "pvalts" : pvalts,
             "roz" : abs(np.mean(sym)-wsp)
             } 
            with  open('symA.txt','a',encoding="utf-8") as myfile:
                myfile.write(tekst.format(**zmienne))
    else:
        print("Odrzucamy hipoteze zerową w teście normalności Kołmogorowa-Smirnova. Rozkład nie jest normalny.")
        print("pvalue wyniosło",pvalks)
        tekst = """
        Symulacja dla parametrów n = {n}, p = {p:5.2f}
        Odrzucamy hipoteze zerową w teście normalności Kołmogorowa-Smirnova. Rozkład nie jest normalny.
        pvalue wyniosło {pvalks}
        Różnica pomiędzy średnią a wartością oczekiwaną wynosi {roz}
        """ 
        zmienne = {
        "n":n, 
        "p":p,
        "pvalks": pvalks,
         "roz" : abs(np.mean(sym)-wsp)
            } 
        with  open('symA.txt','a',encoding="utf-8") as myfile:
            myfile.write(tekst.format(**zmienne))        
    print("")
    end = time.time()
    print("Symulacja wykonana w",end - start,"sekund")
    return sym


# SYMULACJE

il_pow=10000
n=[100,1000,10000,100000]
p=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
poz_uf=0.95

fig,axes = plt.subplots(len(n),len(p),figsize=(32,16))
for i in range(len(n)):
    for j in range(len(p)):
        sym = symulacjaA(il_pow,n[i],p[j])
        sns.distplot(sym,ax=axes[i,j]).set_title("n = "+str(n[i])+", p = " + str(p[j]))
plt.savefig("symA.png")
plt.show()




