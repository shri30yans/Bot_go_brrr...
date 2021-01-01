import os, sys,discord, platform, random, aiohttp, json,time,asyncio
from discord.ext import commands,tasks,menus
from discord.ext.commands import Greedy
from discord.ext.commands.cooldowns import BucketType
import asyncpg
from utils.Troops import Character_lists
from utils.Items import Item_list

class EmbedPageSource(menus.ListPageSource):
    async def format_page(self, menu, embed):
        return embed


main_shop=[
            Item_list.BeskarSword,
            Item_list.BeskarStaff,
            Item_list.EE4Carbine_Rifle,
            Item_list.Bandages,
            Item_list.DarkSaber,
            Item_list.DLT19HeavyBlasterRifle,
            Item_list.FWMB10RepeatingBlaster,
            Item_list.Z6RotaryBlasterCannon,
            Item_list.EE3Carbine_Rifle,
            Item_list.DC15ABlasterRifle,
            Item_list.EE4Carbine_Rifle,
            Item_list.DX13BlasterPistol,
            Item_list.Westar34BlasterPistol,
            Item_list.Model_434,
            Item_list.DL44HeavyBlasterPistol,
            Item_list.Bandages,
            Item_list.Potion,
            Item_list.Medkit]
all_items=[
            Item_list.BeskarSword,
            Item_list.BeskarStaff,
            Item_list.EE4Carbine_Rifle,
            Item_list.Bandages,
            Item_list.DarkSaber,
            Item_list.DLT19HeavyBlasterRifle,
            Item_list.FWMB10RepeatingBlaster,
            Item_list.Z6RotaryBlasterCannon,
            Item_list.EE3Carbine_Rifle,
            Item_list.DC15ABlasterRifle,
            Item_list.EE4Carbine_Rifle,
            Item_list.DX13BlasterPistol,
            Item_list.Westar34BlasterPistol,
            Item_list.Model_434,
            Item_list.DL44HeavyBlasterPistol,
            Item_list.Bandages,
            Item_list.Potion,
            Item_list.Medkit]

    


colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
            0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Stats",aliases=["account"], help='Balance of a user')
    async def bal(self,ctx,user:discord.Member=None):
        user=user or ctx.author
        if user.bot:
            await ctx.send(f"{user.name} is a bot. Bots don't have accounts.")
        else:
        # retrieve an individual connection from our pool, defined later
            async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
                async with connection.transaction():
                    await self.create_account(ctx,user)
                    user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
                    user_account=dict(user_account)
                    health_j=json.loads(user_account['health'])
                    embed=discord.Embed(Title=f"{ctx.author.name}'s Statistics")
                    embed.add_field(name="Imperial Credits:",value=f"{user_account['credits']} credits")
                    embed.add_field(name="XP:",value=f"{user_account['xp']} XP")
                    embed.add_field(name="Health:",value=f"{health_j['health']} out of {health_j['max_health']} health")
                    #embed.add_field(name="XP:",value=f"{user_account['xp']} ",inline=True)
                    embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Star Wars Bot ")
                    await ctx.send(embed=embed)
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Shop", help='Shop')
    async def shop(self,ctx):
        user=ctx.author
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await self.create_account(ctx,user)
                user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
                user_account=dict(user_account)
                healables_string,weapons_string="",""
                weapons_string_length,healables_string_length=0,0
                weapons_list,healables_list=[],[]
                for item in main_shop :
                    name=item.display_name
                    cost=item.cost

                    if item.type == "health":
                        healables_string_length=healables_string_length+len(str(healables_string +"**"+ name +"**" +"\n" + "Cost: " + str(cost) + "\n" + "Description:" + item.description+ "\n"))
                        if healables_string_length<1000:
                            healables_string=healables_string +"**"+ name +"**" +"\n" + "Cost: " + str(cost) + "\n" + "Description:" + item.description+ "\n"
                            
                        else:
                            healables_string_length=0
                            healables_list.append(healables_string)
                            healables_string="**"+ name +"**" +"\n" + "Cost: " + str(cost) + "\n" + "Description:" + item.description+ "\n"
                            
                    
                    elif item.type == "weapon":
                        #print(item)
                        weapons_string_length= weapons_string_length +len(str(weapons_string +"**"+ name +"**" +"\n" + "Cost: " + str(cost) + "\n" + "Description:" + item.description+ "\n"))
                        if weapons_string_length <= 1000:
                            weapons_string= weapons_string +"**"+ name +"**" +"\n" + "Cost: " + str(cost) + "\n" + "Description:" + item.description+ "\n"
                            
                        else:
                            weapons_list.append(weapons_string)
                            weapons_string="**"+ name +"**" +"\n" + "Cost: " + str(cost) + "\n" + "Description:" + item.description+ "\n"
                            weapons_string_length=0
                    else:
                        print("Item type error")
                
                weapons_list.append(weapons_string)
                #print(weapons_list)
                #print(healables_list)
                embeds_list = []
                for embed_string in weapons_list:
                    #index=weapons_string_length.index(embed_string)
                    embeds_list.append(discord.Embed(title =f"The Shop",color = random.choice(colourlist),timestamp=ctx.message.created_at).add_field(name=f"Weapons:",value=f"{embed_string}").set_thumbnail(url='https://i.imgur.com/sulsWKB.jpeg').set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Star Wars Bot "))
                for embed_string in healables_list:
                    #index=weapons_string_length.index(embed_string)
                    embeds_list.append(discord.Embed(title =f"The Shop",color = random.choice(colourlist),timestamp=ctx.message.created_at).add_field(name=f"Healables:",value=f"{embed_string}").set_thumbnail(url='https://i.imgur.com/sulsWKB.jpeg').set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Star Wars Bot "))
                
                menu = menus.MenuPages(EmbedPageSource(embeds_list, per_page=1))
                await menu.start(ctx)


                    



    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Heal", help='Heal')
    async def heal(self,ctx,item_entered:str="bandage"): 
        user=ctx.author
        # retrieve an individual connection from our pool, defined later
        async with self.bot.pool.acquire() as connection:
        # create a transaction for that connection
            async with connection.transaction():
                await self.create_account(ctx,user)
                user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
                user_account=dict(user_account)
                health_j=json.loads(user_account["health"])
                for item in main_shop:  
                    item_found=None
                    if item_entered.lower() in item.names:
                        if item.type=="health":
                            item_found=item
                            break
                if item_found == None:
                    await ctx.send(f"{item_entered.lower().title()} is not found.")
                else:
                    #item_to_buy=dict(item_found)
                    if health_j["health"] == health_j["max_health"]:
                        await ctx.send("You are at max health. Can't heal anymore")
                    else:
                        healables_j=json.loads(user_account["healables"])
                        if healables_j[item.names[0]]==0:
                            await ctx.send("You don't have this item. Buy it first from the shop")
                        else:
                            healables_j[item.names[0]]=healables_j[item.names[0]]-1
                            item_to_add=json.dumps(healables_j)
                            healed_amt=random.choice(item.heal)
                            character_health=min(health_j["health"]+healed_amt,health_j["max_health"])
                            health_j["health"]=character_health
                            health=json.dumps(health_j)

                            await connection.execute("UPDATE star_wars_table SET healables = $1 WHERE user_id=$2",item_to_add,ctx.author.id)
                            await connection.execute("UPDATE star_wars_table SET health = $1 WHERE user_id=$2",health,ctx.author.id)
                            await ctx.send(f"Used **{item.display_name.title()}** and healed for {healed_amt} damage. Current health is {character_health}")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Buy", help='Balance of a user')
    async def buy(self,ctx,*item_entered):
        try:
            quantity=(int(item_entered[-1]))
            item_entered=item_entered[0:-1]
        except:
            quantity=1
        if len(item_entered) > 1:
            item_entered =  ' '.join(item_entered)
        else:
            item_entered = item_entered[0]
        user=ctx.author
        # retrieve an individual connection from our pool, defined later
        async with self.bot.pool.acquire() as connection:
        # create a transaction for that connection
            async with connection.transaction():
                await self.create_account(ctx,user)
                user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
                user_account=dict(user_account)
                for item in main_shop:  
                    item_found=None
                    if item_entered.lower() in item.names:
                        item_found=item
                        break
                if item_found == None:
                    await ctx.send(f"{item_entered} is not found.")
                else:
                    #item_to_buy=dict(item_found)
                    if user_account["credits"] < (item_found.cost * quantity):
                        await ctx.send("Can't afford")
                    else:
                        bal=user_account["credits"] - (item_found.cost* quantity)
                        if item_found.type== "weapon":
                            weapons=user_account["weapons"]
                            weapons_j=json.loads(weapons)
                            if item.names[0] in weapons_j:
                                weapons_j[item.names[0]]=weapons_j[item.names[0]]+ quantity
                            else:
                                weapons_j.update({item.names[0]:quantity})
                            
                            for checking_if_zero in weapons_j:
                                if weapons_j[checking_if_zero]==0:
                                    del weapons_j[item]
                            item_to_add=json.dumps(weapons_j)
                            await connection.execute("UPDATE star_wars_table SET weapons = $1 WHERE user_id=$2",item_to_add,ctx.author.id)

                        elif item_found.type == "health":
                            healables=user_account["healables"]
                            healables_j=json.loads(healables)
                            if item.names[0] in healables_j:
                               healables_j[item.names[0]]=healables_j[item.names[0]]+quantity
                            else:
                                healables_j.update({item.names[0]:quantity})
                            item_to_add=json.dumps(healables_j)

                            await connection.execute("UPDATE star_wars_table SET healables = $1 WHERE user_id=$2",item_to_add,ctx.author.id)
                        else:
                            print("random class")
                            return
                        

                        await connection.execute("UPDATE star_wars_table SET credits = $1 WHERE user_id=$2",bal,ctx.author.id)
                        await ctx.send(f"Bought {quantity}{item.display_name}('s)")
                # embed=discord.Embed(Title=f"{item}")
                # embed.add_field(name="Imperial Credits:",value=f"{user_account['credits']} credits")
                # embed.add_field(name="XP:",value=f"{user_account['xp']} credits")
                # embed.add_field(name="XP:",value=f"{user_account['xp']} ",inline=True)
                # embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Star Wars Bot ")
                # await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Sell", help='Balance of a user')
    async def sell(self,ctx,*item_entered):
        try:
            quantity=(int(item_entered[-1]))
            item_entered=item_entered[0:-1]
        except:
            quantity=1
        if len(item_entered) > 1:
            item_entered =  ' '.join(item_entered)
        else:
            item_entered = item_entered[0]
        #item_entered =  ' '.join(item_entered) 
        #print(item_entered)
        user=ctx.author
        # retrieve an individual connection from our pool, defined later
        async with self.bot.pool.acquire() as connection:
        # create a transaction for that connection
            async with connection.transaction():
                await self.create_account(ctx,user)
                user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
                user_account=dict(user_account)
                for item in main_shop:  
                    item_found=None
                    if item_entered.lower() in item.names:
                        item_found=item
                        break
                if item_found == None:
                    await ctx.send(f"{item_entered} is not found.")
                
                elif item_found.sellable == False:
                    await ctx.send(f"{item.display_name} cannot be sold.")

                else:
                    if item_found.type== "weapon":
                        weapons=user_account["weapons"]
                        weapons_j=json.loads(weapons)
                        if item.names[0] in weapons_j and weapons_j[item.names[0]] != 0 :
                            weapons_j[item.names[0]]=weapons_j[item.names[0]]-quantity
                            updated_weapons_j=json.dumps(weapons_j)
                            credits_to_add=round((item.cost * quantity)*(75/100))
                            await connection.execute("UPDATE star_wars_table SET weapons = $1 WHERE user_id=$2",updated_weapons_j,ctx.author.id)
                            await connection.execute("UPDATE star_wars_table SET credits = $1 WHERE user_id=$2",user_account["credits"]+credits_to_add,ctx.author.id)
                            await ctx.send (f"You sold {quantity} **{item.display_name.capitalize()}** and earned {credits_to_add} credits.")

                        else:
                            await ctx.send ("Can't sell what you dont have")
                            

                    elif item_found.type == "health":
                        healables=user_account["healables"]
                        healables_j=json.loads(healables)
                        if item.names[0] in healables_j and healables_j[item.names[0]] != 0 :
                            healables_j[item.names[0]]=healables_j[item.names[0]]-quantity
                            updated_healables_j=json.dumps(healables_j)
                            credits_to_add=round((item.cost * quantity)*(75/100))
                        else:
                            await ctx.send ("Can't sell what you dont have")

                        await connection.execute("UPDATE star_wars_table SET healables = $1 WHERE user_id=$2",updated_healables_j,ctx.author.id)
                        await connection.execute("UPDATE star_wars_table SET credits = $1 WHERE user_id=$2",user_account["credits"]+credits_to_add,ctx.author.id)
                        await ctx.send (f"You sold {quantity} **{item.display_name.capitalize()}** and earned {credits_to_add} credits.")
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(1, commands.BucketType.user, wait=False)
    @commands.command(name="Explore",aliases=["exp"], help='Explore a region to earn quick cash ')
    async def Explore(self,ctx):
        user=ctx.author
        # retrieve an individual connection from our pool, defined later
        async with self.bot.pool.acquire() as connection:
            await self.create_account(ctx,user)
            # create a transaction for that connection
            async with connection.transaction():
                await self.create_account(ctx,user)
                user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
                user_account=dict(user_account)
                choices =random.sample([{"Coruscant":"Cosmopolitan urban world"},{"Dagobah":"remote swamps and forests"},{"Mustafar":"extremely hot and volcanic hellscapes"},{"Hoth":"inhospitable icy plains"},{"Utapau":"rocky cities and enormous sinkholes"},{"Tatooine":" the sandy dunes, mountains, and canyons"},{"Bespin":"high buildings, cloud cities and mines"},{"Naboo":"beautiful landscapes, classical architecture and oceans"},{"Mandalore":"desolate ruins"}],k=3)
                location_names,location_description = [] ,[]
                
                for location in choices : 
                    location_names.extend(location) #extend appends all the elements of a list L1 to a list L2
                for location in choices : 
                    location_description.extend(location.values()) 
                location_names.extend(['1','2','3'])               
                try:
                    await ctx.send(f"What would you like to explore? **{location_names[0]}** (1), **{location_names[1]}** (2) or **{location_names[2]}** (3). Enter a location below:")
                    msg = await self.bot.wait_for('message', check=lambda m:(m.author==ctx.author and m.content.lower().capitalize() in location_names), timeout=30.0)
                except asyncio.TimeoutError:
                    await ctx.send(embed=discord.Embed(title ="Explore command Timed Out!",description=f"{ctx.author.name} took too much time and didn't reply.",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Star Wars Bot "))
                    return 
                else:
                    #event=random.choice(["cash","fight","fight"])
                    event="fight"
                    if event == "cash":
                        earnings=random.randint(1,60)
                        if msg.content.lower().capitalize() in [location_names[0],'1']:
                            await ctx.send(f"You explored the {location_description[0]} of {location_names[0]} and found {earnings} credits.")
                        
                        elif msg.content.lower().capitalize() in [location_names[1],'2']:
                            await ctx.send(f"You explored the {location_description[1]} of {location_names[1]} and found {earnings} credits.")
                        
                        elif msg.content.lower().capitalize() in [location_names[2],'3']:
                            await ctx.send(f"You explored the {location_description[2]} of {location_names[2]} and found {earnings} credits.")
                        await connection.execute("UPDATE star_wars_table SET credits = $1 WHERE user_id=$2",user_account["credits"]+earnings,ctx.author.id)
                    
                    elif event == "fight":
                        health_j=json.loads(user_account["health"])
                        if msg.content.lower().capitalize() in [location_names[0],'1']:
                            #await ctx.send(f"You explored {location_names[0]} and now have to fight lol")
                            await self.fight(ctx,health_j)
                        elif msg.content.lower().capitalize() in [location_names[1],'2']:
                            #await ctx.send(f"You explored {location_names[1]} and now have to fight lol")
                            await self.fight(ctx,health_j)
                        elif msg.content.lower().capitalize() in [location_names[2],'3']:
                            #await ctx.send(f"You explored {location_names[2]} and now have to fight lol")
                            await self.fight(ctx,health_j)
                    else:
                        await ctx.send("error")

    async def fight(self,ctx,health_j):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():

                player=ctx.author
                player_health=health_j["health"]
                max_player_health=health_j["max_health"]
                #original_player_health=health_j["health"]
                healables_uses_left=5
                character=random.choice([Character_lists.mudhorn,Character_lists.javas,Character_lists.storm_tropper_squad,Character_lists.tusken_raiders])
                character_health=character.health
                max_character_health=character.health
                weapon_recommendations=""
                user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",player.id)
                user_account=dict(user_account)
                weapons_j=json.loads(user_account["weapons"])
                weapons_j_string=""
                for item in weapons_j:
                    if item=="equipped":pass
                    elif weapons_j[item]==0:pass
                    else:
                        for item_info in all_items:
                            if item in item_info.names:
                                weapons_j_string= weapons_j_string + f"**{item_info.display_name.title()}** ({item_info.subtype.capitalize()})" +"\n"+ f"Damage: {min(item_info.damage)} - {max(item_info.damage)} " + " \n"
            
                if weapons_j_string=="":
                    weapons_j_string="You don't own any weapons. Buy them from the shop first"
                
                
                if len(character.effective) !=0:
                    weapon_recommendations = weapon_recommendations + f"Weapons effective against {character.name}: **{str(character.effective)[1:-1].upper()}** \n"
                if len(character.not_effective) !=0:
                    weapon_recommendations = weapon_recommendations + f" Weapons not effective against {character.name}: **{str(character.not_effective)[1:-1].upper()}** \n"
                if len(character.no_effect_against) !=0:
                    weapon_recommendations = weapon_recommendations + f"Weapons with no effects against {character.name}: **{str(character.no_effect_against)[1:-1].upper()}** \n"
                
                embed=discord.Embed(title=f"**{player.name} was attacked by {character.name}**",description=f"",color =0xFD5151,timestamp=ctx.message.created_at)
                #embed.add_field(name=f"{player.name} choose your weapon.",value=f"Choose a weapon from your inventory.\n Note that any weapon that has no effect the character would deal 0 damage. Choose your weapon carefully.\n Weapon choice cannot be switched in middle of a fight.\n To quit the fight type **\"QUIT\"**, at the cost of losing XP.",inline=False)
                embed.add_field(name=f"{player.name} choose your weapon.",value=f"Choose a weapon from your inventory.\n **Your Weapons** \n{weapons_j_string}\n To quit the fight type **\"QUIT\"**, at the cost of losing XP.",inline=False)
                embed.add_field(name=f"Weapon recommendations:",value=f"{weapon_recommendations}",inline=False)
                embed.set_footer(icon_url= player.avatar_url,text=f"Attack executed by {player.name} • Star Wars Bot ")    
                await ctx.send(embed=embed)

                async def choose_weapon(ctx):
                    user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",player.id)
                    user_account=dict(user_account)
                    weapons_j=json.loads(user_account["weapons"])
                    try:
                        #await ctx.send(f"Choose a weapon from your inventory. Make sure that any weapon that has no effect the character would deal 0 damage. Choose your wepon carefully. Wepon choic cannot be switched in middle of a fight")
                        msg = await self.bot.wait_for('message', check=lambda m:(m.author==ctx.author), timeout=30.0)
                    except asyncio.TimeoutError:
                        await ctx.send(embed=discord.Embed(title ="Timed Out!",description=f"{ctx.author.name} took too much time to choose a weapon.",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Star Wars Bot "))
                        return "time out"
                    else:
                        item_entered=msg.content.lower()
                        item_found=None
                        if item_entered in ["end","cancel","finish","quit","stop","exit","forefeit"]:
                            await ctx.send("You quit the fight and lost 20 XP")
                            return "game end"
                        for item in all_items:
                            if item_entered in item.names:
                                if item.names[0] in weapons_j:
                                    item_found=item
                                    break
                                else:
                                    await ctx.send(f" You don't own this {item.display_name}")
                        if item_found == None:
                            await ctx.send(f"{item_entered} is not found. Please enter a different weapon.")
                            weapon_selected=await choose_weapon(ctx)
                            return weapon_selected
                        else:
                            weapon_selected=item_found
                            return weapon_selected


                weapon_selected = await choose_weapon(ctx)
                if weapon_selected == "time out":
                    user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",player.id)
                    user_account=dict(user_account)
                    earnings=0
                    xp= -20
                    embed=discord.Embed(title=f"**Fight Timed Out!**",color =random.choice(colourlist),timestamp=ctx.message.created_at)
                    embed.add_field(name=f"{player.name} took too much time and the game timed out",value=f"You lost and gained {earnings} coins and {xp} XP",inline=False)
                    health_j["health"]=player_health
                    player_health=json.dumps(health_j)
                    await connection.execute("UPDATE star_wars_table SET xp = $1 WHERE user_id=$2",int(user_account["xp"])+xp,player.id)
                    return

                elif weapon_selected == "game end":
                    user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",player.id)
                    user_account=dict(user_account)
                    earnings=0
                    xp= -50
                    embed=discord.Embed(title=f"**Fight forfeited**",color =random.choice(colourlist),timestamp=ctx.message.created_at)
                    embed.add_field(name=f"{player.name} surrendered",value=f"You lost and gained {earnings} coins and {xp} XP",inline=False)
                    health_j["health"]=player_health
                    player_health=json.dumps(health_j)
                    await connection.execute("UPDATE star_wars_table SET xp = $1 WHERE user_id=$2",int(user_account["xp"])+xp,player.id)
                    return

                embed=discord.Embed(title=f"**{player.name} was attacked by {character.name}**",description=f"",color =0xFD5151,timestamp=ctx.message.created_at)
                embed.add_field(name=f"You choose {weapon_selected.names[0].title()}",value=f"{player.name} it's your turn first. Reply with \"**Attack**\" to attack , \"**Heal Healable-Name**\" to heal using Healables from your inventory or \"**End**\" to end the game",inline=False)
                embed.set_footer(icon_url= player.avatar_url,text=f"Attack executed by {player.name} • Star Wars Bot ")    
                await ctx.send(embed=embed)
                
                
                while (player_health != None and character_health != None) or (player_health > 0 and character_health > 0):             
                    def character_questions(player_health,character_health):
                        if character_health==max_character_health:
                            character_choice=random.choice(["attack"])#can't heal when max health
                        else:
                            character_choice=random.choice(["attack","heal"])
                        
                        if character_choice == 'attack':
                            choice=random.choice(character.attacks)
                            key_list = list(choice.keys())
                            val_list = list(choice.values())
                            attack=key_list[0]
                            damage=random.choice(val_list[0])
                            player_health=max(player_health-damage,0)
                            return player_health,character_health,"attack",attack,damage
                            
                        elif character_choice == 'heal':           
                            heal=random.randint(1,30)
                            character_health=min(character_health+heal,max_character_health)
                            return player_health,character_health,"heal","healed",heal
                    
                    async def player_questions(player_health,character_health,healables_uses_left):
                        try:
                            msg = await self.bot.wait_for('message', check=lambda m:(m.author==player), timeout=60.0)
                        except asyncio.TimeoutError:
                            #await ctx.send(embed=discord.Embed(title ="Game Timed Out!",description=f"{player.name} took too much time and has forfeited the game.",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Star Wars Bot "))
                            return "time out","time out","time out"
                        else:
                            if msg.content.lower() in ['attack','a','atk']:
                                #damage=random.randint(1,50)
                                if weapon_selected in character.effective:
                                    damage=random.choice(weapon_selected.damage) + 10 
                                elif weapon_selected in character.not_effective:
                                    damage=random.choice(weapon_selected.damage) - 15 
                                elif weapon_selected in character.no_effect_against:
                                    damage=0
                                else:
                                    damage=random.choice(weapon_selected.damage) 

                                character_health=max(character_health-damage,0)
                                
                                if character_health==0: return player_health,character_health,healables_uses_left
                                
                                player_health,character_health,move,name_of_move,amt=character_questions(player_health,character_health)
                                
                                player_healthbar,character_healthbar=self.healthbar_generator(player_health, character_health, max_player_health, max_character_health)
                                
                                
                                if player_health==0: return player_health,character_health,healables_uses_left

                                if move == "attack":
                                    embed=discord.Embed(title=f"**{player.name} attacked!**",description=f"**You attacked dealing {damage} damage.**\n**{character.name} {name_of_move} dealing {amt} damage.** ",color =0xFD5151,timestamp=ctx.message.created_at)
                                elif move=="heal":
                                    embed=discord.Embed(title=f"**{player.name} healed!**",description=f"**You attacked dealing {damage} damage.**\n**{character.name} {name_of_move} for {amt}.** ",color =0xFD5151,timestamp=ctx.message.created_at)
                                
                                embed.add_field(name=f"Health Bar" ,value=f"{player.name}\n  {player_healthbar}  {player_health}\n{character.name}\n  {character_healthbar} {character_health}")
                                embed.add_field(name=f"{character.name} your turn.",value=f"Reply with \"**Attack**\" to attack , \"**Use**\" an item from your inventory or \"**End**\" to end the game",inline=False)
                                embed.set_footer(icon_url= player.avatar_url,text=f"Attack executed by {player.name} • BB-9E ")    
                                await ctx.send(embed=embed)
                                return player_health,character_health,healables_uses_left
                            
                            elif msg.content.split()[0].lower() in ['heal','h']:
                                if healables_uses_left == 0:
                                    await ctx.send("You already used all your healable uses.You can't use anymore. Select a different option")
                                    player_health,character_health=await player_questions(player_health,character_health,healables_uses_left)
                                    return player_health,character_health,healables_uses_left
                                    
                                else:   
                                    user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",player.id)
                                    user_account=dict(user_account)
                                    healables_uses_left=healables_uses_left-1
                                    if len(msg.content.lower().split())==1:
                                        item_entered="bandage"
                                    else:
                                        item_entered=str(msg.content.lower().split()[1])
                                    
                                    user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",player.id)
                                    user_account=dict(user_account)
                                    #health_j=json.loads(user_account["health"])
                                    for item in main_shop:  
                                        item_found=None
                                        if item_entered.lower() in item.names[0].lower():
                                            if item.type=="health":
                                                item_found=item
                                                break
                                    if item_found == None:
                                        await ctx.send(embed=discord.Embed(title =f"{item_entered.lower().title()} is not found.",description=f"Choose another option. Reply with \"**Attack**\" to attack , \"**Heal Healable-Name**\" to heal using Healables from your inventory or \"**End**\" to end the game",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= player.avatar_url,text=f"Requested by {player} • Star Wars Bot "))
                                        player_health,character_health,healables_uses_left=await player_questions(player_health,character_health,healables_uses_left)
                                        return player_health,character_health,healables_uses_left
                                    else:
                                        #item_to_buy=dict(item_found)
                                        if character_health == max_player_health:
                                            await ctx.send(embed=discord.Embed(title =f"You are at max health. Can't heal anymore",description=f"Choose another option. Reply with \"**Attack**\" to attack , \"**Heal Healable-Name**\" to heal using Healables from your inventory or \"**End**\" to end the game",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= player.avatar_url,text=f"Requested by {player} • Star Wars Bot "))
                                            player_health,character_health,healables_uses_left=await player_questions(player_health,character_health,healables_uses_left)
                                            return player_health,character_health,healables_uses_left
                                        else:
                                            healables_j=json.loads(user_account["healables"])
                                            if healables_j[item.names[0]]==0:
                                                await ctx.send(embed=discord.Embed(title =f"You don't own {item.display_name}.",description=f"Choose another option. Reply with \"**Attack**\" to attack , \"**Heal Healable-Name**\" to heal using Healables from your inventory or \"**End**\" to end the game",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= player.avatar_url,text=f"Requested by {player} • Star Wars Bot "))
                                                player_health,character_health,healables_uses_left=await player_questions(player_health,character_health,healables_uses_left)
                                                return player_health,character_health,healables_uses_left
                                            else:
                                                healables_j[item.names[0]]=healables_j[item.names[0]]-1
                                                item_to_add=json.dumps(healables_j)
                                                healed_amt=random.choice(item.heal)
                                                character_health=min(character_health+healed_amt,max_player_health)

                                                await connection.execute("UPDATE star_wars_table SET healables = $1 WHERE user_id=$2",item_to_add,ctx.author.id)
                                                player_health,character_health,move,name_of_move,amt=character_questions(player_health,character_health)
                        
                                                player_healthbar,character_healthbar=self.healthbar_generator(player_health, character_health, max_player_health, max_character_health)                       
                                                if move == "attack":
                                                    embed=discord.Embed(title=f"**{player.name} attacked!**",description=f"**You used {item.display_name.title()} and healed for {healed_amt} damage. You now have {healables_uses_left} chances of using a healable in this fight. Spend them wisely. **\n**{character.name} {name_of_move} dealing {amt} damage.** ",color =0x7FFF00,timestamp=ctx.message.created_at)
                                                elif move=="heal":
                                                    embed=discord.Embed(title=f"**{player.name} healed!**",description=f"**You used {item.display_name.title()} and healed for {healed_amt} damage. You now have {healables_uses_left} chances of using a healable in this fight. Spend them wisely. **\n**{character.name} {name_of_move} for {amt}.** ",color =0x7FFF00,timestamp=ctx.message.created_at)
                                                
                                                embed.add_field(name=f"Health Bar" ,value=f"{player.name}\n  {player_healthbar}  {player_health}\n{character.name}\n  {character_healthbar} {character_health}")
                                                embed.add_field(name=f"{character.name} your turn.",value=f"Reply with \"**Attack**\" to attack , \"**Use**\" an item from your inventory or \"**End**\" to end the game",inline=False)
                                                embed.set_footer(icon_url= player.avatar_url,text=f"Attack executed by {player.name} • BB-9E ")    
                                                await ctx.send(embed=embed)
                                                return player_health,character_health,healables_uses_left
                                        #await ctx.send(f"Used **{item.names[0].title()}** and healed for {healed_amt} damage. Current health is {character_health}.\n You now have {healables_uses_left} uses of using a healable in this fight.Spend them wisely. ")
                                                        
                                    
                            elif msg.content.lower() in ["end","cancel","finish","quit","stop","exit","forefeit"]:
                            #await ctx.send(embed=discord.Embed(title =f"{character.name} wins!",description=f"{player.name} ended the game. lol what a wimp.",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Star Wars Bot ")) 
                                return "game end","game end","game end"
                            else:
                                await ctx.send(embed=discord.Embed(title =f"Invalid Option",description=f"Reply with \"**Attack**\" to attack , \"**Heal Healable-Name**\" to heal using Healables from your inventory or \"**End**\" to end the game",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= player.avatar_url,text=f"Requested by {player} • Star Wars Bot "))
                                player_health,character_health,healables_uses_left=await player_questions(player_health,character_health,healables_uses_left)
                                return player_health,character_health,healables_uses_left
                    
                    player_health,character_health,healables_uses_left=await player_questions(player_health,character_health,healables_uses_left)
                    if player_health== 0 or character_health == 0 :
                        player_healthbar,character_healthbar=self.healthbar_generator(player_health,character_health,max_player_health,max_character_health)
                        user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",player.id)
                        user_account=dict(user_account)
                        health_j=json.loads(user_account["health"])
                        if character_health==0:
                            earnings=random.choice(character.coins)
                            xp=int(character.xp)
                            embed=discord.Embed(title=f"**Game Ended**",description=f"{player.name} arose victorious!",color =random.choice(colourlist),timestamp=ctx.message.created_at)
                            embed.add_field(name=f"Health Bar" ,value=f"{player.name}\n  {player_healthbar}  {player_health}\n{character.name}\n  {character_healthbar} {character_health}")
                            embed.add_field(name=f"{player.name} you defeated {character.name}",value=f"You won and gained {earnings} coins and {xp} XP",inline=False)
                            health_j["health"]=player_health
                            player_health=json.dumps(health_j)
                            await connection.execute("UPDATE star_wars_table SET credits = $1 WHERE user_id=$2",int(user_account["credits"])+earnings,player.id)
                            await connection.execute("UPDATE star_wars_table SET xp = $1 WHERE user_id=$2",int(user_account["xp"])+xp,player.id)
                            await connection.execute("UPDATE star_wars_table SET health = $1 WHERE user_id=$2",player_health,player.id)
                        elif player_health==0:
                            earnings=0
                            xp=0
                            embed=discord.Embed(title=f"**Game Ended**",description=f"lol {character.name} won!",color =0xFD5151,timestamp=ctx.message.created_at)
                            embed.add_field(name=f"Health Bar" ,value=f"{player.name}\n  {player_healthbar}  {player_health}\n{character.name}\n  {character_healthbar} {character_health}")
                            embed.add_field(name=f"{character.name} defeated {player.name}",value=f"You lost and gained {earnings} coins and {xp} XP",inline=False)
                            await connection.execute("UPDATE star_wars_table SET credits = $1 WHERE user_id=$2",user_account["credits"]+earnings,player.id)
                            await connection.execute("UPDATE star_wars_table SET xp = $1 WHERE user_id=$2",user_account["xp"]+xp,player.id)
                            await connection.execute("UPDATE star_wars_table SET health = $1 WHERE user_id=$2",player_health,player.id)
                                    
                        embed.set_footer(icon_url= player.avatar_url,text=f"Attack executed by {player.name} • Star Wars Bot ")    
                        await ctx.send(embed=embed)
                        break
                    
                    elif player_health== "time out" or character_health == "time out":
                        xp= -20
                        earnings=0
                        embed=discord.Embed(title=f"**Fight Timed Out!**",color =random.choice(colourlist),timestamp=ctx.message.created_at)
                        embed.add_field(name=f"{player.name} took too much time and the game timed out",value=f"You lost and gained {earnings} coins and {xp} XP",inline=False)
                        health_j["health"]=player_health
                        player_health=json.dumps(health_j)
                        await connection.execute("UPDATE star_wars_table SET xp = $1 WHERE user_id=$2",int(user_account["xp"])+xp,player.id)
                        await connection.execute("UPDATE star_wars_table SET health = $1 WHERE user_id=$2",player_health,player.id)
                        break
                    elif player_health== "game end" or character_health == "game end":
                        earnings=0
                        xp= -50
                        embed=discord.Embed(title=f"**Fight forfeited**",color =random.choice(colourlist),timestamp=ctx.message.created_at)
                        embed.add_field(name=f"{player.name} surrendered",value=f"You lost and gained {earnings} coins and {xp} XP",inline=False)
                        health_j["health"]=player_health
                        player_health=json.dumps(health_j)
                        await connection.execute("UPDATE star_wars_table SET xp = $1 WHERE user_id=$2",int(user_account["xp"])+xp,player.id)
                        await connection.execute("UPDATE star_wars_table SET health = $1 WHERE user_id=$2",player_health,player.id)
                        break

    def healthbar_generator(self,player_health,character_health,max_player_health,max_character_health):
        #<a:YB_Red_HealthBar:785870856139702272>
        #<a:YB_Green_HealthBar:785870856172863490>
        #<a:YB_Orange_HealthBar:785870856370126848>
        #player_health_percentage=int((player_health/original_player_health)*100)
        player_health_percentage=int((player_health/max_player_health)*100)
        character_health_percentage=int((character_health/max_character_health)*100)

        if 4<=(player_health_percentage//10) <=7:
            player_healthbar="<a:YB_Orange_HealthBar:785870856370126848>" * (player_health_percentage//10)
        elif (player_health_percentage//10) <=3:
            player_healthbar="<a:YB_Red_HealthBar:785870856139702272>" * (player_health_percentage//10)
        else:
            player_healthbar="<a:YB_Green_HealthBar:785870856172863490>" * (player_health_percentage//10)
        
        if 4<=(character_health_percentage//10) <=7:
            character_healthbar="<a:YB_Orange_HealthBar:785870856370126848>" * (character_health_percentage//10)
        elif (character_health_percentage//10) <=3:
            character_healthbar="<a:YB_Red_HealthBar:785870856139702272>" * (character_health_percentage//10)
        else:
            character_healthbar="<a:YB_Green_HealthBar:785870856172863490>" * (character_health_percentage//10)
        
        return player_healthbar,character_healthbar
        


            # also see: conn.cursor, conn.fetch, conn.fetchrow, etc.

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Gamble", help='Gamble away your money')
    async def gamble(self,ctx,amt:int):
        user=ctx.author
        earnings=random.randint(-100,75)
        if amt<=0:
            await ctx.send(f"You can't gamble away zero or negative credits, dum-dum")
        elif amt<100:
            await ctx.send(f"Minimum Stakes is a 100 Imperial credits.")
        else:
            async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
                async with connection.transaction():
                    await self.create_account(ctx,user)
                    user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
                    if amt > user_account["credits"]:
                        await ctx.send("You can't gamble away what you don't have.")
                    else:
                        choice=random.choice(["lose","win"])
                        earnings=random.randint(0,100)
                        if choice=="lose":
                            total_earned=round(amt*(earnings/100))
                            bal=user_account["credits"]-total_earned
                            await ctx.send(f"You gambled away {amt} and lost {total_earned} credits with an {earnings}% decrease. New balance is {bal} credits ")
                        #elif choice=="win":
                        elif choice=="win":
                            total_earned=round(amt*(earnings/100))
                            bal=user_account["credits"]+total_earned
                            await ctx.send(f"You gambled away {amt} and earned {total_earned} credits with an {earnings}% increase. New balance is {bal} credits ")
                        else:
                            await ctx.send("error")

                        await connection.execute("UPDATE star_wars_table SET credits = $1 WHERE user_id=$2",bal,ctx.author.id)
                            
    @gamble.error
    async def gamble_error_handler(self, ctx, error):
        # Check if our required argument inp is missing.
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'amt':
                await ctx.send("You need to bet on something!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("You need to gamble credits. Not random stuff that comes to your head. Specify a whole number. ")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Beg", help='Beg for cash')
    async def beg(self,ctx):
        user=ctx.author
        earnings=random.randint(1,20)
      
        async with self.bot.pool.acquire() as connection:
        # create a transaction for that connection
            async with connection.transaction():
                await self.create_account(ctx,user)
                user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
                await connection.execute("UPDATE star_wars_table SET credits = $1 WHERE user_id=$2",user_account["credits"]+earnings,ctx.author.id)
                await ctx.send(f"Someone gave you {earnings} credits")
    

    @commands.cooldown(1,24*60*60, commands.BucketType.user)
    @commands.command(name="Daily", help='Daily bonus')
    async def daily_credits(self,ctx):
        user=ctx.author
        async with self.bot.pool.acquire() as connection:
        # create a transaction for that connection
            async with connection.transaction():
                await self.create_account(ctx,user)
                user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
                await connection.execute("UPDATE star_wars_table SET credits = $1 WHERE user_id=$2",user_account["credits"]+100,ctx.author.id)
                await ctx.send(f"You got your daily bonus of 100 credits. New balance is {user_account['credits']+100}")
        
    '''@commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Deposit",aliases=["dep"], help='Deposit all creditss stuff in xp')
    async def deposit(self,ctx,amt:int):
        user=ctx.author
        if amt<=0:
            await ctx.send(f"You can't withdraw zero or negative credits, dum-dum")
        else:        
            async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
                async with connection.transaction():
                    balance = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
                    if amt > balance["credits"]:
                        await ctx.send(f"You can't deposit what you don't have.")
                    else:
                        await connection.execute("UPDATE star_wars_table SET credits = $1 WHERE user_id=$2",balance["credits"]-amt,str(ctx.author.id))
                        await connection.execute("UPDATE star_wars_table SET xp = $1 WHERE user_id=$2",balance["xp"]+amt,str(ctx.author.id))
                        await ctx.send(f"You transfered {amt} credits into your xp")
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Withdraw",aliases=["wth"], help='Deposit all creditss stuff in xp')
    async def withdraw(self,ctx,amt:int):
        user=ctx.author
        if amt<=0:
            await ctx.send(f"You can't withdraw zero or negative credits, dum-dum")
        else:
            async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
                async with connection.transaction():
                    balance = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
                    if amt > balance["xp"]:
                        await ctx.send(f"You can't withdraw what you don't have.")
                    else:
                        await connection.execute("UPDATE star_wars_table SET credits = $1 WHERE user_id=$2",balance["credits"]+amt,str(ctx.author.id))
                        await connection.execute("UPDATE star_wars_table SET xp = $1 WHERE user_id=$2",balance["xp"]-amt,str(ctx.author.id))
                        await ctx.send(f"You withdrawed {amt} credits into your credits")'''
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Give", help='Deposit all creditss stuff in xp')
    async def give(self,ctx,user_mentioned:discord.Member,amt:int):
        user=ctx.author
        # if user.bot:
        #     await ctx.send(f"{user.name} is a bot. Bots don't have accounts.")
        # else:

        if amt<=0:
            await ctx.send(f"You can't give zero or negative credits, dum-dum")
        elif user==user_mentioned:
            await ctx.send(f"You can't give yourself the credits dum dum")
        elif user_mentioned.bot:
            await ctx.send(f"Bots don't have accounts dum dum.")
        else:
            async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
                async with connection.transaction():
                    await self.create_account(ctx,user)
                    await self.create_account(ctx,user_mentioned)
                    user_balance = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
                    user_mentioned_balance = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user_mentioned.id)
                    if amt > user_balance["credits"]:
                        await ctx.send(f"You can't give what you don't have.")
                    else:
                        await connection.execute("UPDATE star_wars_table SET credits = $1 WHERE user_id=$2",user_balance["credits"]-amt,user.id)
                        await connection.execute("UPDATE star_wars_table SET credits = $1 WHERE user_id=$2",user_mentioned_balance["credits"]+amt,user_mentioned.id)
                        await ctx.send(f"You gave {user_mentioned.name}, {amt} credits.")


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Inventory", help='Inventory of a user')
    async def inventory(self,ctx,user:discord.Member=None):
        user=user or ctx.author
        await self.create_account(ctx,user)

        if user.bot:
            await ctx.send(f"{user.name} is a bot. Bots don't have accounts.")
        else:
            # retrieve an individual connection from our pool, defined later
            async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
                async with connection.transaction():
                    user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
                    user_account=dict(user_account)
                    healables_j=json.loads(user_account["healables"])
                    weapons_j=json.loads(user_account["weapons"])
                    weapons_j_string,healables_j_string="",""
                    for item in weapons_j:
                        if item=="equipped":pass
                        elif weapons_j[item]==0:pass
                        else:
                            weapons_j_string= weapons_j_string + item.title() +" ("+ str(weapons_j[item]) +")"+ " \n"
                    for item in healables_j:
                        if healables_j[item]==0:pass
                        else:
                            healables_j_string= healables_j_string + item.title()  +" ("+str(healables_j[item])+")"+ " \n"
                    
                    if healables_j_string== "":
                        healables_j_string="You don't have any healables "
                        
                    embed=discord.Embed(title=f"{user.name}'s Inventory",color = random.choice(colourlist),timestamp=ctx.message.created_at)
                    embed.add_field(name="Healables:",value=f"{healables_j_string}",inline=False) 
                    embed.add_field(name="Weapons:",value=f"{weapons_j_string}",inline=False) 

                    author_avatar=ctx.author.avatar_url
                    embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Star Wars Bot ")
                    await ctx.send(embed=embed)



    async def create_account(self,ctx,user:discord.Member):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
                if user_account == None:
                    if user.bot:
                        await ctx.send(f"{user.name} is a bot. Bots don't need accounts.")

                    else: 
                        healables=json.dumps({"bandage": 0, "potion": 0, "fullheal": 0})
                        health=json.dumps({"health":100, "max_health":100})
                        weapons=json.dumps({'equipped':'','e-11 Blaster':1})

                    # create an account in star_wars_table
                        await connection.execute('INSERT INTO star_wars_table (user_id,credits,xp,health,weapons,healables) VALUES ($1,0,0,$2,$3,$4)',user.id,health,weapons,healables)

                else:
                    return
        
    

    

def setup(bot):
    bot.add_cog(Economy(bot))