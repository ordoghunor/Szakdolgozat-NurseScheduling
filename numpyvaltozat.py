import copy

import numpy as np
import random
from numpy import floor, ceil
from kiiratasok import initialize_log, end_log

def feltolt(nover, nap):
    s = np.zeros((nover, nap), dtype=int)
    return s


def megszamol_nullas(sor):
    nulla = 0
    for i in sor:
        if i == 0:
            nulla += 1
    return nulla


def ellenoriz_sor_eros_megszoritas(sor):
    elso = True
    for i in sor:
        if elso:
            elso = False
        else:
            if elozo == 3 and i == 1:
                return False
        elozo = i
    return True


def ne_legyen_ejjeli_utan_delelotti(s):
    # ellenorizzuk hogy ne legyen ejjeli valtas utan delelotti valtas
    # az egesz napra
    for i in s:
        elozo = -1
        for j in i:
            if elozo > 0:
                if j == 1 and elozo == 3:
                    return False
            elozo = j
    return True


def general(nover, nap):
    s = feltolt(nover, nap)
    szabadnap = nap / 3.5

    for i in range(nover):
        elosztva = (nap - szabadnap) / 3
        while True:
            for j in range(1, 4):
                e_aux = floor(elosztva)
                while e_aux > 0:
                    r = random.randint(0, nap - 1)
                    while s[i][r] != 0:
                        r = random.randint(0, nap - 1)
                    s[i][r] = j
                    e_aux -= 1
            maradt_sz_napok = megszamol_nullas(s[i])
            kiosztando_napok = maradt_sz_napok - szabadnap
            ejjeli_tura_aux = 3
            while floor(kiosztando_napok) != 0:
                munka_nap_adas = random.randint(1, 3)
                while munka_nap_adas == ejjeli_tura_aux:
                    munka_nap_adas = random.randint(1, 3)
                ejjeli_tura_aux = munka_nap_adas
                r = random.randint(0, nap - 1)
                while s[i][r] != 0:
                    r = random.randint(0, nap - 1)
                s[i][r] = munka_nap_adas
                kiosztando_napok -= 1.0
            if kiosztando_napok != floor(kiosztando_napok):
                r_uni = random.uniform(0, 1)
                if r_uni > kiosztando_napok:
                    munka_nap_adas = random.randint(1, 3)
                    while munka_nap_adas == ejjeli_tura_aux:
                        munka_nap_adas = random.randint(1, 3)
                    r = random.randint(0, nap - 1)
                    while s[i][r] != 0:
                        r = random.randint(0, nap - 1)
                    s[i][r] = munka_nap_adas

            if ellenoriz_sor_eros_megszoritas(s[i]):
                break
            else:
                for nulla_index in range(nap):
                    s[i][nulla_index] = 0
    return s


def valtoztat(s, nover, nap):
    nx = random.randint(0, nover - 1)
    n1 = random.randint(0, nap - 1)
    n2 = random.randint(0, nap - 1)
    while n2 == n1:
        n2 = random.randint(0, nap - 1)
    s[nx][n1], s[nx][n2] = s[nx][n2], s[nx][n1]
    return nx


def megszamol_szabadnover_per_nap(s, nover, nap):
    szabadok = np.zeros(nap, dtype=int)
    for i in range(nover):
        for j in range(nap):
            if s[i][j] == 0:
                szabadok[j] += 1
    return szabadok


def megszamol_napokra_munkasok(s, nover, nap):
    delelott = np.zeros(nap, dtype=int)
    delutan = np.zeros(nap, dtype=int)
    ejjel = np.zeros(nap, dtype=int)
    for i in range(nover):
        for j in range(nap):
            match s[i][j]:
                case 1:
                    delelott[j] += 1
                case 2:
                    delutan[j] += 1
                case 3:
                    ejjel[j] += 1
    return delelott, delutan, ejjel


