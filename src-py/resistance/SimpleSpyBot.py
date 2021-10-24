from agent import Agent
import random

class SimpleSpyBot(Agent):        
    '''A sample implementation of a random agent in the game The Resistance'''

    def __init__(self, name='Rando'):
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

        self.M = 0
        self.R = 0

        self.successes = 0
        self.failures = 0

        self.spy = self.id in self.spies

        self.update_fail_rate()


    def is_spy(self):
        '''
        returns True iff the agent is a spy
        '''
        return self.player_number in self.spy_list

    def propose_mission(self, team_size, betrayals_required = 1):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive) and number_of_players (exclusive)
        to be returned. 
        betrayals_required are the number of betrayals required for the mission to fail.
        '''
        team = []
        spy_count = 0
        if self.n_res == team_size:
            team.append(self.id)
            spy_count += 1

        if self.spy:
            while spy_count < self.n_fails[self.M]:
                new_player = random.choice(self.spies)
                if not new_player in team:
                    team.append(new_player)
                spy_count += 1
        
        while len(team)<team_size:
            agent = random.randrange(team_size)
            if agent not in team:
                team.append(agent)
        return team        

    def vote(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
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

    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        #nothing to do here
        pass

    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        By default, spies will betray 30% of the time. 
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
        It iss not expected or required for this function to return anything.
        '''
        #nothing to do here
        pass

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the numbe of missions (0-3) that have failed.
        '''
        #nothing to do here
        pass
    
    def game_outcome(self, spies_win, spies):
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail
        spies, a list of the player indexes for the spies.
        '''
        #nothing to do here
        pass



    def update_fail_rate(self):
        '''
        update the spy fail rate variables
        '''
        mode = 0

        if self.M < 4:
            if mode == 0:
                self.fail_rate = 0.6

            elif mode == 1:
                self.fail_rate = (3-self.failures) / (5-self.M)

            elif mode == 2:
                self.fail_rate = (3-self.failures) / (5-self.M-1)
        
        if self.fail_rate <= 0:
            self.fail_rate = 0.5