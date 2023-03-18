from datetime import datetime


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


def initialize_log(nover, nap, max_ite, alpha, beta, theta):
    now = datetime.now()
    date_time = now.strftime("%m%d%Y_%H%M%S")
    filename = 'futtatasok/' + str(nover) + '_' + str(nap) + '_' + str(max_ite) + '_' + date_time + '.out'
    outfile = open(filename, "w")
    print('Nover Nap Alpha Beta  Theta   MaxIteration')
    print(
        ' {}    {}    {}  {}   {}     {}'.format(nover, nap, alpha, beta, theta, max_ite))
    print('=====================================================================')

    outfile.write('Nover Nap Alpha Beta Theta MaxIteration' + '\n')
    outfile.write(
        ' {}    {}    {}  {}   {}         {}'.format(nover, nap, alpha, beta, theta, max_ite) + '\n')
    outfile.write('=====================================================================' + '\n')
    return outfile


def kiszamol_napok_hanyan_dolgoznak(s):
    delelott = []
    delutan = []
    ejjel = []
    for _ in s[0]:
        delelott.append(0)
        delutan.append(0)
        ejjel.append(0)
    for i in s:
        for j in range(i.__len__()):
            match i[j]:
                case 1:
                    delelott[j] += 1
                case 2:
                    delutan[j] += 1
                case 3:
                    ejjel[j] += 1
    return delelott, delutan, ejjel


def end_log(t, outfile):
    print('=====================================================================')
    print('Napok szerint dolgoznak: (0-szabad, 1-delelott, 2-delutan, 3-ejjel)')
    for i in t:
        print(i)
    print('=====================================================================')
    szabadok_per_nap = kiszamol_szabad_per_nap(t)
    print('Szabad noverek per nap:')
    print(szabadok_per_nap)
    print('Szabad napok per nover:')
    print(kiszamol_szabad_per_nover(t))
    print('=====================================================================')
    delelott, delutan, ejjel = kiszamol_napok_hanyan_dolgoznak(t)
    print('Delelott dolgoznak:')
    print(delelott)
    print('Delutan dolgoznak:')
    print(delutan)
    print('Ejjel dolgoznak:')
    print(ejjel)
    print('=====================================================================')

    outfile.write('=====================================================================' + '\n')
    outfile.write('Napok szerint dolgoznak: (0-szabad, 1-delelott, 2-delutan, 3-ejjel)' + '\n')
    for i in t:
        outfile.write(str(i) + '\n')
    outfile.write('=====================================================================' + '\n')
    szabadok_per_nap = kiszamol_szabad_per_nap(t)
    outfile.write('Szabad noverek per nap:' + '\n')
    outfile.write(str(szabadok_per_nap) + '\n')
    outfile.write('Szabad napok per nover:' + '\n')
    outfile.write(str(kiszamol_szabad_per_nover(t)) + '\n')
    outfile.write('=====================================================================' + '\n')
    delelott, delutan, ejjel = kiszamol_napok_hanyan_dolgoznak(t)
    outfile.write('Delelott dolgoznak:' + '\n')
    outfile.write(str(delelott) + '\n')
    outfile.write('Delutan dolgoznak:' + '\n')
    outfile.write(str(delutan) + '\n')
    outfile.write('Ejjel dolgoznak:' + '\n')
    outfile.write(str(ejjel) + '\n')
    outfile.write('=====================================================================' + '\n')
