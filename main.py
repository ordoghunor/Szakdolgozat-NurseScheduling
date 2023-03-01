# Szakdolgozat
# Nover beosztasi problema - Nurse Scheduling Problem/Nurse rostering problem
# Ordog Hunor - ohim2065


import copy
import random
import math

from numpy import floor, ceil
from datetime import datetime

logfile = open("output.txt", "w")

# ============== Szimulalt lehutes ===================

def feltolt_s(nover, nap):
    s = []
    for i in range(nover):
        ss = []
        for j in range(nap):
            ss.append(0)
        s.append(ss)
    return s


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


def megszamol_nullas(sor):
    nulla = 0
    for i in sor:
        if i == 0:
            nulla += 1
    return nulla


def general_neo(nover, nap):
    s = feltolt_s(nover, nap)
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


def valtoztat_neo(s, switch):
    new_s = copy.deepcopy(s)

    for _ in range(switch):
        nover_index = random.randint(0, new_s.__len__()-1)

        nap1_index = random.randint(0, new_s[nover_index].__len__() - 1)
        nap2_index = random.randint(0, new_s[nover_index].__len__() - 1)
        while nap2_index == nap1_index:
            nap2_index = random.randint(0, new_s[nover_index].__len__() - 1)

        aux = new_s[nover_index][nap1_index]
        new_s[nover_index][nap1_index] = new_s[nover_index][nap2_index]
        new_s[nover_index][nap2_index] = aux

    return new_s


def decrement_linearis(t0, k):
    alpha = 0.5
    return t0 / (1 + alpha * k)


def ne_legyen_ejjeli_utan_delelotti(s):
    # ellenorizzuk hogy ne legyen ejjeli valtas utan delelotti valtas
    for i in s:
        elozo = -1
        for j in i:
            if elozo > 0:
                if j == 1 and elozo == 3:
                    return False
            elozo = j
    return True


def pontozas(x):
    return max(x, 0)


def minoseg_neo(s, alpha, beta, theta, consecutive):
    if not ne_legyen_ejjeli_utan_delelotti(s):
        return 0
    hibak = 0

    logger = []

    hiba_alpha = 0
    for nover in s:
        streak = 0
        szabad = 0
        streak_list = []
        for nap in nover:
            if nap != 0:
                streak += 1
            else:
                szabad += 1
                streak_list.append(streak)
                streak = 0
        streak_list.append(streak)
        for i in streak_list:
            if i > consecutive:
                hiba_alpha += i - consecutive
    hibak += hiba_alpha * alpha

    logger.append(hiba_alpha)

    hiba_beta = 0
    noverek = s.__len__()
    szabadnap_per_nap_optimum = noverek / 3.5
    szabadok_per_nap = kiszamol_szabad_per_nap(s)
    for i in szabadok_per_nap:
        if i != floor(szabadnap_per_nap_optimum) and i != ceil(szabadnap_per_nap_optimum):
            hiba_beta += abs(szabadnap_per_nap_optimum - i)
    hibak += hiba_beta * beta

    logger.append(hiba_beta)

    hiba_theta = 0
    napok = s[0].__len__()
    szabadnap_per_nover = napok / 3.5
    ennyi_kell_dolgozzon_minden_muszakban_naponta = noverek / 3 * (1 - szabadnap_per_nover / napok)
    muszakok = kiszamol_napok_hanyan_dolgoznak(s)
    for muszak in muszakok:
        for nap in muszak:
            if nap != floor(ennyi_kell_dolgozzon_minden_muszakban_naponta) and nap != ceil(ennyi_kell_dolgozzon_minden_muszakban_naponta):
                hiba_theta += abs(ennyi_kell_dolgozzon_minden_muszakban_naponta - nap)

    hibak += hiba_theta * theta

    logger.append(hiba_theta)

    logfile.write(str(logger) + '\n')

    if hibak == 0:
        hibak = 1
    return 1 / hibak


