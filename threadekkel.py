from NurseScheduling import NurseScheduling
from kiiratasok import end_log, initialize_log
from threading import Thread
import time


def run_process(n):
    n.annealing()
    return


def main():
    # === PARAMETEREK ===
    nover = 30
    nap = 14
    alpha = 1.15
    beta = 0.25
    theta = 0.28
    max_it = 10000
    process_count = 7
    # ===================

    outfile = initialize_log(nover, nap, max_it, alpha, beta, theta)

    n, p = [], []
    for i in range(process_count):
        n_aux = NurseScheduling(nover, nap, alpha, beta, theta, max_it)
        n.append(n_aux)
        p.append(Thread(target=run_process, args=(n_aux,)))

    start = time.time()

    for i in p:
        i.start()

    for i in p:
        i.join()

    end = time.time()
    ido = end - start

    best_fitness = 0
    best_s = None
    for i in n:
        aux_fitness = i.fitness(i.get_s())
        if aux_fitness > best_fitness:
            best_fitness = aux_fitness
            best_s = i.get_s()

    print('Performance: {}'.format(ido))
    outfile.write('Performance: {}'.format(ido))

    end_log(best_s, outfile)


if __name__ == '__main__':
    main()
