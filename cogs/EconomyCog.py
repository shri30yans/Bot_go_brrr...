import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config

awards_list=[awards.Helpful_Award,awards.Wholesome_Award,awards.Silver_Award,awards.Gold_Award,awards.Platinum_Award,awards.Trinity_Award]
class Economy(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        #self.bot.loop.create_task(self.startup())#basically runs this function when bot is online and this cog is loaded

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Bal",aliases=["account","stats","karma","acc"], help='Balance of a user')
    async def bal(self,ctx,user:discord.Member=None):
        user=user or ctx.author
        if user.bot:
            await ctx.send(f"{user.name} is a bot. Bots don't have accounts.")
        else:
        # retrieve an individual connection from our pool, defined later
            async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
                async with connection.transaction():
                    await self.create_account(user)
                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                    user_account=dict(user_account)
                    embed=discord.Embed(title=f"{user.name}'s Balance")
                    embed.add_field(name="Balance:",value=f"{user_account['credits']} Credits")
                    embed.add_field(name="Karma:",value=f"{user_account['karma']} Karma")
                    embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
                    await ctx.send(embed=embed)

    async def startup(self):
        await self.bot.wait_until_ready()
        while True:
            ctx = await self.bot.fetch_channel(config.events_channel_id)
            await self.event(ctx)
            least_delay,max_delay=2,2*60# in hours
            time_interval=random.randint(least_delay*60,max_delay*60)#converts to seconds
            #time_interval=60
            await asyncio.sleep(time_interval)
    
    # @commands.is_owner()
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # @commands.command(name="Event",aliases=["events"],hidden=True)
    async def event(self,ctx):
        #user=ctx.author
        rarities_list=["Common","Uncommon","Rare","Epic","Legendary"]
        rarity=random.choices(rarities_list,weights=(40,30,15,10,5),k=1)[0]#k is the number of elements that can be choosen
        #rarity=random.choices(rarities_list,weights=(0,0,0,0,1),k=1)[0]
        #print(rarity)
        
        
        if rarity == 'Common':
            questions={
                "You are in an argument. Quick! Type `No You`.":["no you"],
                "Some one just said \"Hello there\". Quick! Type `General Kenobi`":["general kenobi"],
                "Someone just chopped their pp off! Quick! Give them a Wholesome Award. Send the Wholesome Award Emoji.": [config.reddit_award_wholesome],
                "POV: It's 2018 and you are Shri30yans Gaming. Quick say `Welcome to my Youtube Channel`": ['welcome to my youtube channel'],
                "Reddit just crashed the whole stock market. Quick say `Stonks`": ['stonks'],
                "POV: It's 2019 and Figet Spinners are Trending. Quick say `Fidget`": ['fidget'],
                #"I just  Type `wholesome`":"wholesome",
            }
            word=random.choice(list(questions))
            # print(word)
            # print(questions[word])
            sent_msg =await ctx.send(f"""**{rarity} Event Time!** \n{word}""")
            try:
                msg = await self.bot.wait_for('message', check=lambda m:(m.content.lower() in questions[word]), timeout=180.0)

            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(title ="Timed Out!",description=f"None of you answered on time!",color = self.bot.user.color).set_footer(icon_url= self.bot.user.avatar_url,text=f" • {self.bot.user.name} "))
            
            else:
                user=msg.author
                amt=random.randint(10,20)
                await ctx.send(f"{user.mention} wins {amt} credits for answering first!")
                await self.create_account(user)
                await self.add_credits(user=user,amt=amt)
                await sent_msg.edit(content=f"{sent_msg.content}\n\n This event is expired. No new submissions will be accepted")
            
        
        
        elif rarity == 'Uncommon':
            questions={"Don't underestimate my _____":"power",
            "I find your lack of _____ disturbing.":"faith",
            "In my experience there is no such thing as ____.":"luck",
            "The fear of ____ is a path to the dark side.":"loss",
            "I was in VC with my ___":"bsf"
            }
            word=random.choice(list(questions))
            # print(word)
            # print(questions[word])
            sent_msg =await ctx.send(f"""**{rarity} Event!**\nWrite the fill the missing part of this sentence. Quick! Fastest person wins! \n*{word}*""")
            try:
                msg = await self.bot.wait_for('message', check=lambda m:(m.content.lower() == questions[word].lower()), timeout=180.0)

            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(title ="Timed Out!",description=f"None of you answered on time!",color = self.bot.user.color).set_footer(icon_url= self.bot.user.avatar_url,text=f" • {self.bot.user.name} "))
            
            else:
                user=msg.author
                amt=random.randint(20,40)
                await ctx.send(f"{user.mention} wins {amt} credits! The missing word was `{questions[word]}`")
                await self.create_account(user)
                await self.add_credits(user=user,amt=amt)
                await sent_msg.edit(content=f"{sent_msg.content}\n\n This event is expired. No new submissions will be accepted")



        elif rarity == 'Rare':
            questions=["panzer IV","jalapenos","send nudes","takes shit off","dead chat"]
            word=random.choice(questions)
            shuffled_words = ""
            word_list=word.split(" ")
            for x in word_list:
                x=list(x)
                random.shuffle(x)
                shuffled_words = shuffled_words + "".join(x) + " "  
            sent_msg = await ctx.send(f"""**{rarity} Event!**\nUnscramble the words and type them below. Fastest person to type `{shuffled_words}` wins.""")
            try:
                msg = await self.bot.wait_for('message', check=lambda m:(m.content.lower() == word.lower()), timeout=180.0)

            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(title ="Timed Out!",description=f"None of you answered on time!",color = self.bot.user.color).set_footer(icon_url= self.bot.user.avatar_url,text=f" • {self.bot.user.name} "))
            
            else:
                user=msg.author
                amt=random.randint(40,70)
                await ctx.send(f"{user.mention} wins {amt} credits! The word was `{word}`")
                await self.create_account(user)
                await self.add_credits(user=user,amt=amt) 
                await sent_msg.edit(content=f"{sent_msg.content}\n\n This event is expired. No new submissions will be accepted")

        
        
        elif rarity == 'Epic':
            questions={"Hottest Star Wars Character?":['obi-wan kenobi','kenobi','obi wan','obi-wan','obi wan kenobi',],
                        "Some one just threw something really far. What are they supposed to say?":["yeet","yeet!"],
                        "Hottest Harry Potter Character? Go!":['hagrid'],}
            word=random.choice(list(questions))

            sent_msg = await ctx.send(f"""**{rarity} Event!**\n{word} First person to answer wins!""")

            try:
                msg = await self.bot.wait_for('message', check=lambda m:(m.content.lower() in questions[word]), timeout=180.0)

            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(title ="Timed Out!",description=f"None of you answered on time!",color = self.bot.user.color).set_footer(icon_url= self.bot.user.avatar_url,text=f" • {self.bot.user.name} "))
            
            else:
                user=msg.author
                amt=random.randint(80,100)
                await ctx.send(f"{user.mention} wins {amt} credits! The answer was `{questions[word][0].capitalize()}`")
                await self.create_account(user)
                await self.add_credits(user=user,amt=amt)
                await sent_msg.edit(content=f"{sent_msg.content}\n\n This event is expired. No new submissions will be accepted")

        
        elif rarity == 'Legendary':
            questions={"https://i.imgur.com/HBUtYuZ.jpg":['this is fine','this is fine.'],
                        "https://i.imgur.com/IyX19td.png":["stonks"],
                        "https://i.imgur.com/2B85WEe.png":['aight imma head out','ight imma head out','alright imma head out'],
                        "https://i.imgur.com/awn4TlW.png":['where banana'],
                        "https://i.imgur.com/4OIx1l4.jpg?1":["same","y same"]}
            word=random.choice(list(questions))

            sent_msg =await ctx.send(f"""**{rarity} Event!** \nEnter the words associated with this meme template.""")
            await ctx.send(f"""{word}""")
            
            try:
                msg = await self.bot.wait_for('message', check=lambda m:(m.content.lower() in questions[word]), timeout=180.0)

            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(title ="Timed Out!",description=f"None of you answered on time!",color = self.bot.user.color).set_footer(icon_url= self.bot.user.avatar_url,text=f" • {self.bot.user.name} "))
            
            else:
                user=msg.author
                amt=random.randint(100,150)
                await ctx.send(f"{user.mention} wins {amt} credits! The answer was {questions[word][0].capitalize()}")
                await self.create_account(user)
                await self.add_credits(user=user,amt=amt)
                await sent_msg.edit(content=f"{sent_msg.content}\n\n This event is expired. No new submissions will be accepted")
        
        else:
            await ctx.send("You should never see this message")

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(name="Beg", help='Beg for cash')
    async def beg(self,ctx):
        user=ctx.author
        amt=random.randint(1,20)
        await self.create_account(user)
        await self.add_credits(user=ctx.message.author,amt=amt)
        await ctx.send(f"Someone gave you {amt} credits")


    #async def create_account(self,ctx,user:discord.Member):
    async def create_account(self,user:discord.Member):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                if user_account == None:
                    if user.bot:pass
                        #await ctx.send(f"{user.name} is a bot. Bots don't need accounts.")
                    else: 
                    # create an account                  
                        await connection.execute('INSERT INTO info (user_id,credits,karma) VALUES ($1,0,0)',user.id)


                else:
                    return
    
    async def add_karma(self,user,amt):
        #user=ctx.author
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():

                if user.bot:
                    return
                else: 
                    await self.create_account(user)

                user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                await connection.execute("UPDATE info SET karma = $1 WHERE user_id=$2",user_account["karma"]+amt,user.id)

    async def add_credits(self,user,amt):
        #user=ctx.author
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():

                if user.bot:
                    return
                else: 
                    await self.create_account(user)

                user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                await connection.execute("UPDATE info SET credits = $1 WHERE user_id=$2",user_account["credits"]+amt,user.id)
                #await ctx.send(f"Someone gave you {earnings} credits")


