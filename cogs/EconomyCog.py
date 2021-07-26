import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config

colourlist=config.embed_colours

class Economy(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        self.messages_count_dict={}
        

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Stats",aliases=["account","bal","acc","balance","karma","credits","profile"], help=f"Shows the Karma, Credits and Awards of a user\nFormat: `{config.prefix}stats'\nAliases: `Account`, `Bal`, `Acc`, `Balance`, `Karma`, `Credits`, `Stats`, `Profile`")
    async def bal(self,ctx,user:discord.Member=None):
        user = user or ctx.author
        sent_msg=await ctx.reply(embed=discord.Embed(title=f"{user.name}'s Balance",description=f"Fetching {user.name}'s inventory from the database..."))
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        if user.bot:
            await ctx.reply(f"{user.name} is a bot. Bots don't have accounts.")
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
                    awards_given_str,total_awards_given= await self.format_awards_in_order(awards_dict=awards_given_j)
                    awards_received_str,total_awards_received= await self.format_awards_in_order(awards_dict=awards_received_j)

                    awards_given_str=awards_given_str or "None"
                    awards_received_str= awards_received_str or "None"

                    embed.add_field(name="Awards given:",value=f"{awards_given_str}\nTotal awards given: {total_awards_given}",inline=False)
                    embed.add_field(name="Awards received:",value=f"{awards_received_str}\nTotal awards received: {total_awards_received}",inline=False)
                    # embed.add_field(name="Upvotes given:",value=f"{user_account['karma']} Karma")
                    # embed.add_field(name="Upvotes received:",value=f"{user_account['karma']} Karma")                                             


                    embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
                    await sent_msg.edit(embed=embed)

    async def format_awards_in_order(self,awards_dict:str):
        #formats the awards in order of cost
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        ordered_reactions_of_post={}
        for x in list(awards.awards_list.values())[::-1]:
            try:
                ordered_reactions_of_post[x.name.lower()] = awards_dict[x.name]
            except:
                pass                
            
        total_awards=0        
        reaction_id_string=""
        for r in ordered_reactions_of_post:
            award = await ImportantFunctions.fetch_award(award_name_or_id=r)
            count=ordered_reactions_of_post[r]
            total_awards+=count
            reaction_id = award.reaction_id
            reaction_id_string = reaction_id_string + f"{count} {reaction_id} ,   "

        return reaction_id_string,total_awards


    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Awards",aliases=["award,awardlist"], help=f"Shows list of all the awards with their description, cost and other details\nFormat: `?Awardlist'\nAliases: `Awardlist`")
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

                for award in list(awards.awards_list.values())[::-1]:
                    embed.add_field(name=f"{award.reaction_id} {award.name} ",value=f"{award.cost} credits \n {award.description} \n",inline=False)

                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
                await ctx.reply(embed=embed)

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(name="Beg", help='Beg for cash\nFormat: `?beg`')
    async def beg(self,ctx):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        user=ctx.author 
        amt=random.randint(1,20)
        beg_options=[f"Someone gave you {amt} credits",f"A comrade gave you half his money. You got {amt} credits.",f"You begged and got {amt} credits.",]
        await ctx.reply(random.choice(beg_options))
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
    #             elif amt < 50:
    #                 await ctx.send(f"Minimum Stakes is 50 credits.")
    #             else:
    #                 if amt > user_account["credits"]:
    #                     await ctx.send("You can't gamble away what you don't have.")
    #                     return
    #                 else:
    #                     choice=random.choice(["lose","win"])
    #                     earnings=random.randint(0,20)
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
    @commands.command(name="Daily", help='Get some bonus coins everyday.\nFormat: `?Daily`')
    async def daily_credits(self,ctx):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        user=ctx.author
        amt = 100
        await ctx.reply(f"{amt} credits were added to your account.")   
        await ImportantFunctions.create_account(user)
        await ImportantFunctions.add_credits(user=user,amt=amt) 
    

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Give", help='Give your credits to others\nFormat: `?Give @user amount_to_give`')
    async def give(self,ctx,user_mentioned:discord.Member,amt:int):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        user=ctx.author
        guild=self.bot.get_guild(config.APPROVED_SERVERS[0])
        member=guild.get_member(user_mentioned.id)
        if amt<=0:
            await ctx.reply(f"You can't give zero or negative credits, dum-dum")
        elif user==user_mentioned:
            await ctx.reply(f"You can't give yourself the credits dum dum")
        elif user_mentioned.bot:
            await ctx.reply(f"Bots don't have accounts dum dum.")
        #checks if the person you are giving it to has a boost role.
        elif any([role.id in [config.wheel_credit_boost_role_id,] for role in member.roles]):
            await ctx.reply(f"The person you are giving the credits to has a Booster role. Try again later.")
        else:
                await ImportantFunctions.create_account(user)
                await ImportantFunctions.create_account(user_mentioned)
                async with self.bot.pool.acquire() as connection:
                    async with connection.transaction():
                        user_balance = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                        if amt > user_balance["credits"]:
                            await ctx.reply(f"You can't give what you don't have.")
                        else:
                            await ImportantFunctions.add_credits(user=user,amt=-amt)   
                            await ImportantFunctions.add_credits(user=user_mentioned,amt=amt)  
                            await ctx.reply(f"{user.mention} gave {user_mentioned.mention}, {amt} credits.")     

    @commands.group(name="Leaderboard",aliases=["lb"],help=f"Shows the server leaderboard\nFormat: `{config.prefix}Leaderboard subcommand`\nSubcommands: `Karma`, `Credits`",case_insensitive=True,invoke_without_command=True)   
    async def leaderboard(self,ctx,page:int=1):
        await self.karma_leaderboard(ctx,page)

    
    @leaderboard.command(name="Credits",aliases=["credit","creds","cred"],help=f"Shows the server leaderboard according to the credits.\nFormat: `{config.prefix}Leaderboard credits`")
    async def credits_leaderboard(self,ctx,page:int=1):
        formated_list = await self.get_leaderboard("credits")
        #Top 10
        top=formated_list[page*10-10:page*10]
        top_string=""
        for entry in top:
            num=formated_list.index(entry)+1
            try:
                user = await self.bot.get_user(entry["user_id"])
                top_string = top_string + f"`{num}.` " + f" {user.mention} • `{entry['credits']} Credits `" + "\n"
            except:
                user = await self.bot.fetch_user(entry["user_id"])
                top_string = top_string + f"`{num}.` " + f" {user.mention} • `{entry['credits']} Credits `" + "\n"
        
        if len(top_string) == 0:#is space/blank/None
            top_string = "There are no entries in your leaderboard."
        
        embed=discord.Embed(title=f"Credits Leaderboard",colour=random.choice(colourlist),description=f"{top_string}")
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await ctx.reply(embed=embed)

    @leaderboard.command(name="Karma",help=f"Shows the server leaderboard according to the karma.\nFormat: `{config.prefix}Leaderboard karma`")
    async def karma_leaderboard(self,ctx,page:int=1):
        formated_list = await self.get_leaderboard("karma")
        #Top 5
        top=formated_list[page*10-10:page*10]
        top_string=""
        for entry in top:
            try:
                num=formated_list.index(entry)+1
                user = await self.bot.bot_user(entry["user_id"])
                top_string = top_string + f"`{num}.` " + f" {user.mention} • `{entry['karma']} Karma `" + "\n"
            except:
                user = await self.bot.fetch_user(entry["user_id"])
                top_string = top_string + f"`{num}.` " + f" {user.mention} • `{entry['karma']} Karma `" + "\n"
        
        if len(top_string) == 0 :
            top_string = "There are no entries in your leaderboard"
        
        embed=discord.Embed(title=f"Karma Leaderboard",colour=random.choice(colourlist),description=f"{top_string}")
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await ctx.reply(embed=embed)

    
    async def get_leaderboard(self,column):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                if column == "credits":
                    all_rows = await connection.fetch("SELECT * FROM info ORDER BY credits DESC")
                elif column== "karma":
                    all_rows = await connection.fetch("SELECT * FROM info ORDER BY karma DESC")
                return all_rows

   #Reaction listeners for awards have been shifted to Reactions.py
    @commands.command(name="test") 
    async def test(self,ctx):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                all_rows = await connection.fetch("SELECT * FROM info ORDER BY credits DESC")
                print(all_rows)


   #For adding credits for chatting in #main_chat
    @commands.Cog.listener()
    async def on_message(self,message):
        user=message.author
        if user.bot:
            return
        if message.channel.id != config.main_chat_id:
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
            if str(user.id) in self.messages_count_dict:
                if self.messages_count_dict[str(user.id)] >= 5:
                    self.messages_count_dict[str(user.id)] = 0 #reset messages
                    #Add credits
                    ImportantFunctions = self.bot.get_cog('ImportantFunctions')
                    amt=5
                    await ImportantFunctions.create_account(user)
                    await ImportantFunctions.add_credits(user=user,amt=amt)
                
                else:
                    self.messages_count_dict[str(user.id)] += 1
                
            else:
                self.messages_count_dict[str(user.id)] = 1
            
   


def setup(bot):
    bot.add_cog(Economy(bot))
        