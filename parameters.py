
# === PARAMETEREK ===
nover = 23          # number of nurses
nap = 14            # days to do the schedule
alpha = 1.15        # fitness parameter - consecutive dolgozas
beta = 0.25         # fitness parameter - szabadnap
theta = 0.28        # fitness parameter - egyenletes megkozelites minden muszakban
population_size = 10    # genetic_algorithm population size
max_it = 20000      # maximum iteration
mu_ = 3             # evo_strategy parameter
lambda_ = 10        # evo_strategy parameter
method = 3          # 1-annealing, 2-genetic, 3-hybridEvolution
sleep_rule = 2      # 1-after nightshift can come [2,3,0], 2-after nightshift can come only [3,0]
max_cons = 5        # soft constraint - max consecutive working days
# ===================
eloszlas = 1        # 1-egyenletes, 2-minden muszakra kulon
e_hetfo = 6, 5, 3   # [0] delelott, [1] delutan, [2] ejjel
e_kedd = 8, 6, 3    # [0] delelott, [1] delutan, [2] ejjel
e_szerda = 9, 7, 5  # [0] delelott, [1] delutan, [2] ejjel
e_csut = 8, 5, 4    # [0] delelott, [1] delutan, [2] ejjel
e_pentek = 8, 5, 3  # [0] delelott, [1] delutan, [2] ejjel
e_szomb = 8, 4, 5   # [0] delelott, [1] delutan, [2] ejjel
e_vasarn = 6, 5, 3  # [0] delelott, [1] delutan, [2] ejjel
e_hetre = e_hetfo, e_kedd, e_szerda, e_csut, e_pentek, e_szomb, e_vasarn
gamma = 0.12         # fitness par. - specialis eloszlas eseteben
