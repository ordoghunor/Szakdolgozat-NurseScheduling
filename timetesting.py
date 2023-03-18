import timeit
from NurseScheduling import NurseScheduling

def test_1(n):
    n.annealing()


def main():
    nover = 30
    nap = 7
    alpha = 1
    beta = 0.25
    theta = 0.28
    max_it = 1000000

    n = NurseScheduling(nover, nap, alpha, beta, theta, max_it)

    print(timeit.timeit(lambda: test_1(n), number=1))


if __name__ == '__main__':
    main()
