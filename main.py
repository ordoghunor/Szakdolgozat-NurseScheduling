from NurseScheduling import NurseScheduling
from kiiratasok import end_log, initialize_log
import timeit


def main():
    nover = 30
    nap = 7
    alpha = 1
    beta = 0.25
    theta = 0.28
    max_it = 1000000

    outfile = initialize_log(nover, nap, max_it, alpha, beta, theta)

    n = NurseScheduling(nover, nap, alpha, beta, theta, max_it)
    ido = timeit.timeit(lambda: n.annealing(), number=1)

    end_log(n.get_s(), outfile)
    print('Performance: {}'.format(ido))
    outfile.write('Performance: {}'.format(ido))


if __name__ == '__main__':
    main()