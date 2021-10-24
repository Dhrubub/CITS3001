from agent import Agent
import random


class VoteBot(Agent):        
    def __init__(self, name='BeliefBot'):
        '''
        Initialises the agent.
        Nothing to do here.
        '''
        self.name = name

    def new_game(self, number_of_players, player_number, spy_list):
        '''
        initialises the game, informing the agent of the 
        number_of_players, the player_number (an id number for the agent in the game),
        and a list of agent indexes which are the spies, if the agent is a spy, or empty otherwise
        '''
        self.m_size = self.mission_sizes[number_of_players]
        self.n_spy = self.spy_count[number_of_players]
        self.n_fails = self.fails_required[number_of_players]

        self.id = player_number
        self.spies = spy_list
        self.N = number_of_players
        self.n_res = self.N - self.n_spy

        self.player_sus = [self.n_spy / (self.N - 1) for _ in range(number_of_players)]
        self.player_sus[self.id] = 0

        self.M = 0
        self.R = 0

        self.successes = 0
        self.failures = 0

        self.spy = self.id in self.spies


        self.good_teams = set()
        self.bad_teams = set()

        self.PEN_THRESH = 0.9
        self.PENALTY = 0.05
        self.REWARD = -0.03
        self.SPY_THRESH = 0.7

        self.update_fail_rate()


    def propose_mission(self, team_size, betrayals_required = 1):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive) and number_of_players (exclusive)
        to be returned. 
        betrayals_required are the number of betrayals required for the mission to fail.

        selects the players with the least probability of being a spy
        ''' 
        team = []
        spy_count = 0
        if self.n_res == team_size:
            team.append(self.id)
            spy_count += 1

        spies_guess = self.get_spy_chance_order()
        if self.spy:
            counter = 0
            while spy_count < self.n_fails[self.M]:
                if not spies_guess[counter] in team and spies_guess[counter] in self.spies:
                    team.append(spies_guess[counter])
                    spy_count += 1
                counter += 1

        for i in spies_guess:
            if len(team) == team_size:
                break
            if not i in team:
                team.append(i)

        return team
  

    def vote(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.

        checklist to go through to determine if player should vote approve or reject
        '''

        if len(mission) == self.n_res and not self.id in mission:
            return False

        if self.spy:
            n_spies = 0
            for i in self.spies:
                if i in mission:
                    n_spies += 1
            if n_spies < self.n_fails[self.M]:
                return False 

        if self.is_team_bad(mission):
            return False

        if self.can_mission_fail(mission):
            return False

        if self.player_sus[proposer] >= self.SPY_THRESH:
            return False

        return True


    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        return random.random()<0.5
            
        

    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        By default, spies will betray 30% of the time. 

        a spy will betray according to its failrate
        '''
        if self.spy:
            if self.failures == 2:
                return True
            return random.random() < self.fail_rate

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It is not expected or required for this function to return anything.

        Applies bayes' theorem to update the probability of the players in the mission being a spy
        Updates the set of successful and unsuccessful teams
        '''
        current_sus = self.player_sus.copy()
        pB = self.mission_fail_chance(mission, current_sus, betrayals)
        if pB <= 0:
            pB = 0.5
        for i in range(len(mission)):
            pBA = self.mission_fail_given_spy(mission, current_sus, i, betrayals)
            pA = current_sus[mission[i]]

            pAB = (pBA * pA) / pB
            self.player_sus[mission[i]] = pAB

        self.update_teams(mission, mission_success)

 

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the numbe of missions (0-3) that have failed.

        updates game state variables
        '''
        self.M = rounds_complete
        self.failures = missions_failed
        self.successes = self.M - self.failures
    
    def game_outcome(self, spies_win, spies):
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail
        spies, a list of the player indexes for the spies.

        unused
        '''
        #nothing to do here
        pass

    def get_spy_chance_order(self):
        '''
        takes player_sus and returns a list which orders the player id's 
        from least probability of being spy to most probability
        '''
        return sorted(range(len(self.player_sus)), key=lambda k: self.player_sus[k])

    def get_permutations(self, mission_size, betrayals):
        '''
        returns the different permuations of mission outcomes for a given number of fails
        '''
        permutations = []
        for p in range(2**mission_size):
            pb = "{0:b}".format(p).zfill(mission_size)
            if pb.count('1') == betrayals:
                permutations.append(pb)
        
        return permutations

    def update_teams(self, mission, mission_success):
        '''
        stores the different combination of teams that have succeeded or failed
        '''
        good_teams_copy = self.good_teams.copy()
        if mission_success:
            if not tuple(sorted(mission)) in self.bad_teams:
                is_super = False
                for bt in self.bad_teams:
                    if set(mission).issuperset(set(bt)):
                        is_super = True
                if not is_super:
                    self.good_teams.add(tuple(sorted(mission)))
        else:
            for gt in good_teams_copy:
                if set(gt).issuperset(set(mission)) or set(gt) == set(mission):
                    self.good_teams.remove(gt)

            self.bad_teams.add(tuple(sorted(mission)))


    def update_fail_rate(self):
        '''
        update the spy fail rate variables
        '''
        mode = 2

        if self.M < 4:
            if mode == 0:
                self.fail_rate = 0.6

            elif mode == 1:
                self.fail_rate = (3-self.failures) / (5-self.M)

            elif mode == 2:
                self.fail_rate = (3-self.failures) / (5-self.M-1)
        
        if self.fail_rate <= 0:
            self.fail_rate = 0.5


    def mission_fail_chance(self, mission, player_sus, betrayals):
        '''
        calculates the probability of a mission failing with a specific number of fails
        '''
        p_fail = 0
        permutations = self.get_permutations(len(mission), betrayals)

        for p in permutations:
            probability = 1
            for i in range(len(p)):
                if p[i] == '1':
                    probability *= (player_sus[mission[i]] * self.fail_rate)      
                else:
                    probability *= (player_sus[mission[i]] * (1 - self.fail_rate) + (1 - player_sus[mission[i]])) 
            
            p_fail += probability

        return p_fail


    def mission_fail_given_spy(self, mission, player_sus, player_index, betrayals):
        '''
        calculates the probability of the mission failing 
        with a specific number of fails given player is a spy
        '''
        p_fail = 0
        permutations = self.get_permutations(len(mission), betrayals)

        for p in permutations:
            probability = 1
            for i in range(len(p)):
                if i == player_index:
                    if p[i] == '1':
                        probability *= self.fail_rate
                    else:
                        probability *= (1 - self.fail_rate)
                else:
                    if p[i] == '1':
                        probability *= (player_sus[mission[i]] * self.fail_rate)
                    else:
                        probability *= (player_sus[mission[i]] * (1 - self.fail_rate) +  (1 - player_sus[mission[i]]))

            p_fail += probability
        
        return p_fail

    def is_team_bad(self, mission):
        '''
        checks if the team has previously failed a mission
        '''
        if tuple(sorted(mission)) in self.bad_teams:
            return True

        for bt in self.bad_teams:
            if set(mission).issuperset(set(bt)):
                return True
        return False

    def is_team_good(self, mission):
        '''
        checks if the mission has only succeeded missions
        '''
        if tuple(sorted(mission)) in self.good_teams:
            return True

        for gt in self.good_teams:
            if set(mission).issuperset(set(gt)):
                return True
        return False 

    def can_mission_fail(self, mission):
        '''
        returns True if there are enough suspected spies to fail the mission
        '''
        spy_count = [i for i in mission if self.player_sus[i] >= self.SPY_THRESH]
        return len(spy_count) >= self.n_fails[self.M]







