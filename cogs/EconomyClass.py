import os, sys, discord, platform, random, aiohttp, json,time,asyncio
from discord.ext import commands,tasks
from discord.ext.commands import Greedy
from discord.ext.commands.cooldowns import BucketType
import asyncpg


colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
            0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Balance",aliases=["bal"], help='Balance of a user')
    async def bal(self,ctx,user:discord.Member=None):
        user=user or ctx.author
        if user.bot:
            await ctx.send(f"{user.name} is a bot. Bots don't have accounts.")
        else:
    # retrieve an individual connection from our pool, defined later
            async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
                async with connection.transaction():
                    user_account = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                    if user_account ==None:
                        await self.create_account(ctx,user)
                        user_account  = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                    user_account=dict(user_account)
                    embed=discord.Embed(Title=f"{ctx.author.name}'s Statistics")
                    embed.add_field(name="Imperial Credits:",value=f"{user_account['credits']} credits")
                    #embed.add_field(name="XP:",value=f"{user_account['xp']} ",inline=True)
                    embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                    await ctx.send(embed=embed)
   
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Explore",aliases=["exp"], help='Explore a region to earn quick cash ')
    async def Search(self,ctx):
        user=ctx.author
    # retrieve an individual connection from our pool, defined later
        async with self.bot.pool.acquire() as connection:
        # create a transaction for that connection
            async with connection.transaction():
                user_account = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                if user_account ==None:
                    await self.create_account(ctx,user)
                    user_account  = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                user_account=dict(user_account)
                choices =random.sample([{"Forest":""},{"Swamp":""},{"Hills":""},{"Wilderness":""},{"Cave":""},{"Volcano":""},{"Dungeons":""},{"Future":""},{"Sewer":""}],k=3)
                location_names,location_activity = [] ,[]
                for location in choices : 
                    #extend appends all the elements of a list L1 to a list L2
                    location_names.extend(location) 
                for location in choices : 
                    location_activity.extend(location.values()) 
                
                earnings=random.randint(1,30)
                await ctx.send(f"What would you like to explore? **{location_names[0]}**, **{location_names[1]}** or **{location_names[2]}**. Enter a location below:")
                
                try:
                    msg = await self.bot.wait_for('message', check=lambda m:(m.author==ctx.author and m.content.lower().capitalize() in location_names), timeout=30.0)
                except asyncio.TimeoutError:
                    await ctx.send(embed=discord.Embed(title ="Explore command Timed Out!",description=f"{ctx.author.name} took too much time and didn't reply.",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
                else:
                    if msg.content==location_names[0]:
                        await ctx.send(f"You explored {location_names[0]} and found {earnings} credits.")
                    elif msg.content==location_names[1]:
                        await ctx.send(f"You explored {location_names[1]} and found {earnings} credits.")
                    elif msg.content==location_names[0]:
                        await ctx.send(f"You explored {location_names[2]} and found {earnings} credits.")
                await connection.execute("UPDATE rpgdatabase SET credits = $1 WHERE user_id=$2",user_account["credits"]+earnings,ctx.author.id)



                #embed=discord.Embed(Title=f"{ctx.author.name}'s Statistics")
                #embed.add_field(name="credits:",value=f"{user_account['credits']} credits")
                #embed.add_field(name="XP:",value=f"{user_account['xp']} ",inline=True)
                #embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                #await ctx.send(embed=embed)

    '''async def fight(self,ctx):
            challenger=ctx.author
            challenged=mentioned_user
            challenger_health=100
            challenger_damage_done=0

            choices = ["attack","heal","end"]
            if len(challenger.name)>=len(challenged.name):
                max_length_of_player_names=len(challenger.name)
            else:
                max_length_of_player_names=len(challenged.name)

                    
                while challenger_health>0 and challenged_health>0:
                
                    #---------------------------------------------------------------------------------------
                    #Challenger
                    #---------------------------------------------------------------------------------------
                    #challenger_msg=await ctx.send(embed=discord.Embed(title =f"{challenger.name} your turn.",description=f"Reply with \"**Attack**\" to attack , \"**Heal**\" to heal , \"**Special**\" for a Special Attack or \"**End**\" to end the game"",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_thumbnail(url=str(challenger.avatar_url)).set_footer(icon_url= challenger.avatar_url,text=f"Turn of {challenger.name} • Yeet Bot "))
                    
                    async def challenger_questions(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done):
                        try:
                            msg = await self.bot.wait_for('message', check=lambda m:(m.author==challenger and m.content.lower() in choices), timeout=60.0)
                        except asyncio.TimeoutError:
                            await ctx.send(embed=discord.Embed(title ="Game Timed Out!",description=f"{challenger.name} took too much time and has forfeited the game. {challenged.name} wins!",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
                            return -1,-1,-1,-1
                        else:
                            if msg.content.lower() == 'attack'
                                damage_attack=random.choice(damage_attacks)
                                damage=random.randint(1,40)
                                challenged_health=max(challenged_health-damage,0)
                                challenger_damage_done=challenger_damage_done+damage
                                challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
                                embed=discord.Embed(title=f"**{challenger.name} attacked!**",color =0xFD5151,timestamp=ctx.message.created_at)
                                embed.add_field(name=f"**{damage_attack.format(challenger.name,challenged.name)}, dealing {damage} damage.**" ,value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack: {challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done}") 
                                embed.add_field(name=f"{challenged.name} your turn.",value=f"Reply with \"**Attack**\" to attack , \"**Heal**\" to heal , \"**Special**\" for a Special Attack or \"**End**\" to end the game",inline=False)
                                embed.set_footer(icon_url= challenger.avatar_url,text=f"Attack executed by {challenger.name} • Yeet Bot ")    
                                await ctx.send(embed=embed)
                            
                                
                            elif msg.content.lower() == 'end':
                                await ctx.send(embed=discord.Embed(title =f"{challenged.name} wins!",description=f"{challenger.name} ended the game. lol what a wimp.",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
                                return -1,-1,-1,-1

                            elif msg.content.lower() == 'heal':
                                if challenger_health==100:
                                    embed = discord.Embed(title=f"**{challenger.name} you are already at full health!**",color = random.choice(colourlist))
                                    embed.add_field(name=f"**{challenger.name} 100 is the Maximum Health, dum-dum**",value=f"Please choose another option. Reply with \"**Attack**\" or \"**Special**\" or \"**End**\" to end the game",inline=False)
                                    embed.set_footer(icon_url=challenger.avatar_url,text=f"Heal not executed by {challenger.name} • Yeet Bot ")
                                    challenger_health,challenged_health,challenger_damage_done,challenged_damage_done=await challenger_questions(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
                                    await ctx.send(embed=embed)
                                    
                                else:    
                                    heal=random.randint(1,30)
                                    challenger_health=min(challenger_health+heal, 100)
                                    challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
                                    embed=discord.Embed(title=f"**{challenger.name} healed!**",color = 0x5AFF00,timestamp=ctx.message.created_at)
                                    embed.add_field(name=f"**{challenger.name} healed {heal}**",value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack: {challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done}") 
                                    embed.add_field(name=f"{challenged.name} your turn.",value=f"Reply with \"**Attack**\" to attack , \"**Heal**\" to heal , \"**Special**\" for a Special Attack or \"**End**\" to end the game",inline=False)
                                    embed.set_footer(icon_url= challenger.avatar_url,text=f"Heal executed by {challenger.name} • Yeet Bot ")   
                                await ctx.send(embed=embed)
                                return challenger_health,challenged_health,challenger_damage_done,challenged_damage_done
                            
                            


                    challenger_health,challenged_health=await challenger_questions(challenger_health,challenged_health)
                    if challenger_health==-1:
                        break
                    
                    if challenger_health<=0 or challenged_health<=0:
                        break
    def healthbar_generator(self,challenger_health,challenged_health,challenger_damage_done,challenged_damage_done):
        #<a:YB_Red_HealthBar:785870856139702272>
        #<a:YB_Green_HealthBar:785870856172863490>
        #<a:YB_Orange_HealthBar:785870856370126848>
        if 4<=(challenger_health // 10) <=7:
            challenger_healthbar="<a:YB_Orange_HealthBar:785870856370126848>" * (challenger_health // 10)
        elif (challenger_health // 10) <=3:
            challenger_healthbar="<a:YB_Red_HealthBar:785870856139702272>" * (challenger_health // 10)
        else:
            challenger_healthbar="<a:YB_Green_HealthBar:785870856172863490>" * (challenger_health // 10)
        
        if 4<=(challenged_health // 10) <=7:
            challenged_healthbar="<a:YB_Orange_HealthBar:785870856370126848>" * (challenged_health // 10)
        elif (challenged_health // 10) <=3:
            challenged_healthbar="<a:YB_Red_HealthBar:785870856139702272>" * (challenged_health // 10)
        else:
            challenged_healthbar="<a:YB_Green_HealthBar:785870856172863490>" * (challenged_health // 10)
        
        
        return challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar'''


            # also see: conn.cursor, conn.fetch, conn.fetchrow, etc.

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Gamble", help='Gamble away your money')
    async def gamble(self,ctx,amt:int):
        user=ctx.author
        earnings=random.randint(-100,75)
        if amt<=0:
            await ctx.send(f"You can't gamble away zero or negative credits, dum-dum")
        else:
            async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
                async with connection.transaction():
                    choice=random.choice(["lose","win"])
                    earnings=random.randint(0,100)
                    if choice=="lose":
                        total_earned=round(amt*(earnings/100))
                    #elif choice=="win":
                    else:
                        total_earned=round(amt*(earnings/100))
                    user_account = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                    if user_account==None:
                        await self.create_account(ctx,user)
                    bal=user_account["credits"]+total_earned
                    #if user_account==None:
                        #self.create_account(user)
                        #user_account = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                    if amt > user_account["credits"]:
                        await ctx.send("You can't gamble away what you don't have")
                    else:
                        await connection.execute("UPDATE rpgdatabase SET credits = $1 WHERE user_id=$2",bal,ctx.author.id)
                        await ctx.send(f"You gambled away {amt} and earned {total_earned} credits with an {earnings}% increase. New balance is {bal} credits ")
    
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
        earnings=random.randint(1,30)
      
        async with self.bot.pool.acquire() as connection:
        # create a transaction for that connection
            async with connection.transaction():
                user_account = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                if user_account==None:
                    await self.create_account(ctx,user)
                    user_account = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                await connection.execute("UPDATE rpgdatabase SET credits = $1 WHERE user_id=$2",user_account["credits"]+earnings,ctx.author.id)
                await ctx.send(f"Someone gave you {earnings} credits")
    

    @commands.cooldown(1,24*60*60, commands.BucketType.user)
    @commands.command(name="Daily", help='Daily bonus')
    async def daily_credits(self,ctx):
        user=ctx.author
        async with self.bot.pool.acquire() as connection:
        # create a transaction for that connection
            async with connection.transaction():
                user_account = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                if user_account==None:
                    await self.create_account(ctx,user)
                    user_account = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                await connection.execute("UPDATE rpgdatabase SET credits = $1 WHERE user_id=$2",user_account["credits"]+100,ctx.author.id)
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
                    balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                    if amt > balance["credits"]:
                        await ctx.send(f"You can't deposit what you don't have.")
                    else:
                        await connection.execute("UPDATE rpgdatabase SET credits = $1 WHERE user_id=$2",balance["credits"]-amt,str(ctx.author.id))
                        await connection.execute("UPDATE rpgdatabase SET xp = $1 WHERE user_id=$2",balance["xp"]+amt,str(ctx.author.id))
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
                    balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                    if amt > balance["xp"]:
                        await ctx.send(f"You can't withdraw what you don't have.")
                    else:
                        await connection.execute("UPDATE rpgdatabase SET credits = $1 WHERE user_id=$2",balance["credits"]+amt,str(ctx.author.id))
                        await connection.execute("UPDATE rpgdatabase SET xp = $1 WHERE user_id=$2",balance["xp"]-amt,str(ctx.author.id))
                        await ctx.send(f"You withdrawed {amt} credits into your credits")'''
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Give", help='Deposit all creditss stuff in xp')
    async def give(self,ctx,user_mentioned:discord.Member,amt:int):
        user=ctx.author

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
                    user_balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                    user_mentioned_balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user_mentioned.id)
                    if user_balance==None:
                        await self.create_account(ctx,user)
                        user_balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                    if user_mentioned_balance==None:
                        await self.create_account(ctx,user)
                        user_balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user_mentioned.id)

                    if amt > user_balance["credits"]:
                        await ctx.send(f"You can't give what you don't have.")
                    else:
                        await connection.execute("UPDATE rpgdatabase SET credits = $1 WHERE user_id=$2",user_balance["credits"]-amt,user.id)
                        await connection.execute("UPDATE rpgdatabase SET credits = $1 WHERE user_id=$2",user_mentioned_balance["credits"]+amt,user_mentioned.id)
                        await ctx.send(f"You gave {user_mentioned.name}, {amt} credits.")


    '''@commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Inventory", help='Inventory of a user')
    async def inventory(self,ctx,user:discord.Member=None):
        user=user or ctx.author
        async with self.bot.pool.acquire() as connection:
        # create a transaction for that connection
            async with connection.transaction():
                balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                #inventory = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                balance,xp
                
                
                balance=dict(balance)
                credits_amt=balance["credits"]
                xp_amt=balance["xp"]
                inventory_items=inventory

                embed=discord.Embed(Title=f"{ctx.author.name}'s balance")
                embed.add_field(name="credits:",value=f"{credits_amt} ")
                embed.add_field(name="xp:",value=f"{xp_amt} ")
                embed.add_field(name="Inventory:",value=f"{inventory_items} ")
                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed)'''

    async def create_account(self,ctx,user:discord.Member):
        async with self.bot.pool.acquire() as connection:
            if user.bot:
                await ctx.send(f"{user.name} is a bot. Bots don't need accounts.")

            else: 
            # create a transaction for that connection
                async with connection.transaction():
                    await connection.execute("INSERT INTO rpgdatabase (user_id,credits,xp,health) VALUES ($1,0,0,100,)",user.id)
        
    

    

def setup(bot):
    bot.add_cog(Economy(bot))