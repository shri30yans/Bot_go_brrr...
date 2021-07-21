import random
import config
class Award:
    def __init__(self,name:str,reaction_id:str,description:str,cost:int=None,):
        self.name=name
        self.reaction_id= reaction_id
        self.description=description
        self.cost=cost


Wholesome_Award=Award(name="Wholesome",reaction_id=config.reddit_award_wholesome,
                    description="A wholesome award given out for *wholesome* moments",
                    cost=15)