# _____                _       
# |  ___|              | |      
# | |____   _____ _ __ | |_ ___ 
# |  __\ \ / / _ \ '_ \| __/ __|
# | |___\ V /  __/ | | | |_\__ \
# \____/ \_/ \___|_| |_|\__|___/
      
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return

        elif message.channel.id==config.suggestions_channel_id:
            await message.add_reaction(config.upvote_reaction)
            await message.add_reaction(config.downvote_reaction)

        elif message.channel.id==config.meme_channel_id and len(message.attachments) !=0:
            await message.add_reaction(config.upvote_reaction)
            await message.add_reaction(config.downvote_reaction)

        # else:
        #     return

        # if "Stonks".lower() in message.content.lower():
        #     amt= random.randint(300,100)
        #     await self.add_karma(user=message.author,amt=amt)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):  
        channel=self.bot.get_channel(payload.channel_id) 
        user=self.bot.get_user(payload.user_id)
        message= await channel.fetch_message(payload.message_id)
        emoji=payload.emoji  
        
        if user.bot:#if reaction is by a bot
            return
        
        if str(emoji) == config.upvote_reaction and message.author != user:
            amt = random.randint(0,2)
            await self.add_karma(user=message.author,amt=amt)

        elif str(emoji) == config.downvote_reaction and message.author != user:
            amt = random.randint(-3,-1)
            await self.add_karma(user=message.author,amt=amt)

        #if any post has 10 or more upvotes, award that posts author 100 credits
        all_reacts=message.reactions
        for reaction in all_reacts:
            if str(emoji) == config.upvote_reaction and reaction.count >= 10:
                amt=100
                await self.add_credits(user=message.author,amt=amt)
                return


        # upvote_limit = 8
        # downvote_limit = 5
        # #in Suggestions channel
        # if channel.id == config.suggestions_channel_id:
        #     all_reacts=message.reactions
        #     for reaction in all_reacts:
        #         if str(reaction) == config.upvote_reaction and reaction.count >= upvote_limit+1:
        #             pass
        #         if str(reaction) == config.downvote_reaction and reaction.count >= downvote_limit+1:
        #             await reaction.message.delete()
        
        # else:
        # if reaction.message.author == user: #return #self upvote

        for award in awards_list:
            if str(emoji) == award.reaction_id:
                async with self.bot.pool.acquire() as connection:
                    async with connection.transaction():
                        await self.create_account(user)
                        user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                        user_account=dict(user_account)
                        if user_account["credits"] < award.cost:
                            await message.remove_reaction(emoji, user)
                            await message.channel.send("You don't have enough credits to buy this award. Try earning some credits first",delete_after=5)
                        
                        else:
                            if user == message.author:
                                await message.remove_reaction(emoji, user)
                                await channel.send("Awarding yourself? You seriously aren't that desperate, are you?")
                                return
                            elif message.author.bot:
                                await message.remove_reaction(emoji, user)
                                await channel.send("Awarding bots? Sorry no can do.")
                                return
                            else:

                                embed = discord.Embed(title=f"{user.name}, Give {award.name} award to {message.author.name}?",description="React with ✅ to give the award and ❌ to not give it.",color = 0xFFD700)
                                embed.add_field(name="Note:",value="An award cannot be revoked, once given. The reaction can be removed, but that would not remove the award. \n This action is irreversible. \n Credits cannot be refunded.")
                                embed.set_thumbnail(url=str(emoji.url))
                                embed.set_footer(icon_url= user.avatar_url,text=f"Requested by {message.author} • {self.bot.user.name} ")
                                check_message=await message.channel.send(embed=embed)
                                await check_message.add_reaction('✅')
                                await check_message.add_reaction('❌')
                                
                                def check_accept_or_reject(confirm_reaction,confirm_user):
                                    return str(confirm_reaction.emoji) in ['✅', '❌'] and user == confirm_user

                                try:
                                    confirm_reaction,confirm_user = await self.bot.wait_for('reaction_add',check=check_accept_or_reject, timeout=60)

                                except asyncio.TimeoutError:
                                    await check_message.edit(embed=discord.Embed(title="Timeout!",description=f"{user.mention}, did not react after 60 seconds. Award is forfeited.",color = 0xFFD700))

                                else:
                                    if str(confirm_reaction.emoji) == '✅':
                                        await check_message.delete()
                                        await message.channel.send(f"{user.mention} gave {message.author.mention} a {award.name} award.")
                                        embed = discord.Embed(title=f"You recieved an {award.name} Award!",description=f"{user.mention} liked your [post]({message.jump_url}) so much that the gave it the {award.name} award.",color = 0xFFD700)
                                        embed.set_thumbnail(url=str(emoji.url))
                                        embed.set_footer(icon_url= user.avatar_url,text=f"Given by {message.author} • {self.bot.user.name} ")
                                        try:await message.author.send(embed=embed)
                                        except:pass

                                        await self.add_karma(user=message.author,amt=award.karma_given_to_receiver)
                                        await self.add_karma(user=user,amt=award.karma_given_to_giver)
                                        await self.add_credits(user=user,amt = -award.cost)

                                    
                                    elif str(confirm_reaction.emoji) == '❌':
                                        await check_message.delete()
                                        await message.remove_reaction(emoji, user)
                                        await message.channel.send("Award was cancelled.",delete_after=5)
                                    else:
                                        await message.channel.send("Well, you should not be able to see this. Something went wrong")
   
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):  
        channel=self.bot.get_channel(payload.channel_id) 
        user=self.bot.get_user(payload.user_id)
        message= await channel.fetch_message(payload.message_id)
        emoji=payload.emoji  
        if user.bot:#if reaction is by a bot
            return

        if str(emoji) == config.upvote_reaction and message.author != user:
            amt = random.randint(-3,-1)
            await self.add_karma(user=message.author,amt=amt)

        elif str(emoji) == config.downvote_reaction and message.author != user:
            amt = random.randint(0,2)
            await self.add_karma(user=message.author,amt=amt)
                
    
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # @commands.command(name="Beg", help='Beg for cash')
    # async def beg(self,ctx):
    #     user=ctx.author
    #     earnings=random.randint(1,20)
      
    #     async with self.bot.pool.acquire() as connection:
    #     # create a transaction for that connection
    #         async with connection.transaction():
    #             await self.create_account(ctx,user)
    #             user_account = await connection.fetchrow("SELECT * FROM star_wars_table WHERE user_id=$1",user.id)
    #             await connection.execute("UPDATE star_wars_table SET credits = $1 WHERE user_id=$2",user_account["credits"]+earnings,ctx.author.id)
    #             await ctx.send(f"Someone gave you {earnings} credits")
    

def setup(bot):
    bot.add_cog(Economy(bot))
        