from NurseScheduling import NurseScheduling
from kiiratasok import end_log, initialize_log
from multiprocessing import Process, Queue
import time


def run_process(q, nover, nap, max_it, alpha, beta, theta):
    n = NurseScheduling(nover, nap, alpha, beta, theta, max_it)
    n.annealing()
    q.put(n.get_s())
    return


def main():
    # === PARAMETEREK ===
    nover = 21
    nap = 14
    alpha = 1.15
    beta = 0.25
    theta = 0.28
    max_it = 10000
    process_count = 6
    # ===================

    outfile = initialize_log(nover, nap, max_it, alpha, beta, theta)

    p, q = [], []
    for i in range(process_count):
        queue_aux = Queue()
        q.append(queue_aux)
        p.append(Process(target=run_process, args=(queue_aux, nover, nap, max_it, alpha, beta, theta)))

    start = time.time()

    for i in p:
        i.start()

    results = []
    for i in q:
        results.append(i.get())

    for i in p:
        i.join()

    end = time.time()
    ido = end - start

    n = NurseScheduling(nover, nap, alpha, beta, theta, max_it)

    best_fitness = 0
    best_s = None
    for i in results:
        aux_fitness = n.fitness(i)
        if aux_fitness > best_fitness:
            best_fitness = aux_fitness
            best_s = i

    print('Performance: {}'.format(ido))
    outfile.write('Performance: {}'.format(ido))

    end_log(best_s, outfile)


if __name__ == '__main__':
    main()