def fitness(s, nover, nap, alpha=2, beta=1, theta=1, u_sor_cserelve=-1, consecutive=5):
    if u_sor_cserelve == -1 and not ne_legyen_ejjeli_utan_delelotti(s):
        return 0
    elif not ellenoriz_sor_eros_megszoritas(s[u_sor_cserelve]):
        return 0

    hiba = 1

    hiba_1 = 0                      # nezzuk hogy ha be van-e tartva a maximalis egymas utani napok dolgozasa
    for i in range(nover):                     # x-el iteraljuk a novereket
        streak, szabad = 0, 0
        streak_list = []
        for j in range(nap):                 # y-al iteraljuk a napokat
            if s[i][j] == 0:
                szabad += 1
                streak_list.append(streak)
                streak = 0
            else:
                streak += 1
        streak_list.append(streak)
        for k in streak_list:
            if k > consecutive:
                hiba_1 += k - consecutive
    hiba += hiba_1 * alpha

    hiba_2 = 0                       # nezzuk ha kb. minden nap ugyanannyi nover van szabad
    opt_sz_per_nap = nover / 3.5     # optimalisan ennyi szabadnapos nover kellene legyen 1 nap
    szabadok = megszamol_szabadnover_per_nap(s, nover, nap)
    also, felso = floor(opt_sz_per_nap), ceil(opt_sz_per_nap)
    for i in szabadok:
        if i != also and i != felso:
            hiba_2 += abs(opt_sz_per_nap - i)
    hiba += hiba_2 * beta

    hiba_3 = 0
    sz_p_nover = nap / 3.5          # ennyi szabadnapja kell legyen egy novernek (ezt kell megkozelitse)
    nvr_p_msz_p_n = nover / 3 * (1 - sz_p_nover / nap)  # ennyi nover kellene dolgozzon minden egyes muszakban(minden nap)
    muszak = megszamol_napokra_munkasok(s, nover, nap)
    for i in range(3):
        for j in range(nap):
            if muszak[i][j] != floor(nvr_p_msz_p_n) and muszak[i][j] != ceil(nvr_p_msz_p_n):
                hiba_3 += abs(nvr_p_msz_p_n - muszak[i][j])
    hiba += hiba_3 * theta

    return 1/hiba


def decrement_linearis(t, k):
    alfa = 0.5
    return t / (1 + alfa * k)


def annealing(nover, nap, max_ite, alpha=2, beta=1, theta=1, t=100000):
    k = 0

    s = general(nover, nap)
    legjobb = copy.deepcopy(s)
    legjobb_fitness = fitness(legjobb, nover, nap, alpha, beta, theta)
    line_counter, kiir_aux = 1, 0

    while k < max_ite:
        w = copy.deepcopy(s)
        unap = valtoztat(w, nover, nap)
        r = random.uniform(0, 1)

        sfitness = fitness(s, nover, nap, alpha, beta, theta, unap)
        wfitness = fitness(w, nover, nap, alpha, beta, theta, unap)
        if sfitness > 0 and wfitness > 0:
            ujra = 0
            aux = 0.01
            if t > 0.01:
                aux = np.emath.power(np.e, (sfitness - wfitness) / t)
            if wfitness > sfitness or r < aux:
                s = copy.deepcopy(w)
                ujra = 1
            if t > 0.001:
                t = decrement_linearis(t, k)
            if ujra == 1:
                sfitness = fitness(s, nover, nap, alpha, beta, theta, unap)
            if sfitness > legjobb_fitness:
                legjobb = copy.deepcopy(s)
                legjobb_fitness = sfitness
        k += 1
        if kiir_aux != legjobb_fitness:
            print(line_counter, '\t\t@', legjobb_fitness, '\t\t#', k)
            line_counter += 1
            kiir_aux = legjobb_fitness
    return legjobb


def main():
    nover = 27
    nap = 7
    alpha = 1
    beta = 0.25
    theta = 0.275
    max_ite = 500000

    outfile = initialize_log(nover, nap, max_ite, alpha, beta, theta)

    eredmeny = annealing(nover, nap, max_ite, alpha, beta, theta)

    end_log(eredmeny, outfile)


if __name__ == '__main__':
    main()
