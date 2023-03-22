from NurseScheduling import NurseScheduling
from kiiratasok import end_log, initialize_log
import timeit


def main():
    # === PARAMETEREK ===
    nover = 30
    nap = 14
    alpha = 1.15
    beta = 0.25
    theta = 0.28
    max_it = 10000
    # ===================

    outfile = initialize_log(nover, nap, max_it, alpha, beta, theta)

    n = NurseScheduling(nover, nap, alpha, beta, theta, max_it)
    ido = timeit.timeit(lambda: n.annealing(), number=1)

    end_log(n.get_s(), outfile)
    print('Performance: {}'.format(ido))
    outfile.write('Performance: {}'.format(ido))

    (h1, h2, h3) = n.kiertekel_megszoritasok(n.get_s())
    print('h1 = ', h1)
    print('h2 = ', h2)
    print('h3 = ', h3)


if __name__ == '__main__':
    main()
