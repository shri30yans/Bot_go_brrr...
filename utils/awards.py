import random
import config


class Award:
    def __init__(
        self,
        name: str,
        reaction_id: str,
        karma_given_to_receiver: int,
        karma_given_to_giver: int,
        credits_given_to_receiver,
        description: str,
        starboard_post: bool,
        cost: int,
        animated_reaction_id=None,
    ):
        self.name = name
        self.reaction_id = reaction_id
        self.animated_reaction_id = animated_reaction_id
        self.karma_given_to_receiver = karma_given_to_receiver
        self.karma_given_to_giver = karma_given_to_giver
        self.description = description
        self.starboard_post = starboard_post
        self.cost = cost
        self.credits_given_to_receiver = credits_given_to_receiver


awards_list = {
    "Wholesome_Award": Award(
        name="Wholesome",
        reaction_id=config.reddit_award_wholesome,
        karma_given_to_receiver=5,
        karma_given_to_giver=random.randint(2, 10),
        credits_given_to_receiver=0,
        description="A wholesome award given out for *wholesome* moments",
        starboard_post=False,
        cost=15,
    ),
    # "Rocket_Like":Award(name="Rocket Like",reaction_id=config.reddit_award_rocket_like,
    #                     karma_given_to_receiver=random.randint(5,10),karma_given_to_giver=0,
    #                     credits_given_to_receiver=0,
    #                     description="Rockets go brrr! For posts that a upvote doesn't do justice",
    #                     starboard_post=False,
    #                     cost=25),
    # "Rocket_Dislike":Award(name="Rocket Disike",reaction_id=config.reddit_award_rocket_dislike,
    #                     karma_given_to_receiver=random.randint(-10,-5),karma_given_to_giver=0,
    #                     credits_given_to_receiver=0,
    #                     description="Rockets go brrr! Reduces karma for the reciever.",
    #                     starboard_post=False,
    #                     cost=25),
    "Silver_Award": Award(
        name="Silver",
        reaction_id=config.reddit_award_silver,
        karma_given_to_receiver=random.randint(10, 30),
        karma_given_to_giver=random.randint(10, 20),
        credits_given_to_receiver=0,
        description="Just a Silver award",
        starboard_post=False,
        cost=100,
    ),
    "Gold_Award": Award(
        name="Gold",
        reaction_id=config.reddit_award_gold,
        karma_given_to_receiver=random.randint(20, 50),
        karma_given_to_giver=random.randint(20, 35),
        credits_given_to_receiver=0,
        description="For posts you think are worth gilding.",
        starboard_post=False,
        cost=200,
    ),
    "Platinum_Award": Award(
        name="Platinum",
        reaction_id=config.reddit_award_platinum,
        karma_given_to_receiver=random.randint(50, 80),
        karma_given_to_giver=random.randint(30, 45),
        credits_given_to_receiver=20,
        description="An Award for a good post.\n (awards the reciever coins)",
        starboard_post=False,
        cost=500,
    ),
    "Argentinum_Award": Award(
        name="Argentinum",
        reaction_id=config.reddit_award_argentinum,
        karma_given_to_receiver=random.randint(200, 300),
        karma_given_to_giver=random.randint(70, 100),
        credits_given_to_receiver=random.randint(200, 250),
        description="Latin for distinguished, it’s for those who deserve outsized recognition.\n(Posts to starboard and awards the reciever coins)",
        starboard_post=True,
        cost=1000,
    ),
    "Ternion_Award": Award(
        name="Ternion",
        reaction_id=config.reddit_award_ternion,
        karma_given_to_receiver=random.randint(300, 500),
        karma_given_to_giver=random.randint(100, 150),
        credits_given_to_receiver=random.randint(400, 500),
        description="An award reserved for the very best posts.\n(Posts to starboard and awards the reciever coins)",
        starboard_post=True,
        cost=2000,
    ),
}
