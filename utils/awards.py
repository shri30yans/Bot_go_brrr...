import random
import config
class Award:
    def __init__(self,name:str,reaction_id:str,karma_given_to_receiver:int,karma_given_to_giver:int,description:str,starboard_post:bool,cost:int):
        self.name=name
        self.reaction_id= reaction_id
        self.karma_given_to_receiver=karma_given_to_receiver
        self.karma_given_to_giver=karma_given_to_giver
        self.description=description
        self.starboard_post=starboard_post
        self.cost=cost


Wholesome_Award=Award(name="Wholesome",reaction_id=config.reddit_award_wholesome,karma_given_to_receiver=random.randint(6,10),karma_given_to_giver=random.randint(2,10),description="A wholesome award given out for wholesome moments",starboard_post=False,cost=20)
Helpful_Award=Award(name="Helpful",reaction_id=config.reddit_award_helpful,karma_given_to_receiver=random.randint(6,10),karma_given_to_giver=2,description="An award given to people who you feel were helpful",starboard_post=False,cost=10)
Gold_Award=Award(name="Gold",reaction_id=config.reddit_award_gold,karma_given_to_receiver=random.randint(20,50),karma_given_to_giver=random.randint(20,35),description="Gold Award",starboard_post=True,cost=100)
Silver_Award=Award(name="Silver",reaction_id=config.reddit_award_silver,karma_given_to_receiver=random.randint(10,30),karma_given_to_giver=random.randint(10,20),description="Silver Award",starboard_post=False,cost=60)
Platinum_Award=Award(name="Platinum",reaction_id=config.reddit_award_platinum,karma_given_to_receiver=random.randint(50,100),karma_given_to_giver=random.randint(30,45),description="Platinum Award",starboard_post=True,cost=150)
Trinity_Award=Award(name="Trinity",reaction_id=config.reddit_award_trinity,karma_given_to_receiver=random.randint(300,500),karma_given_to_giver=random.randint(100,150),description="Trinty Award",starboard_post=True,cost=500)