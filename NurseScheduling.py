
import copy
import numpy as np
import random
from numpy import floor, ceil


class NurseScheduling:
    _s = None

    def __init__(self, nurses, days, alpha, beta, theta, max_it):
        self.nurses = nurses
        self.days = days
        self.alpha = alpha
        self.beta = beta
        self.theta = theta
        self.max_it = max_it

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

    def _generate(self):
        self._s = np.zeros((self.nurses, self.days), dtype=int)
        szabadnap = self.days / 3.5
        ejjeli_tura_aux, hiba_kovetes = random.randint(1, 3), -1

        for i in range(self.nurses):
            elosztva = (self.days - szabadnap) / 3
            while True:
                hiba_kovetes = ejjeli_tura_aux
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
                # ejjeli_tura_aux = -1
                while floor(kiosztando_napok) != 0:
                    munka_nap_adas = 1 + ejjeli_tura_aux % 3
                    # munka_nap_adas = random.randint(1, 3)
                    # while munka_nap_adas == ejjeli_tura_aux:
                    #     munka_nap_adas = random.randint(1, 3)
                    ejjeli_tura_aux = munka_nap_adas
                    r = random.randint(0, self.days - 1)
                    while self._s[i][r] != 0:
                        r = random.randint(0, self.days - 1)
                    self._s[i][r] = munka_nap_adas
                    kiosztando_napok -= 1.0
                if kiosztando_napok != floor(kiosztando_napok):
                    r_uni = random.uniform(0, 1)
                    if r_uni > kiosztando_napok:
                        munka_nap_adas = random.randint(1, 3)
                        while munka_nap_adas == ejjeli_tura_aux:
                            munka_nap_adas = random.randint(1, 3)
                        r = random.randint(0, self.days - 1)
                        while self._s[i][r] != 0:
                            r = random.randint(0, self.days - 1)
                        self._s[i][r] = munka_nap_adas

                if self.ellenoriz_sor_eros_megszoritas(self._s, i):
                    break
                else:
                    ejjeli_tura_aux = hiba_kovetes
                    for nulla_index in range(self.days):
                        self._s[i][nulla_index] = 0

    def _modify(self, s):
        nx = random.randint(0, self.nurses - 1)
        n1 = random.randint(0, self.days - 1)
        n2 = random.randint(0, self.days - 1)
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

    def fitness(self, s, u_sor_cserelve=-1, consecutive=5):
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

        hiba_2 = 0  # nezzuk ha kb. minden nap ugyanannyi nover van szabad
        opt_sz_per_nap = self.nurses / 3.5  # optimalisan ennyi szabadnapos nover kellene legyen 1 nap
        szabadok = self.megszamol_szabadnover_per_nap(s)
        also, felso = floor(opt_sz_per_nap), ceil(opt_sz_per_nap)
        for i in szabadok:
            if i != also and i != felso:
                hiba_2 += abs(opt_sz_per_nap - i)
        hiba += hiba_2 * self.beta

        hiba_3 = 0
        sz_p_nover = self.days / 3.5  # ennyi szabadnapja kell legyen egy novernek (ezt kell megkozelitse)
        nvr_p_msz_p_n = self.nurses / 3 * (
                    1 - sz_p_nover / self.days)  # ennyi nover kellene dolgozzon minden egyes muszakban(minden nap)
        muszak = self.megszamol_napokra_munkasok(s)
        for i in range(3):
            for j in range(self.days):
                if muszak[i][j] != floor(nvr_p_msz_p_n) and muszak[i][j] != ceil(nvr_p_msz_p_n):
                    hiba_3 += abs(nvr_p_msz_p_n - muszak[i][j])
        hiba += hiba_3 * self.theta

        return 1 / hiba

    def decrement_linearis(self, t, k):
        alfa = 0.5
        return t / (1 + alfa * k)

    def annealing(self, t=100000):
        k = 0

        self._generate()
        legjobb = copy.deepcopy(self._s)
        legjobb_fitness = self.fitness(legjobb)
        line_counter, kiir_aux = 1, 0

        while k < self.max_it:
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
                    t = self.decrement_linearis(t, k)
                if sfitness > legjobb_fitness:
                    legjobb = copy.deepcopy(self._s)
                    legjobb_fitness = sfitness
            k += 1
            if kiir_aux != legjobb_fitness:
                # print(line_counter, '\t\t@', legjobb_fitness, '\t\t#', k)
                line_counter += 1
                kiir_aux = legjobb_fitness
        self._s = copy.deepcopy(legjobb)

    def kiertekel_megszoritasok(self, s, consecutive=5):
        hiba = 1

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

        hiba_2 = 0  # nezzuk ha kb. minden nap ugyanannyi nover van szabad
        opt_sz_per_nap = self.nurses / 3.5  # optimalisan ennyi szabadnapos nover kellene legyen 1 nap
        szabadok = self.megszamol_szabadnover_per_nap(s)
        also, felso = floor(opt_sz_per_nap), ceil(opt_sz_per_nap)
        for i in szabadok:
            if i != also and i != felso:
                hiba_2 += abs(opt_sz_per_nap - i)
        hiba += hiba_2 * self.beta

        hiba_3 = 0
        sz_p_nover = self.days / 3.5  # ennyi szabadnapja kell legyen egy novernek (ezt kell megkozelitse)
        nvr_p_msz_p_n = self.nurses / 3 * (
                1 - sz_p_nover / self.days)  # ennyi nover kellene dolgozzon minden egyes muszakban(minden nap)
        muszak = self.megszamol_napokra_munkasok(s)
        for i in range(3):
            for j in range(self.days):
                if muszak[i][j] != floor(nvr_p_msz_p_n) and muszak[i][j] != ceil(nvr_p_msz_p_n):
                    hiba_3 += abs(nvr_p_msz_p_n - muszak[i][j])
        hiba += hiba_3 * self.theta
        return hiba_1, hiba_2, hiba_3

    def get_s(self):
        return self._s
