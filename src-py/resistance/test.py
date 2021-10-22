def get_permutations(mission_size):
    permutations = []
    for p in range(2**mission_size):
        pb = "{0:b}".format(p).zfill(mission_size)
        permutations.append(pb)
    
    return permutations

def mission_fail_chance(mission, player_sus):
    p_fail = [0 for _ in range(len(mission) + 1)]
    permutations = get_permutations(len(mission))


    for p in permutations:
        probability = 1
        for i in range(len(p)):
            if p[i] == '1':
                probability *= (player_sus[mission[i]] * 0.6)      
            else:
                probability *= (player_sus[mission[i]] * (1 - 0.6) + (1 - player_sus[mission[i]])) 
        
        p_fail[p.count('1')] += probability

    return p_fail


mission = [2,4]
player_sus = [0.0, 1.0, 0.6875, 0.6875, 0.5]

def mission_fail_given_spy( mission, player_sus, player_index):
    p_fail = [0 for _ in range(len(mission) + 1)]
    permutations = get_permutations(len(mission))

    for p in permutations:
        probability = 1
        for i in range(len(p)):
            if i == player_index:
                if p[i] == '1':
                    probability *= 0.6
                else:
                    probability *= (1 - 0.6)
            else:
                if p[i] == '1':
                    probability *= (player_sus[mission[i]] * 0.6)
                else:
                    probability *= (player_sus[mission[i]] * (1 - 0.6) +  (1 - player_sus[mission[i]]))

        p_fail[p.count('1')] += probability
    
    return p_fail


print(mission_fail_chance(mission, player_sus))

n_fails = 1
pB = mission_fail_chance(mission, player_sus)[n_fails]

for i in range(len(mission)):
    pBA = mission_fail_given_spy(mission, player_sus, i)[n_fails]
    pA = player_sus[mission[i]]

    print((pBA * pA) / pB)

