

class Weapon:
    def __init__(self,display_name:str,names:str,type_of_item,subtype,damage,cost:int,description:str,sellable=True):
        self.display_name=display_name
        self.names=names
        self.type=type_of_item
        self.cost=cost
        self.damage=damage
        self.description=description
        self.subtype=subtype
        self.sellable=sellable
        #melee,shortrange,heavy,longrange,midrange
class Healable:
    def __init__(self,display_name:str,names:str,type_of_item,heal,cost:int,description:str,sellable:bool=True):
        self.display_name=display_name
        self.names=names
        self.type=type_of_item
        self.cost=cost
        self.heal=heal
        self.description=description
        self.sellable=sellable

class Item_list:
        DarkSaber = Weapon(display_name="Dark Saber",names=["dark saber","darksaber"],type_of_item="weapon",subtype="melee",damage=list(range(100,151)),cost =50000,description="A legendary, one of a kind light saber. The wielder can claim the throne of Mandalore (Damage:100-150)",sellable=False)
        BeskarSword = Weapon(display_name="Beskar Sword",names=["beskar sword","beskarsword"],type_of_item="weapon",subtype="melee",damage=list(range(65,75)),cost =30000,description="A sword made out of pure Beskar. (Damage:62-75)")
        BeskarStaff = Weapon(display_name="Beskar Staff",names=["beskar staff","beskarstaff"],type_of_item="weapon",subtype="melee",damage=list(range(60,81)),cost =30000,description="A staff wielded by the extremly skilled Mandalores.(Damage:60-80)")
        
        DLT19HeavyBlasterRifle = Weapon(display_name="DLT-19 Heavy Blaster Rifle",names=["dlt-19 heavy blaster rifle","dlt 19 heavy blaster rifle","dlt19heavyblasterrifle","dlt19"],type_of_item="weapon",subtype="heavy",damage=list(range(42,47)),cost =11000,description="With high rate of fire, heavy damage and long-range, the DLT-19 is one of the best heavy weapons (Damage:42-46)")
        FWMB10RepeatingBlaster = Weapon(display_name="FWMB-10 repeating blaster",names=["fwmb-10 repeating blaster","fwmb 10 repeating blaster","fwmb 10","fwmb-10"],type_of_item="weapon",subtype="heavy",damage=list(range(35,46)),cost =15000,description="also known as the megablaster, this heavy weapon is filled with features (Damage:30-45)")
        Z6RotaryBlasterCannon = Weapon(display_name="Z-6 Rotary Blaster Cannon",names=["Z-6 rotary blaster cannon","Z-6","Z6 rotary blaster cannon","Z6"],type_of_item="weapon",subtype="heavy",damage=list(range(38,49)),cost =20000,description="also known as the megablaster, this heavy weapon is filled with features (Damage:38-48)")


        EE3Carbine_Rifle = Weapon(display_name="EE-3 Carbine Rifle",names=["ee-3 carbine rifle","ee3"],type_of_item="weapon",subtype="midrange",damage=list(range(30,37)),cost =9000,description="A medium range weapon with three automatic burst rounds (Damage:30-36)")
        DC15ABlasterRifle = Weapon(display_name="DC-15A Blaster Rifle",names=["dc-15a blaster rifle","dc-15a","dc 15a"],type_of_item="weapon",subtype="midrange",damage=list(range(22,39)),cost =7500,description="A medium-long range, powerful blaster rifle (Damage:22-38)")
        
        
        EE4Carbine_Rifle = Weapon(display_name="EE-4 Carbine Rifle",names=["ee-4 carbine rifle","ee4"],type_of_item="weapon",subtype="shortrange",damage=list(range(28,33)),cost =6000,description="A short range, modified blaster rifle (Damage:28-35)")
        DX13BlasterPistol = Weapon(display_name="DX-13 Blaster Pistol",names=["DX13","DX 13","DX 13 blaster pistol","DX-13 blaster pistol"],type_of_item="weapon",subtype="shortrange",damage=list(range(30,36)),cost =7000,description="A unigue pistol with a more precise, single shot fire mode as well as a more deadly rapid fire one (Damage:30-35)")
        Westar34BlasterPistol = Weapon(display_name="Westar-34 Blaster Pistol",names=["westar-34","westar 34","westar 34 blaster pistol","westar-34 blaster pistol"],type_of_item="weapon",subtype="shortrange",damage=list(range(32,39)),cost =8500,description="Designed intense surprise attacks at close range, the WESTAR-34 blaster pistol is made from an expensive dallorian alloy (Damage:32-38)")
        Model_434 = Weapon(display_name="The Model 434",names=["the model 434","model 434","deathhammer"],type_of_item="weapon",subtype="shortrange",damage=list(range(36,41)),cost =9000,description="A compact blaster pistol, the 434 earned the nickname \"DeathHammer\" from its loyal users because of its heavy durasteel plating and deadly fire capability (Damage:36-40)")
        DL44HeavyBlasterPistol = Weapon(display_name="DL-44 Heavy Blaster Pistol",names=["dl-44 heavy blaster pistol","dl-44","dl 44"],type_of_item="weapon",subtype="shortrange",damage=list(range(36,46)),cost =11000,description="A powerful, highly modifiable and accurate blaster pistol. It packs a heavy punch without losing accuracy (Damage:36-45)")
        E11 = Weapon(display_name="E-11 Blaster",names=["e-11 Blaster","e11 blaster","e11","e-11"],type_of_item="weapon",subtype="midrange",damage=list(range(10,15)),cost=1000,description="The basic starter pistol given to all in the Mandalorian Creed. (Damage:10-14)",sellable=False)
        #ThermalDetonator = Weapon(display_name="EE-4 Carbine Rifle",names=["thermaldetonator","thermal detonator",],type_of_item="weapon",subtype="explosive",damage=(list(range(1,5))+list(range(20,25))),cost =20000,description="A short range fire, modified blaster rifle(Damage:40-60)")
        
        Bandages = Healable(display_name="Bandage",names=["bandage","bandages"],type_of_item="health",heal=list(range(10,21)),cost =20,description="A basic healable to heal little damage (10-20)")
        Potion = Healable(display_name="Potion of Healing",names=["potion"],type_of_item="health",heal=list(range(20,40)),cost =50,description="A healable used to cure heal more damage (20-40)")
        Medkit = Healable(display_name="Medical Kit",names=["medkit"],type_of_item="health",heal=list(range(40,80)),cost =50,description="A better healable used to heal more serious injuries (40-80)")
