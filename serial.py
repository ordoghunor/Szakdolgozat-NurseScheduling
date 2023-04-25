from NurseScheduling import NurseScheduling
from kiiratasok import end_log, initialize_log
from parameters import *
import timeit


def main():
    outfile = initialize_log(nover, nap, max_it, alpha, beta, theta, mu_, lambda_, method, eloszlas, gamma)

    n = NurseScheduling(nover, nap, alpha, beta, theta, gamma, max_it, sleep_rule, eloszlas, e_hetre)
    ido = None
    if method == 1:
        ido = timeit.timeit(lambda: n.annealing(), number=1)
    elif method == 2:
        ido = timeit.timeit(lambda: n.genetic(population_size), number=1)
    elif method == 3:
        ido = timeit.timeit(lambda: n.evo_strategy(mu_, lambda_), number=1)

    end_log(n.get_s(), outfile)
    print('Performance: {}'.format(ido))
    outfile.write('Performance: {}'.format(ido))
    print('fitness: {}'.format(n.fitness(n.get_s())))

    h1, h2, h3, h4 = n.fitness(n.get_s(), kiertekel=True)
    print('h1 = ', h1)
    print('h2 = ', h2)
    print('h3 = ', h3)
    print('h3 = ', h4)


if __name__ == '__main__':
    main()
