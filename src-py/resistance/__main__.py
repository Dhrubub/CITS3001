from random_agent import RandomAgent
from BeliefBot import BeliefBot

from game import Game

agents5 = [BeliefBot(name='s1'), 
        BeliefBot(name='s2'),
        BeliefBot(name='r1'),  
        BeliefBot(name='r2'),  
        BeliefBot(name='r3'),
        ]

agents6 = [BeliefBot(name='s1'), 
        BeliefBot(name='s2'),
        BeliefBot(name='r1'),  
        BeliefBot(name='r2'),  
        BeliefBot(name='r3'),
        BeliefBot(name='r4'),
        ]

agents7 = [BeliefBot(name='s1'), 
        BeliefBot(name='s2'),
        BeliefBot(name='s3'),  
        BeliefBot(name='r1'),  
        BeliefBot(name='r2'),  
        BeliefBot(name='r3'),
        BeliefBot(name='r4'),   
        ]

agents8 = [BeliefBot(name='s1'), 
        BeliefBot(name='s2'),
        BeliefBot(name='s3'),  
        BeliefBot(name='r1'),  
        BeliefBot(name='r2'),  
        BeliefBot(name='r3'),
        BeliefBot(name='r4'), 
        BeliefBot(name='r5'),  
        ]

agents9 = [BeliefBot(name='s1'), 
        BeliefBot(name='s2'),
        BeliefBot(name='s3'),  
        BeliefBot(name='r1'),  
        BeliefBot(name='r2'),  
        BeliefBot(name='r3'),
        BeliefBot(name='r4'),  
        BeliefBot(name='r5'), 
        BeliefBot(name='r6'), 
        ]

agents10 = [BeliefBot(name='s1'), 
        BeliefBot(name='s2'),
        BeliefBot(name='s3'),  
        BeliefBot(name='s4'),  
        BeliefBot(name='r1'),  
        BeliefBot(name='r2'),  
        BeliefBot(name='r3'),
        BeliefBot(name='r4'),  
        BeliefBot(name='r5'), 
        BeliefBot(name='r6'),   
        ]

all_agents = [agents5, agents6, agents7, agents8, agents9, agents10]
for agents in all_agents:
        b = 100
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
        print(str(c) + "/" + str(b))


