import discord,random,aiohttp,json,time,asyncio
from discord.ext import commands,tasks
import utils.awards as awards
import config   
from datetime import datetime 
import pytz 

colourlist=config.embed_colours

    
class Events(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        # run this function when this cog is loaded (which program is started)
        self.bot.loop.create_task(self.startup())

    async def check_if_time_is_ok(self):
        # it will get the time zone of the specified location 
        IST = pytz.timezone('Asia/Kolkata') 

        datetime_ist = datetime.now(IST) 
        hour = datetime_ist.hour
        if hour > 23 or hour < 10:#if time between 12 AM and 10 AM
            return False
        else:
            return True


    async def startup(self):
        if config.run_event: #Boolean
            await self.bot.wait_until_ready()
            while True:
                time_check = await self.check_if_time_is_ok()
                if time_check:    
                    ctx = await self.bot.fetch_channel(config.events_channel_id)
                    await self.event(ctx)
                least_delay,max_delay=10,2*60# in miutes
                time_interval=random.randint(least_delay*60,max_delay*60)#converts to seconds
                #time_interval=60
                await asyncio.sleep(time_interval)
    
    @commands.is_owner()
    @commands.command(name="Event",aliases=["events"],hidden=True)
    async def event(self,ctx,rarity="Random"):
        #user=ctx.author
        rarities_list=["Common","Uncommon","Rare","Epic","Legendary"]
        if rarity == "Random":
            #k is the number of elements that can be choosen
            rarity=random.choices(rarities_list,weights=(40,30,15,10,5),k=1)[0]
        
        elif rarity.lower().capitalize() in rarities_list:
            rarity=rarity.lower().capitalize()
        
        else:
            await ctx.send("Enter a proper rarity. (Common, Uncommon, Rare, Epic, Legendary).")
          
        if rarity == 'Common':
            questions={
                "You are in an argument. Quick! Type `No You`.":["no you"],
                "POV: Someone just replied \"General Kenobi\" to a \"Hello there\". Quick! Type `This is the Way`":["this is the way"],
                "Someone just sent a rad meme in the chat. Quick! Type `kek` ": ['kek',],
                "PS5 just came in stock. Quick say `Add to cart`": ['add to cart'],
                "I just died playing Minecraft. Type `F` in the chat": ['f'],
                "People are lurking in chat. Send this emoji (🕵️) ": ['🕵️'],
                "POV: You are Tahir. Quick send this emoji in the chat (😹)":['😹'],
            }
            word=random.choice(list(questions))
            # print(word)
            # print(questions[word])
            sent_msg =await ctx.send(f"""**{rarity} Event Time!** \n{word}""")
            try:
                msg = await self.bot.wait_for('message', check=lambda m:(m.content.lower() in questions[word]), timeout=300)#timeout after 5 mins

            except asyncio.TimeoutError:
                await sent_msg.delete()
                #await ctx.send(embed=discord.Embed(title ="Timed Out!",description=f"None of you answered on time!",color = self.bot.user.color).set_footer(icon_url= self.bot.user.avatar_url,text=f" • {self.bot.user.name} "))
            
            else:
                user=msg.author
                amt=random.randint(10,20)
                await ctx.send(f"{user.mention} wins {amt} credits for answering first!")
                await sent_msg.edit(content=f"{sent_msg.content}\n\n This event is expired. No new submissions will be accepted")
            
        
        
        elif rarity == 'Uncommon':
            questions={
            "Weaklings die ___  ___":"big deal",
            "The ability to ___ does not make you intelligent.":"speak",
            "In my experience there is no such thing as ___.":"luck",
            "Difficult to see; always in motion is the ___.":"future",
            "Only a Sith deals in  ___":"absolutes",
            "There’s always a bigger ___.":"fish",
            "So this is how liberty dies … with thunderous ___.":"applause",

            }
            word=random.choice(list(questions))
            # print(word)
            # print(questions[word])
            sent_msg =await ctx.send(f"""**{rarity} Event!**\nWrite the fill the missing part of this sentence. Quick! Fastest person wins! \n*{word}*""")
            try:
                msg = await self.bot.wait_for('message', check=lambda m:(m.content.lower() == questions[word].lower()), timeout=180.0)

            except asyncio.TimeoutError:
                await sent_msg.delete()
                #await ctx.send(embed=discord.Embed(title ="Timed Out!",description=f"None of you answered on time!",color = self.bot.user.color).set_footer(icon_url= self.bot.user.avatar_url,text=f" • {self.bot.user.name} "))
            
            else:
                user=msg.author
                amt=random.randint(20,40)
                await ctx.send(f"{user.mention} wins {amt} credits! The missing word was `{questions[word]}`")
                await sent_msg.edit(content=f"{sent_msg.content}\n\n This event is expired. No new submissions will be accepted")



        elif rarity == 'Rare':
            questions=["stonks","minecraft","talented mf","ender dragon","diamond armour","ding ding",]
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
                await sent_msg.delete()
                #await ctx.send(embed=discord.Embed(title ="Timed Out!",description=f"None of you answered on time!",color = self.bot.user.color).set_footer(icon_url= self.bot.user.avatar_url,text=f" • {self.bot.user.name} "))
            
            else:
                user=msg.author
                amt=random.randint(40,70)
                await ctx.send(f"{user.mention} wins {amt} credits! The word was `{word}`")
                await sent_msg.edit(content=f"{sent_msg.content}\n\n This event is expired. No new submissions will be accepted")

        
        
        elif rarity == 'Epic':
            questions={"What is the name of the Internet meme consisting of a green anthropomorphic frog with a humanoid body originated in a 2005 comic?":['pepe','pepe the frog',],
                        "What is the name of the Internet meme of a picture of a Shiba Inu dog that became popular in 2013? ":["doge"],
                        "Who is the famous Pixar character featured in the two-eyed green spherical monster meme staring awkwardly? ":['mike wazowski'],}
            word=random.choice(list(questions))

            sent_msg = await ctx.send(f"""**{rarity} Event!**\n{word} First person to answer wins!""")

            try:
                msg = await self.bot.wait_for('message', check=lambda m:(m.content.lower() in questions[word]), timeout=180.0)

            except asyncio.TimeoutError:
                await sent_msg.delete()
                #await ctx.send(embed=discord.Embed(title ="Timed Out!",description=f"None of you answered on time!",color = self.bot.user.color).set_footer(icon_url= self.bot.user.avatar_url,text=f" • {self.bot.user.name} "))
            
            else:
                user=msg.author
                amt=random.randint(80,100)
                await ctx.send(f"{user.mention} wins {amt} credits! The answer was `{questions[word][0].capitalize()}`")
                await sent_msg.edit(content=f"{sent_msg.content}\n\n This event is expired. No new submissions will be accepted")

        
        elif rarity == 'Legendary':
            questions={"https://i.imgur.com/HBUtYuZ.jpg":['this is fine','this is fine.'],
                        "https://i.imgur.com/IyX19td.png":["stonks"],
                        "https://i.imgur.com/2B85WEe.png":['aight imma head out','ight imma head out','alright imma head out'],
                        "https://i.imgur.com/awn4TlW.png":['where banana'],
                        "https://i.imgur.com/4OIx1l4.jpg?1":["same","y same"],
                        "https://i.imgur.com/RG2zL0G.jpg":["is this a pigeon?","is this a pigeon"]}
            word=random.choice(list(questions))

            sent_msg =await ctx.send(f"""**{rarity} Event!** \nEnter the words associated with this meme template.""")
            await ctx.send(f"""{word}""")
            
            try:
                msg = await self.bot.wait_for('message', check=lambda m:(m.content.lower() in questions[word]), timeout=180.0)

            except asyncio.TimeoutError:
                await sent_msg.delete()
                #await ctx.send(embed=discord.Embed(title ="Timed Out!",description=f"None of you answered on time!",color = self.bot.user.color).set_footer(icon_url= self.bot.user.avatar_url,text=f" • {self.bot.user.name} "))
            
            else:
                user=msg.author
                amt=random.randint(100,150)
                await ctx.send(f"{user.mention} wins {amt} credits! The answer was `{questions[word][0].capitalize()}`")
                await sent_msg.edit(content=f"{sent_msg.content}\n\n This event is expired. No new submissions will be accepted")
        
        else:
            await ctx.send("You should never see this message")
        
        try:
            ImportantFunctions = self.bot.get_cog('ImportantFunctions')
            await ImportantFunctions.create_account(user=user)
            await ImportantFunctions.add_credits(user=user,amt=amt)
        except:
            pass

    @commands.command(name="Eventlist",aliases=["eventslist"],hidden=True)
    async def eventslist(self,ctx):
        embed=discord.Embed(title="Events List",color = random.choice(colourlist))
        embed.add_field(name="Event rarities:",value=f"""
                        **Common Event** (40% Chance of occuring) \nTyping \n10-20 Coins\n
                        **Uncommon Event** (30% Chance of occuring)  \nFill in the blanks \n20-40 Coins\n
                        **Rare Event** (15% Chance of occuring) \nUnscramble \n40-70 Coins\n
                        **Epic Event** (10% Chance of occuring) \nMeme question \n80-100 Coins\n
                        **Legendary Event** (5% Chance of occuring) \nMeme caption \n100-150 Coins\n""" ,
                        inline=False)
        await ctx.send(embed=embed)

    
    @commands.Cog.listener()
    async def on_message(self,message):
        user=message.author
        if user.bot:
            return
        else:    
            #For random reactions that give you credits
            outcomes=[True,False]
            outcome=random.choices(outcomes,weights=(1,99),k=1)[0]
            if outcome == True:
                await self.credit_reaction(message)

        
    async def credit_reaction(self,message):
        await message.add_reaction(config.credits_emoji)

        def check(reaction, user):
            return str(reaction.emoji) in [config.credits_emoji,] and user != self.bot.user

        try:
            reaction,user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
        except asyncio.TimeoutError:
            await message.remove_reaction(reaction.emoji,self.bot.user)
        else:
            amt=random.choice(list(range(1,200))+list(range(400,500))+list(range(975,1000))+list(range(1975,2000)))
            await message.channel.send(f"{user.mention} wins {amt} credits for reacting to the Credit Emojiyeh first.")
           

          
   


def setup(bot):
    bot.add_cog(Events(bot))