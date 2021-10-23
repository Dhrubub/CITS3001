from BeliefBot import BeliefBot
from random_agent import RandomAgent

from game import Game

agents5 = [RandomAgent(name='s1'), 
        RandomAgent(name='s2'),
        BeliefBot(name='r1'),  
        BeliefBot(name='r2'),  
        BeliefBot(name='r3'),
        ]

agents6 = [RandomAgent(name='s1'), 
        RandomAgent(name='s2'),
        BeliefBot(name='r1'),  
        BeliefBot(name='r2'),  
        BeliefBot(name='r3'),
        BeliefBot(name='r4'),
        ]

agents7 = [RandomAgent(name='s1'), 
        RandomAgent(name='s2'),
        RandomAgent(name='s3'),  
        BeliefBot(name='r1'),  
        BeliefBot(name='r2'),  
        BeliefBot(name='r3'),
        BeliefBot(name='r4'),   
        ]

agents8 = [RandomAgent(name='s1'), 
        RandomAgent(name='s2'),
        RandomAgent(name='s3'),  
        BeliefBot(name='r1'),  
        BeliefBot(name='r2'),  
        BeliefBot(name='r3'),
        BeliefBot(name='r4'), 
        BeliefBot(name='r5'),  
        ]

agents9 = [RandomAgent(name='s1'), 
        RandomAgent(name='s2'),
        RandomAgent(name='s3'),  
        BeliefBot(name='r1'),  
        BeliefBot(name='r2'),  
        BeliefBot(name='r3'),
        BeliefBot(name='r4'),  
        BeliefBot(name='r5'), 
        BeliefBot(name='r6'), 
        ]

agents10 = [RandomAgent(name='s1'), 
        RandomAgent(name='s2'),
        RandomAgent(name='s3'),  
        RandomAgent(name='s4'),  
        BeliefBot(name='r1'),  
        BeliefBot(name='r2'),  
        BeliefBot(name='r3'),
        BeliefBot(name='r4'),  
        BeliefBot(name='r5'), 
        BeliefBot(name='r6'),   
        ]

all_agents = [agents5, agents6, agents7, agents8, agents9, agents10]
for agents in all_agents:
        b = 25
        c = 0
        for j in range(b):
                a = 0
                for i in range(b):
                        game = Game(agents)
                        game.play()
                        if str(game)[:3] == "won":
                                a+=1
                        # print(game)
                c += a

        c = c / b
        if b == 25:
                c*=4
                b*=4
        print(str(c) + "/" + str(b))


