
# === PARAMETEREK ===
nover = 100          # number of nurses
nap = 28            # days to do the schedule
alpha = 1.15        # fitness parameter - consecutive dolgozas
beta = 0.25         # fitness parameter - szabadnap
theta = 0.28        # fitness parameter - egyenletes megkozelites minden muszakban
population_size = 10    # genetic_algorithm population size
max_it = 50000      # maximum iteration
mu_ = 3             # memetic parameter
lambda_ = 10        # memetic parameter
method = 1          # 1-annealing, 2-genetic, 3-memetic
sleep_rule = 2      # 1-after nightshift can come [2,3,0], 2-after nightshift can come only [3,0]
max_cons = 5        # soft constraint - max consecutive working days
mutation = 0.5      # mutation probability in ga
crossover = 0.5     # crossover probability in ga
process_count = 4   # number of parallel processen in simulated annealing
t0 = 50000         # intial temperature simulated annealing
zeta = 1            # sleep rule strenght
# ===================
eloszlas = 1        # 1-egyenletes, 2-minden muszakra kulon
e_hetfo = 13, 9, 8   # [0] delelott, [1] delutan, [2] ejjel
e_kedd = 12, 10, 8    # [0] delelott, [1] delutan, [2] ejjel
e_szerda = 13, 10, 8  # [0] delelott, [1] delutan, [2] ejjel
e_csut = 11, 11, 9    # [0] delelott, [1] delutan, [2] ejjel
e_pentek = 11, 13, 14  # [0] delelott, [1] delutan, [2] ejjel
e_szomb = 11, 13, 14   # [0] delelott, [1] delutan, [2] ejjel
e_vasarn = 11, 11, 8  # [0] delelott, [1] delutan, [2] ejjel
e_hetre = e_hetfo, e_kedd, e_szerda, e_csut, e_pentek, e_szomb, e_vasarn
gamma = 0.12         # fitness par. - specialis eloszlas eseteben
oszlop_csere = 0.1
