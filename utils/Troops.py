import random
class Character:
    def __init__(self,name:str,health,attacks,xp,coins,not_effective,effective,no_effect_against,description:str):
        self.name=name
        self.health=health
        self.attacks=attacks
        self.xp=xp
        self.coins=coins
        self.description=description
        self.not_effective=not_effective
        self.effective=effective
        self.no_effect_against=no_effect_against
        #melee,shortrange,heavy,longrange,

class Character_lists:
    mudhorn=Character(
        name="Mudhorn",
        health=400,
        attacks=[
            {"charged you":list(range(1,61))},
            {"rammed":list(range(1,31))},
            {"stomped":list(range(1,21))}
            ],
        xp=200,
        coins=list(range(50,150)),
        effective=[],
        not_effective=["melee"],
        no_effect_against=["longrange"],
        description="muddwelling giant horned beast"
        )


    javas= Character(
        name="Java",
        health=50,
        attacks=[
                {"poked you":list(range(1,10))},
                {"robbed you":list(range(1,10))},
                {"ran their Sandcrawler over you":list(range(1,30))},
                {"used Jawa ion blaster's":list(range(1,20))},
                {"used Ion Pistol's":list(range(1,10))},
                {"used Jawa ion blaster's":list(range(1,15))},
                {"used their Droids to attack you":list(range(1,30))}
                ],
        xp=20,
        coins=list(range(10,20)),
        effective=["melee","longrange"],
        not_effective=[],
        no_effect_against=[],
        description="java")

    storm_tropper_squad=Character(
        name="Storm Troopers squad",
        health=150,
        attacks=[
                {"shot at you with the E-11 blaster rifle":list(range(1,20))},
                {"used MPL-57 grenade launchers":list(range(1,30))},
                {"used DLT-19 heavy blaster rifle's":list(range(1,25))},
                {"used RT-97C heavy blaster rifle's":list(range(1,25))},
                {"used E-22 blaster rifle's":list(range(1,20))}
                ],
        xp=20,
        coins=list(range(20,50)),
        effective=["melee","heavy"],
        not_effective=[],
        no_effect_against=[],
        description="4 Storm Trooper's ")

    tusken_raiders=Character(
        name="Tusken raiders",
        health=100,
        attacks=[
                    {"shot you with Tusken cycler rifle":list(range(1,20))},
                    {"used Gaderffii sticks":list(range(1,15))}
                ],
        xp=50,
        coins=list(range(20,30)),
        effective=["melee"],
        not_effective=[],
        no_effect_against=[],
        description="Tusken raiders common in Tatooine")
    