def kiszamol_szabad_per_nover(s):
    szabad = []
    for _ in s:
        szabad.append(0)
    for i in range(s.__len__()):
        for j in s[i]:
            if j == 0:
                szabad[i] += 1
    return szabad


def kiszamol_szabad_per_nap(s):
    szabadok_per_nap = []
    for _ in s[0]:
        szabadok_per_nap.append(0)
    for i in s:
        for j in range(i.__len__()):
            if i[j] == 0:
                szabadok_per_nap[j] += 1
    return szabadok_per_nap


def histogram(S, j):
    delelott = 0
    delutan = 0
    ejjel = 0
    szabad = 0
    for i in S:
        match i[j]:
            case 0:
                szabad += 1
            case 1:
                delelott += 1
            case 2:
                delutan += 1
            case 3:
                ejjel += 1
    return szabad, delelott, delutan, ejjel


def kiszamol_napok_hanyan_dolgoznak(s):
    delelott = []
    delutan = []
    ejjel = []
    for _ in s[0]:
        delelott.append(0)
        delutan.append(0)
        ejjel.append(0)
    for i in s:
        for j in range(i.__len__()):
            match i[j]:
                case 1:
                    delelott[j] += 1
                case 2:
                    delutan[j] += 1
                case 3:
                    ejjel[j] += 1
    return delelott, delutan, ejjel


def annealing(nover, nap, max_iteration, alpha, beta, theta, switch, consecutive, fitness, outfile):
    k = 0
    T0 = 100000
    kiir_aux = 0
    min_legjobb = 0
    line_counter = 1

    t = copy.deepcopy(T0)
    S = general_neo(nover, nap)
    Legjobb = S

    print('Kezdeti fitness:', fitness(S, alpha, beta, theta, consecutive))
    outfile.write('Kezdeti fitness: ' + str(fitness(S, alpha, beta, theta, consecutive)) + '\n')

    while t > 0 and k < max_iteration:
        Ss = S
        W = valtoztat_neo(Ss, switch)
        r = random.uniform(0, 1)

        sss = fitness(S, alpha, beta, theta, consecutive)
        www = fitness(W, alpha, beta, theta, consecutive)
        if sss > 0 and www > 0:
            aux = math.e ** ((sss - www) / t)
            if www > sss or r < aux:
                S = copy.deepcopy(W)
            t = decrement_linearis(T0, k)
            m_s_aux = fitness(S, alpha, beta, theta, consecutive)
            if m_s_aux > fitness(Legjobb, alpha, beta, theta, consecutive):
                Legjobb = copy.deepcopy(S)
                min_legjobb = m_s_aux
        k += 1
        if kiir_aux != min_legjobb:
            print(line_counter, '\t\t@', min_legjobb, '\t\t#', k)
            outfile.write(str(line_counter) + '\t\t@' + str(min_legjobb) + '\t\t#' + str(k) + '\n')
            line_counter += 1
            kiir_aux = min_legjobb
    return Legjobb

# ====================================================


def hegymaszo(nover, nap, max_iteration, alpha, beta, theta, switch, consecutive, fitness, outfile):
    s = general_neo(nover, nap)
    legjobb = copy.deepcopy(s)
    minoseg_legjobb = fitness(legjobb, alpha, beta, theta, consecutive)

    outfile.write('Kedeti fitness: ' + str(minoseg_legjobb) + '\n')
    line_counter = 1

    for k in range(max_iteration):
        new_s = valtoztat_neo(s, switch)
        minoseg_new_s = fitness(new_s, alpha, beta, theta, consecutive)
        if minoseg_legjobb < minoseg_new_s:
            legjobb = copy.deepcopy(new_s)
            s = copy.deepcopy(new_s)
            minoseg_legjobb = minoseg_new_s
            outfile.write(str(line_counter) + '\t\t@' + str(minoseg_legjobb) + '\t\t#' + str(k) + '\n')
            line_counter += 1

    return legjobb


