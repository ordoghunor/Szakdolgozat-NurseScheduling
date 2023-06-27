from NurseScheduling import NurseScheduling
from kiiratasok import end_log, initialize_log
from multiprocessing import Process, Queue
from parameters import *
import time


def run_process(q):
    n = NurseScheduling(nover, nap, alpha, beta, theta, gamma, max_it, sleep_rule, eloszlas, max_cons, zeta, oszlop_csere, e_hetre)
    n.annealing(t0)
    q.put(n)
    return


def main():

    outfile = initialize_log()

    queue = Queue()
    p = []
    for i in range(process_count):
        p.append(Process(target=run_process, args=(queue,)))

    start = time.time()

    for i in p:
        i.start()

    res = queue.get()
    queue.close()

    for i in p:
        if i.is_alive():
            i.terminate()

    end = time.time()
    ido = end - start

    fitnes = res.fitness(res.get_s())
    h1, h2, h3, h4 = res.fitness(res.get_s(), kiertekel=True)

    end_log(res.get_s(), outfile)
    print('Performance: {}'.format(ido))
    print('Fitness: {}'.format(fitnes))
    outfile.write('Performance: {}'.format(ido))

    print('h1 = ', h1)
    print('h2 = ', h2)
    print('h3 = ', h3)
    print('h3 = ', h4)


if __name__ == '__main__':
    main()
