import random
import config


class Award:
    def __init__(
        self,
        name: str,
        reaction_id: str,
        description: str,
        cost: int = None,
        karma_required=None,
    ):
        self.name = name
        self.reaction_id = reaction_id
        self.description = description
        self.cost = cost
        self.karma_required = karma_required


badges_list = {
    "Stonks_Badge": Award(
        name="Stonks",
        reaction_id=config.badge_stonks,
        description="stonks go brrr",
        karma_required=5000,
    ),
    "Gold_Stonks_Badge": Award(
        name="Gold Stonks",
        reaction_id=config.badge_gold_stonks,
        description="Only the dankest shitposters get this",
        karma_required=10000,
    ),
    "Legendary_Badge": Award(
        name="Legendary Badge",
        reaction_id=config.badge_legendary,
        description="A very rare badge. Only rich people have this.",
        cost=100000,
    ),
    "Mythic_Badge": Award(
        name="Mythic Badge",
        reaction_id=config.badge_mythic,
        description="An extremly rare badge to flex how rich you are.",
        cost=500000,
    ),
    "Ultimate_Badge": Award(
        name="Ultimate Badge",
        reaction_id=config.badge_ultimate,
        description="Only the richest of rich can afford this.",
        cost=1000000,
    ),
    "Double_Credits_Badge": Award(
        name="Double Credits Badge",
        reaction_id=config.badge_double_credits,
        description="Doubles the amount of any credits earned.",
    ),
    "Double_Karma_Badge": Award(
        name="Double Karma Badge",
        reaction_id=config.badge_double_karma,
        description="Doubles the amount of any karma earned.",
    ),
}
