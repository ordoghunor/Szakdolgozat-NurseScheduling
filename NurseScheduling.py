
import copy
import numpy as np
import random
from numpy import floor, ceil
from statistics import mean


def _check_gfit(gfit):
    for i in gfit:
        if i >= 1:
            return False
    return True


def decrement_linearis(t, k):
    alfa = 0.5
    return t / (1 + alfa * k)


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


def _szabadnap_hibak(s):
    hiba = 0
    sz = kiszamol_szabad_per_nover(s)
    kozep = mean(sz)
    k1 = floor(kozep)
    k2 = ceil(kozep)
    for i in sz:
        if i < k1 or i > k2:
            hiba += abs(kozep - i)
    return hiba


class NurseScheduling:
    _s = None

    def __init__(self, nurses, days, alpha, beta, theta, gamma, max_it, sleep_rule, eloszlas, e_hetre=None):
        self.nurses = nurses
        self.days = days
        self.alpha = alpha
        self.beta = beta
        self.theta = theta
        self.gamma = gamma
        self.max_it = max_it
        self.sleep_rule = sleep_rule
        self.eloszlas = eloszlas
        self.e_hetre = e_hetre

    def megszamol_nullas(self, sor):
        nulla = 0
        for i in range(self.days):
            if self._s[sor][i] == 0:
                nulla += 1
        return nulla

    def ellenoriz_sor_eros_megszoritas(self, s, sor):
        elso = True
        elozo = None
        for j in range(self.days):
            if elso:
                elso = False
            else:
                if elozo == 3 and s[sor][j] == 1:
                    return False
            elozo = s[sor][j]
        return True

    def _generate_uniform(self):
        self._s = np.zeros((self.nurses, self.days), dtype=int)
        szabadnap = self.days / 3.5
        elozo_munka_nap_adas, hiba_kovetes = random.randint(1, 3), -1

        for i in range(self.nurses):
            elosztva = (self.days - szabadnap) / 3
            while True:
                hiba_kovetes = elozo_munka_nap_adas
                for j in range(1, 4):
                    e_aux = floor(elosztva)
                    while e_aux > 0:
                        r = random.randint(0, self.days - 1)
                        while self._s[i][r] != 0:
                            r = random.randint(0, self.days - 1)
                        self._s[i][r] = j
                        e_aux -= 1
                maradt_sz_napok = self.megszamol_nullas(i)
                kiosztando_napok = maradt_sz_napok - szabadnap
                while floor(kiosztando_napok) != 0:
                    munka_nap_adas = 1 + elozo_munka_nap_adas % 3
                    elozo_munka_nap_adas = munka_nap_adas
                    r = random.randint(0, self.days - 1)
                    while self._s[i][r] != 0:
                        r = random.randint(0, self.days - 1)
                    self._s[i][r] = munka_nap_adas
                    kiosztando_napok -= 1.0
                if kiosztando_napok != floor(kiosztando_napok):
                    r_uni = random.uniform(0, 1)
                    if r_uni > kiosztando_napok:
                        munka_nap_adas = random.randint(1, 3)
                        while munka_nap_adas == elozo_munka_nap_adas:
                            munka_nap_adas = random.randint(1, 3)
                        r = random.randint(0, self.days - 1)
                        while self._s[i][r] != 0:
                            r = random.randint(0, self.days - 1)
                        self._s[i][r] = munka_nap_adas

                if self.ellenoriz_sor_eros_megszoritas(self._s, i):
                    break
                else:
                    elozo_munka_nap_adas = hiba_kovetes
                    for nulla_index in range(self.days):
                        self._s[i][nulla_index] = 0

    def _generate_as_expected(self):
        while True:
            self._s = np.zeros((self.nurses, self.days), dtype=int)
            for i in range(7):
                for j in range(3):
                    aux = self.e_hetre[i][j]
                    while aux > 0:
                        megvan = 0
                        while megvan == 0:
                            r = random.randint(0, self.nurses-1)
                            ii = i
                            while ii < self.days:
                                if self._s[r][ii] == 0:
                                    self._s[r][ii] = j + 1
                                    if not self.ellenoriz_sor_eros_megszoritas(self._s, r):
                                        self._s[r][ii] = 0
                                    else:
                                        megvan = 1
                                ii += 7
                        aux -= 1
            if self.ne_legyen_ejjeli_utan_delelotti(self._s):
                break

    def _generate(self):
        if self.eloszlas == 1:
            self._generate_uniform()
        elif self.eloszlas == 2:
            self._generate_as_expected()

    def _modify(self, s):
        # swap 2 random
        if self.eloszlas == 2 and random.uniform(0, 1) < 0.1:
            nx: int = random.randint(0, self.days - 1)
            n1: int = random.randint(0, self.nurses - 1)
            n2: int = random.randint(0, self.nurses - 1)
            while n1 == n2:
                n2 = random.randint(0, self.nurses - 1)
            s[n1][nx], s[n2][nx] = s[n2][nx], s[n1][nx]
            return n1
        else:
            nx: int = random.randint(0, self.nurses - 1)
            n1: int = random.randint(0, self.days - 1)
            n2: int = random.randint(0, self.days - 1)
            while n2 == n1:
                n2 = random.randint(0, self.days - 1)
            s[nx][n1], s[nx][n2] = s[nx][n2], s[nx][n1]
            return nx

    def ne_legyen_ejjeli_utan_delelotti(self, s):
        for i in range(self.nurses):
            elozo = -1
            for j in range(self.days):
                if elozo > 0:
                    if s[i][j] == 1 and elozo == 3:
                        return False
                elozo = s[i][j]
        return True

    def megszamol_szabadnover_per_nap(self, s):
        szabadok = np.zeros(self.days, dtype=int)
        for i in range(self.nurses):
            for j in range(self.days):
                if s[i][j] == 0:
                    szabadok[j] += 1
        return szabadok

    def megszamol_napokra_munkasok(self, s):
        delelott = np.zeros(self.days, dtype=int)
        delutan = np.zeros(self.days, dtype=int)
        ejjel = np.zeros(self.days, dtype=int)
        for i in range(self.nurses):
            for j in range(self.days):
                match s[i][j]:
                    case 1:
                        delelott[j] += 1
                    case 2:
                        delutan[j] += 1
                    case 3:
                        ejjel[j] += 1
        return delelott, delutan, ejjel

    def sleep_rule_check(self, s):
        before = None
        hiba = 0
        for i in range(self.nurses):
            for j in range(self.days):
                if j == 0:
                    before = s[i][j]
                else:
                    if before == 3 and s[i][j] == 2:
                        hiba += 1
                    before = s[i][j]
        return hiba

    def hetre_eloszlas(self, s):
        hiba = 0
        hetre_aktualis = np.zeros((self.days, 3), dtype=int)
        for j in range(self.days):
            for i in range(self.nurses):
                if s[i][j] > 0:
                    hetre_aktualis[j][s[i][j] - 1] += 1
        for i in range(self.days):
            for j in range(3):
                hiba += abs(self.e_hetre[i % 7][j] - hetre_aktualis[i][j])
        return hiba

    def fitness(self, s, u_sor_cserelve=-1, consecutive=5, kiertekel=False):
        hiba = 1
        if u_sor_cserelve == -1 and not self.ne_legyen_ejjeli_utan_delelotti(s):
            hiba += 100
        elif not self.ellenoriz_sor_eros_megszoritas(s, u_sor_cserelve):
            hiba += 100

        hiba_1 = 0  # nezzuk hogy ha be van-e tartva a maximalis egymas utani napok dolgozasa
        for i in range(self.nurses):  # x-el iteraljuk a novereket
            streak, szabad = 0, 0
            streak_list = []
            for j in range(self.days):  # y-al iteraljuk a napokat
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
        hiba += hiba_1 * self.alpha

        hiba_2 = 0
        if self.eloszlas == 1:
            opt_sz_per_nap = self.nurses / 3.5  # optimalisan ennyi szabadnapos nover kellene legyen 1 nap
            szabadok = self.megszamol_szabadnover_per_nap(s)  # nezzuk ha kb. minden nap ugyanannyi nover van szabad
            also, felso = floor(opt_sz_per_nap), ceil(opt_sz_per_nap)
            for i in szabadok:
                if i != also and i != felso:
                    hiba_2 += abs(opt_sz_per_nap - i)
        elif self.eloszlas == 2:
            hiba_2 += _szabadnap_hibak(s)
        hiba += hiba_2 * self.beta

        hiba_3 = 0
        if self.eloszlas == 1:
            sz_p_nover = self.days / 3.5  # ennyi szabadnapja kell legyen egy novernek (ezt kell megkozelitse)
            nvr_p_msz_p_n = self.nurses / 3 * (
                        1 - sz_p_nover / self.days)  # ennyi nover kellene dolgozzon minden egyes muszakban(minden nap)
            muszak = self.megszamol_napokra_munkasok(s)
            for i in range(3):
                for j in range(self.days):
                    if muszak[i][j] != floor(nvr_p_msz_p_n) and muszak[i][j] != ceil(nvr_p_msz_p_n):
                        hiba_3 += abs(nvr_p_msz_p_n - muszak[i][j])
            hiba += hiba_3 * self.theta
        elif self.eloszlas == 2:
            hiba_3 += self.hetre_eloszlas(s)
        hiba += hiba_3 * self.gamma

        hiba_4 = 0
        if self.sleep_rule == 2:
            hiba_4 = self.sleep_rule_check(s)
            hiba += hiba_4

        if kiertekel:
            return hiba_1, hiba_2, hiba_3, hiba_4
        else:
            return 1 / hiba

    def annealing(self, t=100000):
        k = 0

        self._generate()
        legjobb = copy.deepcopy(self._s)
        legjobb_fitness = self.fitness(legjobb)
        line_counter, kiir_aux = 1, 0

        while k < self.max_it and legjobb_fitness < 1:
            w = copy.deepcopy(self._s)
            unap = self._modify(w)
            r = random.uniform(0, 1)

            sfitness = self.fitness(self._s, u_sor_cserelve=unap)
            wfitness = self.fitness(w, u_sor_cserelve=unap)
            if sfitness > 0 and wfitness > 0:
                aux = 0.001
                if t > aux:
                    aux = np.emath.power(np.e, (sfitness - wfitness) / t)
                if wfitness > sfitness or r < aux:
                    self._s = copy.deepcopy(w)
                    sfitness = wfitness
                if t > 0.001:
                    t = decrement_linearis(t, k)
                if sfitness > legjobb_fitness:
                    legjobb = copy.deepcopy(self._s)
                    legjobb_fitness = sfitness
            k += 1
            if kiir_aux != legjobb_fitness:
                # print(line_counter, '\t\t@', legjobb_fitness, '\t\t#', k)
                line_counter += 1
                kiir_aux = legjobb_fitness
        self._s = copy.deepcopy(legjobb)

    def _init_genetic_populations(self, population_size):
        g = np.zeros((population_size, self.nurses, self.days), dtype=int)
        for i in range(population_size):
            self._generate()
            g[i] = self.get_s()
        return g

    def _cross_ga(self, p1, p2):
        child = np.zeros((self.nurses, self.days), dtype=int)
        for i in range(self.nurses):
            r = random.uniform(0, 1)
            if r < 0.5:
                child[i] = p1[i]
            else:
                child[i] = p2[i]
        return child

    def genetic(self, population_size=20, mutation=0.2, cross=0.9):
        g = self._init_genetic_populations(population_size)

        gfit = np.zeros(population_size)
        for i in range(population_size):
            gfit[i] = self.fitness(g[i])

        k = 0
        while k < self.max_it:
            new_population = np.zeros((population_size, self.nurses, self.days), dtype=int)
            max1, max2 = (-1, 0.0), (-1, 0.0)   # select 2 best chromosomes
            for i in range(population_size):
                if gfit[i] > max1[1]:
                    max2 = max1
                    max1 = i, gfit[i]
                elif gfit[i] > max2[1]:
                    max2 = i, gfit[i]
            new_population[0], gfit[0] = g[max1[0]], gfit[max1[0]]  # 2 best chromosomes are injected into the new pop.
            new_population[1], gfit[1] = g[max2[0]], gfit[max2[0]]
            for i in range(population_size - 2):
                ii = i + 2
                r = random.uniform(0, 1)
                if r < mutation:
                    u_sor = self._modify(g[ii])
                    new_population[ii], gfit[ii] = g[ii], self.fitness(g[ii], u_sor)
                elif r < cross:
                    new_population[ii] = self._cross_ga(new_population[0], new_population[1])
                    gfit[ii] = self.fitness(new_population[ii])
                else:
                    self._generate()
                    new_population[ii] = self.get_s()
                    gfit[ii] = self.fitness(new_population[ii])
                g = copy.deepcopy(new_population)
            k = k + 1
        maxi = (-1, 0.0)
        for i in range(population_size):
            if gfit[i] > maxi[1]:
                maxi = i, gfit[i]
        return g[maxi[0]]

    def _init_evo_strategy(self, _mu, _lambda):
        g = np.zeros((_mu + _lambda, self.nurses, self.days), dtype=int)
        gfit = np.zeros(_mu + _lambda)
        for i in range(_mu):
            self._generate()
            g[i] = self.get_s()
            gfit[i] = self.fitness(g[i])
        return g, gfit

    def _qsort_best_evo_strategy(self, bal, jobb, g, gfit):
        k = bal + random.randint(0, 999999) % (jobb - bal + 1)
        i = bal
        j = jobb
        while True:
            while gfit[i] > gfit[k]:
                i += 1
            while gfit[j] < gfit[k]:
                j -= 1
            if i <= j:
                gfit[i], gfit[j] = gfit[j], gfit[i]
                g[i], g[j] = g[j], g[i]
                i += 1
                j -= 1
            if i > j:
                break
        if i < jobb:
            self._qsort_best_evo_strategy(i, jobb, g, gfit)
        if j > bal:
            self._qsort_best_evo_strategy(bal, j, g, gfit)

    def evo_strategy(self, _mu, _lambda):
        g, gfit = self._init_evo_strategy(_mu, _lambda)

        k = 0
        while k < self.max_it and _check_gfit(gfit):
            for i in range(_lambda):
                aux = copy.deepcopy(g[i % _mu])
                u_sor = self._modify(aux)
                g[i + _mu] = aux
                if self.eloszlas == 1:
                    gfit[i + _mu] = self.fitness(aux, u_sor_cserelve=u_sor)
                elif self.eloszlas == 2:
                    gfit[i + _mu] = self.fitness(aux)
            self._qsort_best_evo_strategy(0, _mu + _lambda - 1, g, gfit)
            k += 1
        self._s = g[0]

    def get_s(self):
        return self._s
