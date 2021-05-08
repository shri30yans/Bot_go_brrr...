import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config

colourlist=config.embed_colours

awards_list=[awards.Rocket_Dislike,awards.Rocket_Like,awards.Wholesome_Award,awards.Silver_Award,awards.Gold_Award,awards.Platinum_Award,awards.Argentinum_Award,awards.Ternion_Award]
class Economy(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        
        

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Stats",aliases=["account","bal","acc","balance","karma","credits"], help='Displays the account of a user')
    async def bal(self,ctx,user:discord.Member=None):
        user = user or ctx.author
        sent_msg=await ctx.send(embed=discord.Embed(title=f"{user.name}'s Balance",description=f"Fetching {user.name}'s inventory from the database..."))
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')

        if user.bot:
            await ctx.send(f"{user.name} is a bot. Bots don't have accounts.")
        else:
        # retrieve an individual connection from our pool, defined later
            async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
                async with connection.transaction():
                    await ImportantFunctions.create_account(user)
                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                    user_account=dict(user_account)
                    embed=discord.Embed(title=f"{user.name}'s Balance")
                    embed.add_field(name="Balance:",value=f"{user_account['credits']} Credits",inline=True)
                    embed.add_field(name="Karma:",value=f"{user_account['karma']} Karma",inline=True)

                    awards_given_j=json.loads(user_account["awards_given"])
                    awards_received_j=json.loads(user_account["awards_received"])
                    awards_given_str= await self.format_awards_in_order(awards_given_or_recieved_dict=awards_given_j)
                    awards_received_str= await self.format_awards_in_order(awards_given_or_recieved_dict=awards_received_j)

                    awards_given_str=awards_given_str or "None"
                    awards_received_str= awards_received_str or "None"

                    embed.add_field(name="Awards given:",value=f"{awards_given_str}",inline=False)
                    embed.add_field(name="Awards received:",value=f"{awards_received_str}",inline=False)
                    # embed.add_field(name="Upvotes given:",value=f"{user_account['karma']} Karma")
                    # embed.add_field(name="Upvotes received:",value=f"{user_account['karma']} Karma")                                             


                    embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
                    #await ctx.send(embed=embed)
                    await sent_msg.edit(embed=embed)

    async def format_awards_in_order(self,awards_given_or_recieved_dict):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        ordered_reactions_of_post={}
        for x in awards_list[::-1]:
            try:
                ordered_reactions_of_post[x.name.lower()] = awards_given_or_recieved_dict[x.name]
            except:
                pass
            
        all_award_names=[]
        for award in awards_list:
            all_award_names.append(award.name.lower())
        reaction_id_string=""
        for r in ordered_reactions_of_post:
            if r in all_award_names:
                award = await ImportantFunctions.fetch_award(award_name_or_id=r)
                if award == None:
                    print("Not found award")
                    #return
                reaction_id = award.reaction_id
            else:
                print("Not an award or an Star")
            reaction_id_string = reaction_id_string + f"{ordered_reactions_of_post[r]} {reaction_id} ,   "

        return reaction_id_string


    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Awards",aliases=["award,awardlist"], help='A list of all the awards')
    async def award_list(self,ctx):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        user=ctx.author
        async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
            async with connection.transaction():
                await ImportantFunctions.create_account(user)
                user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                user_account=dict(user_account)
                embed=discord.Embed(title=f"{user.name}'s Balance",description=f"Your balance: **{user_account['credits']} Credits**")
                awards_string=""

                for award in awards_list:
                    #awards_string=awards_string + f"{award.reaction_id} **{award.name}** \n {award.cost} credits \n {award.description} \n"
                    embed.add_field(name=f"{award.reaction_id} {award.name} ",value=f"{award.cost} credits \n {award.description} \n",inline=False)

                #embed.add_field(name="Awards:",value=f"{awards_string}",inline=True)
                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
                await ctx.send(embed=embed)

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(name="Beg", help='Beg for cash')
    async def beg(self,ctx):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        user=ctx.author 
        amt=random.randint(1,20)
        beg_options=[f"Someone gave you {amt} credits",f"A comrade gave you half his money. You got {amt} credits.",f"You begged and got {amt} credits.",]
        await ctx.send(random.choice(beg_options))
        await ImportantFunctions.create_account(user)
        await ImportantFunctions.add_credits(user=ctx.message.author,amt=amt)

            

    # @commands.cooldown(1,20, commands.BucketType.user)
    # @commands.command(name="Gamble", help='Gamble away your money')
    # async def gamble(self,ctx,amt:str):
    #     ImportantFunctions = self.bot.get_cog('ImportantFunctions')
    #     user=ctx.author
    #     async with self.bot.pool.acquire() as connection:
    #         async with connection.transaction():
    #             await ImportantFunctions.create_account(user)
    #             user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
    #             if amt.lower() == "all":
    #                 amt = user_account["credits"]
    #             try:
    #                 amt=int(amt)
    #             except:
    #                 await ctx.send(f"{amt} is not a valid number. Please use \"all\" or a valid number.")
    #                 return
    #             if amt <= 0:
    #                 await ctx.send(f"You can't gamble away zero or negative credits, dum-dum")
    #             elif amt < 20:
    #                 await ctx.send(f"Minimum Stakes is 20 credits.")
    #             else:
    #                 if amt > user_account["credits"]:
    #                     await ctx.send("You can't gamble away what you don't have.")
    #                     return
    #                 else:
    #                     choice=random.choice(["lose","win"])
    #                     earnings=random.randint(0,50)
    #                     if choice=="lose":
    #                         total_earned=-(round(amt*(earnings/100)))
    #                         bal=user_account["credits"]+total_earned
    #                         await ctx.send(f"You gambled away {amt} and got {total_earned} credits with an {earnings}% decrease. New balance is {bal} credits ")
    #                     elif choice=="win":
    #                         total_earned=round(amt*(earnings/100))
    #                         bal=user_account["credits"]+total_earned
    #                         await ctx.send(f"You gambled away {amt} and earned {total_earned} credits with an {earnings}% increase. New balance is {bal} credits ")
    #                     else:
    #                         await ctx.send("error")
                        
    #                     await ImportantFunctions.add_credits(user=user,amt=total_earned)

    @commands.cooldown(1,24*60*60, commands.BucketType.user)
    @commands.command(name="Daily", help='Daily bonus')
    async def daily_credits(self,ctx):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        user=ctx.author
        amt = 100
        await ctx.send(f"{amt} credits were added to your account.")   
        await ImportantFunctions.create_account(user)
        await ImportantFunctions.add_credits(user=user,amt=amt) 
    

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Give", help='Give your credits to others')
    async def give(self,ctx,user_mentioned:discord.Member,amt:int):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        user=ctx.author
        if amt<=0:
            await ctx.send(f"You can't give zero or negative credits, dum-dum")
        elif user==user_mentioned:
            await ctx.send(f"You can't give yourself the credits dum dum")
        elif user_mentioned.bot:
            await ctx.send(f"Bots don't have accounts dum dum.")
        else:
            await ImportantFunctions.create_account(user)
            await ImportantFunctions.create_account(user_mentioned)
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    user_balance = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                    if amt > user_balance["credits"]:
                        await ctx.send(f"You can't give what you don't have.")
                    else:
                        await ImportantFunctions.add_credits(user=user,amt=-amt)   
                        await ImportantFunctions.add_credits(user=user_mentioned,amt=amt)  
                        await ctx.send(f"{user.mention} gave {user_mentioned.mention}, {amt} credits.")     

    @commands.group(name="Leaderboard",aliases=["lb"],case_insensitive=True,invoke_without_command=True)   
    async def leaderboard(self,ctx):
        # embed=discord.Embed(title=f"Leaderboard",colour=ctx.guild.me.colour,)
        # embed.add_field(name="Please enter a valid subcommand.",value=f"You can check the leaderboasrds of the highest Karma or Credits.\n Type \"{config.prefix}leaderboard credits\" or \"{config.prefix}leaderboard karma\" ")
        # embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        # await ctx.send(embed=embed)
        await self.karma_leaderboard(ctx)

    
    @leaderboard.command(name="Credits",aliases=["credit","creds","cred"])
    async def credits_leaderboard(self,ctx):
        def myFunc(e):
            return e['credits']
        
        formated_list = await self.leaderboard_row_formatter()
        formated_list.sort(reverse=True,key=myFunc)
        #Top 5
        top5=formated_list[:10]
        top5_string=""
        num=1
        for entry in top5:
            user = self.bot.get_user(entry["user_id"])
            # if user == None:
            #     print(entry["user_id"])
            top5_string = top5_string + f"`{num}.` " + f" {user.mention} • `{entry['credits']} Credits `" + "\n"
            num=num+1
        
        if len(top5_string) == 0:#is space/blank/None
            top5_string = "There are no entries in your leaderboard."
        
        embed=discord.Embed(title=f"Credits Leaderboard",colour=random.choice(colourlist),description=f"{top5_string}")
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await ctx.send(embed=embed)

    @leaderboard.command(name="Karma")
    async def karma_leaderboard(self,ctx):
        def myFunc(e):
            return e['karma']
        formated_list = await self.leaderboard_row_formatter()
        formated_list.sort(reverse=True,key=myFunc)
        #Top 5
        top5=formated_list[:10]
        top5_string=""
        num=1
        for entry in top5:
            user = self.bot.get_user(entry["user_id"])
            top5_string = top5_string + f"`{num}.` " + f" {user.mention} • `{entry['karma']} Karma `" + "\n"
            num=num+1
        
        if top5_string == None:
            print("no entries")
            top5_string = "There are no entries in your leaderboard"
        
        embed=discord.Embed(title=f"Karma Leaderboard",colour=random.choice(colourlist),description=f"{top5_string}")
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await ctx.send(embed=embed)

    
    async def leaderboard_row_formatter(self):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                all_rows = await connection.fetch("SELECT * FROM info")
                formated_list=[]
                elem_dict={}
                for row in all_rows:
                    elem_dict["user_id"]=row["user_id"]
                    elem_dict["credits"]=row["credits"]
                    elem_dict["karma"]=row["karma"]
                    formated_list.append(dict(elem_dict))
                return formated_list

                
#================================================================================
#                _____                _       
#                |  ___|              | |      
#                | |____   _____ _ __ | |_ ___ 
#                |  __\ \ / / _ \ '_ \| __/ __|
#                | |___\ V /  __/ | | | |_\__ \
#                \____/ \_/ \___|_| |_|\__|___/  
#     
#================================================================================
    
   #All reaction listeners for awards take place in Reactions.py
   
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return

        elif message.channel.id==config.suggestions_channel_id:
            if message.content.startswith("//"):
                return
            else:
                await message.add_reaction(config.upvote_reaction)
                await message.add_reaction(config.downvote_reaction)

        elif message.channel.id==config.meme_channel_id and len(message.attachments) !=0:
            await message.add_reaction(config.upvote_reaction)
            await message.add_reaction(config.downvote_reaction)





   
def setup(bot):
    bot.add_cog(Economy(bot))
        