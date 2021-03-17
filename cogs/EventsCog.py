import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config   
#from cogs.EconomyCog import Economy
from datetime import datetime 
import pytz 


    
class Events(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        #basically runs this function when this cog is loaded (which program is started)
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
                time_check = self.check_if_time_is_ok()
                if time_check == False :
                    return
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
            await ctx.send("Enter a proper rarity. (Common,Uncommon,Rare,Epic,Legendary).")
          
        if rarity == 'Common':
            questions={
                "You are in an argument. Quick! Type `No You`.":["no you"],
                "Some one just said \"Hello there\". Quick! Type `General Kenobi`":["general kenobi"],
                "Someone just chopped their pp off! Quick! Give them a Wholesome Award. Send the Wholesome Award Emoji.": [config.reddit_award_wholesome],
                "POV: It's 2018 and you are Shri30yans Gaming. Quick say `Welcome to my Youtube Channel`": ['welcome to my youtube channel'],
                "Reddit just crashed the whole stock market. Quick say `Stonks`": ['stonks'],
                "POV: It's 2017 and Figet Spinners are Trending. Quick say `Fidget`": ['fidget'],
                #"POV: It's Valentine's day. Send this emoji in the chat. (💖) ": ['💖'],
                "POV: It's Christmas! Send this emoji in the chat. (🎄)":['🎄'],
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
                await sent_msg.edit(content=f"{sent_msg.content}\n\n This event is expired. No new submissions will be accepted")
            
        
        
        elif rarity == 'Uncommon':
            questions={"Don't underestimate my _____":"power",
            "I find your lack of _____ disturbing.":"faith",
            "In my experience there is no such thing as ____.":"luck",
            "The fear of ____ is a path to the dark side.":"loss",
            "I was in VC with my ___":"bsf",
            """\nRoses are red,\n
            I love to screw,\n
            My PP is missing,\n
            Nvm it's inside ___""":"you",
            "We need to go ____":"deeper",
            "Don't care, ______ it":"shipped",
            "We were not allowed to ____ in the airport.":"shoot"

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
                await sent_msg.edit(content=f"{sent_msg.content}\n\n This event is expired. No new submissions will be accepted")



        elif rarity == 'Rare':
            questions=["panzer IV","who is golf ball","send nudes","takes shit off","dead chat","creme de la penis","creme de la penis",]
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
                await sent_msg.edit(content=f"{sent_msg.content}\n\n This event is expired. No new submissions will be accepted")

        
        
        elif rarity == 'Epic':
            questions={"Who always has the high ground?":['obi-wan kenobi','kenobi','obi wan','obi-wan','obi wan kenobi',],
                        "Some one just threw something really far. What are they supposed to say?":["yeet","yeet!"],
                        "Hottest Harry Potter Character? Go!":['hagrid'],
                        "What is the name of Tanya's favourite doctor?":['johnny sins'],}
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

    
    @commands.Cog.listener()
    async def on_message(self,message):
        user=message.author
        if user.bot:
            return
        if message.channel.id != 748786284599705688:
            return
        messages = await message.channel.history(limit=5).flatten() 
        #if previous message is also written by same person
        count=0
        for msg in messages:
            if msg.author == message.author:
                count += 1
        if count >= 3:
            return

        else:    
            with open("messagecount.json","r") as messagecount_j:
                users = json.load(messagecount_j)

            if str(user.id) in users:
                if users[str(user.id)] >= 5:
                    users[str(user.id)] = 0 #reset messages
                    #print("added cash")
                    
                    ImportantFunctions = self.bot.get_cog('ImportantFunctions')
                    amt=5
                    await ImportantFunctions.create_account(user)
                    await ImportantFunctions.add_credits(user=user,amt=amt)
                
                else:
                    users[str(user.id)] += 1
                
            else:
                users[str(user.id)] = 1
            
            with open("messagecount.json","w") as messagecount_j:
                json.dump(users,messagecount_j)
        




def setup(bot):
    bot.add_cog(Events(bot))