# ====================================================

def main():
    nover = 15
    nap = 7
    consecutive = 5  # dokumentacioban x-nek van emlitve
    alpha = 0.15     # egymas utani munkanapok betartasa
    beta = 0.14      # minden nap ugyanannyi munkas legyen szabad
    theta = 0.18     # minden muszakban kb ugyanannyian dolgozzanak
    max_iteration = 250000
    csere_per_valtoztatas = 2
    fitness = minoseg_neo

    now = datetime.now()
    # subfolder = 'szimulalt_lehutes/'
    # subfolder = 'hegymaszo/'
    date_time = now.strftime("%m%d%Y_%H%M%S")
    filename = 'futtatasok/' + str(nover) + '_' + str(nap) + '_' + str(max_iteration) + '_' + date_time + '.out'
    outfile = open(filename, "w")

    print('Nover Nap Alpha Beta Theta Switch Consecutive MaxIteration')
    print(' {}    {}    {}  {}   {}    {}     {}        {}'.format(nover,nap,alpha,beta,theta,csere_per_valtoztatas,consecutive,max_iteration))
    print('=====================================================================')

    outfile.write('Nover Nap Alpha Beta Theta Switch Consecutive MaxIteration' + '\n')
    outfile.write(
        ' {}    {}    {}  {}   {}    {}     {}        {}'.format(nover, nap, alpha, beta, theta, csere_per_valtoztatas,
                                                                 consecutive, max_iteration) + '\n')
    outfile.write('=====================================================================' + '\n')

    T = annealing(nover, nap, max_iteration, alpha, beta, theta, csere_per_valtoztatas, consecutive, fitness, outfile)
    # T = hegymaszo(nover, nap, max_iteration, alpha, beta, theta, csere_per_valtoztatas, consecutive, fitness, outfile)

    print('=====================================================================')
    print('Napok szerint dolgoznak: (0-szabad, 1-delelott, 2-delutan, 3-ejjel)')
    for i in T:
        print(i)
    print('=====================================================================')
    szabadok_per_nap = kiszamol_szabad_per_nap(T)
    print('Szabad noverek per nap:')
    print(szabadok_per_nap)
    print('Szabad napok per nover:')
    print(kiszamol_szabad_per_nover(T))
    print('=====================================================================')
    delelott, delutan, ejjel = kiszamol_napok_hanyan_dolgoznak(T)
    print('Delelott dolgoznak:')
    print(delelott)
    print('Delutan dolgoznak:')
    print(delutan)
    print('Ejjel dolgoznak:')
    print(ejjel)
    print('=====================================================================')

    outfile.write('=====================================================================' + '\n')
    outfile.write('Napok szerint dolgoznak: (0-szabad, 1-delelott, 2-delutan, 3-ejjel)' + '\n')
    for i in T:
        outfile.write(str(i) + '\n')
    outfile.write('=====================================================================' + '\n')
    szabadok_per_nap = kiszamol_szabad_per_nap(T)
    outfile.write('Szabad noverek per nap:' + '\n')
    outfile.write(str(szabadok_per_nap) + '\n')
    outfile.write('Szabad napok per nover:' + '\n')
    outfile.write(str(kiszamol_szabad_per_nover(T)) + '\n')
    outfile.write('=====================================================================' + '\n')
    delelott, delutan, ejjel = kiszamol_napok_hanyan_dolgoznak(T)
    outfile.write('Delelott dolgoznak:' + '\n')
    outfile.write(str(delelott) + '\n')
    outfile.write('Delutan dolgoznak:' + '\n')
    outfile.write(str(delutan) + '\n')
    outfile.write('Ejjel dolgoznak:' + '\n')
    outfile.write(str(ejjel) + '\n')
    outfile.write('=====================================================================' + '\n')


if __name__ == '__main__':
    main()
