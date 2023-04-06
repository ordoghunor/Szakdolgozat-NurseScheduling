from NurseScheduling import NurseScheduling
from kiiratasok import end_log, initialize_log
from parameters import *
import timeit


def main():
    outfile = initialize_log(nover, nap, max_it, alpha, beta, theta)

    n = NurseScheduling(nover, nap, alpha, beta, theta, max_it)
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

    (h1, h2, h3) = n.kiertekel_megszoritasok(n.get_s())
    print('h1 = ', h1)
    print('h2 = ', h2)
    print('h3 = ', h3)


if __name__ == '__main__':
    main()
