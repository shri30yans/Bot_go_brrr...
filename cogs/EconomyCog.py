import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config

awards_list=[awards.Helpful_Award,awards.Wholesome_Award,awards.Silver_Award,awards.Gold_Award,awards.Platinum_Award,awards.Argentinum_Award,awards.Ternion_Award]
class Economy(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        
        

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Bal",aliases=["account","stats","karma","acc"], help='Balance of a user')
    async def bal(self,ctx,user:discord.Member=None):
        DatabaseFunctions = self.bot.get_cog('DatabaseFunctions')
        user=user or ctx.author
        if user.bot:
            await ctx.send(f"{user.name} is a bot. Bots don't have accounts.")
        else:
        # retrieve an individual connection from our pool, defined later
            async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
                async with connection.transaction():
                    await DatabaseFunctions.create_account(user)
                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                    user_account=dict(user_account)
                    embed=discord.Embed(title=f"{user.name}'s Balance")
                    embed.add_field(name="Balance:",value=f"{user_account['credits']} Credits",inline=True)
                    embed.add_field(name="Karma:",value=f"{user_account['karma']} Karma",inline=True)

                    awards_given_j=json.loads(user_account["awards_given"])
                    awards_received_j=json.loads(user_account["awards_received"])
                    awards_given_str,awards_received_str="",""

                    for award_name in awards_given_j:
                        for award_found in awards_list:
                            if award_name == award_found.name:
                                award=award_found
                                awards_given_str= awards_given_str + award.reaction_id + ": " + str(awards_given_j[award_name]) + ", "

                    for award_name in awards_received_j:
                        for award_found in awards_list:
                            if award_name == award_found.name:
                                award=award_found
                                awards_received_str= awards_received_str + award.reaction_id + ": " + str(awards_received_j[award_name])+ ", "
                    
                    #if its None, the embed will go empty, so to convert None to a string we do this
                    awards_given_str=awards_given_str or "None"
                    awards_received_str= awards_received_str or "None"

                    embed.add_field(name="Awards given:",value=f"{awards_given_str}",inline=False)
                    embed.add_field(name="Awards received:",value=f"{awards_received_str}",inline=False)
                    # embed.add_field(name="Upvotes given:",value=f"{user_account['karma']} Karma")
                    # embed.add_field(name="Upvotes received:",value=f"{user_account['karma']} Karma")                                             


                    embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
                    await ctx.send(embed=embed)

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Awards",aliases=["award,awardlist"], help='A list of all the awards')
    async def award_list(self,ctx):
        DatabaseFunctions = self.bot.get_cog('DatabaseFunctions')
        user=ctx.author
        async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
            async with connection.transaction():
                await DatabaseFunctions.create_account(user)
                user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                user_account=dict(user_account)
                embed=discord.Embed(title=f"{user.name}'s Balance",description=f"Your balance: **{user_account['credits']} Credits**")
                awards_string=""

                for award in awards_list:
                    awards_string=awards_string + f"{award.reaction_id} **{award.name}** \n {award.cost} credits \n {award.description} \n"

                embed.add_field(name="Awards:",value=f"{awards_string}",inline=True)
                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
                await ctx.send(embed=embed)

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(name="Beg", help='Beg for cash')
    async def beg(self,ctx):
        DatabaseFunctions = self.bot.get_cog('DatabaseFunctions')
        user=ctx.author
        amt=random.randint(1,20)
        await DatabaseFunctions.create_account(user)
        await DatabaseFunctions.add_credits(user=ctx.message.author,amt=amt)
        await ctx.send(f"Someone gave you {amt} credits")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Gamble", help='Gamble away your money')
    async def gamble(self,ctx,amt:str):
        DatabaseFunctions = self.bot.get_cog('DatabaseFunctions')
        user=ctx.author
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await DatabaseFunctions.create_account(user)
                user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                if amt.lower() == "all":
                    amt = user_account["credits"]
                try:
                    amt=int(amt)
                except:
                    await ctx.send(f"{amt} is not a valid number. Please use \"all\" or a valid number.")
                    return
                if amt <= 0:
                    await ctx.send(f"You can't gamble away zero or negative credits, dum-dum")
                elif amt < 20:
                    await ctx.send(f"Minimum Stakes is 20 credits.")
                else:
                    if amt > user_account["credits"]:
                        await ctx.send("You can't gamble away what you don't have.")
                        return
                    else:
                        choice=random.choice(["lose","win"])
                        earnings=random.randint(0,100)
                        if choice=="lose":
                            total_earned=-(round(amt*(earnings/100)))
                            bal=user_account["credits"]+total_earned
                            await ctx.send(f"You gambled away {amt} and got {total_earned} credits with an {earnings}% decrease. New balance is {bal} credits ")
                        elif choice=="win":
                            total_earned=round(amt*(earnings/100))
                            bal=user_account["credits"]+total_earned
                            await ctx.send(f"You gambled away {amt} and earned {total_earned} credits with an {earnings}% increase. New balance is {bal} credits ")
                        else:
                            await ctx.send("error")
                        
                        await DatabaseFunctions.add_credits(user=user,amt=total_earned)

    @commands.cooldown(1,24*60*60, commands.BucketType.user)
    @commands.command(name="Daily", help='Daily bonus')
    async def daily_credits(self,ctx):
        DatabaseFunctions = self.bot.get_cog('DatabaseFunctions')
        user=ctx.author
        await DatabaseFunctions.create_account(user)
        amt=100
        await DatabaseFunctions.add_credits(user=user,amt=amt)        

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Give", help='Give your credits to others')
    async def give(self,ctx,user_mentioned:discord.Member,amt:int):
        DatabaseFunctions = self.bot.get_cog('DatabaseFunctions')
        user=ctx.author
        if amt<=0:
            await ctx.send(f"You can't give zero or negative credits, dum-dum")
        elif user==user_mentioned:
            await ctx.send(f"You can't give yourself the credits dum dum")
        elif user_mentioned.bot:
            await ctx.send(f"Bots don't have accounts dum dum.")
        else:
            await DatabaseFunctions.create_account(user)
            await DatabaseFunctions.create_account(user_mentioned)
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    user_balance = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                    if amt > user_balance["credits"]:
                        await ctx.send(f"You can't give what you don't have.")
                    else:
                        await DatabaseFunctions.add_credits(user=user,amt=-amt)   
                        await DatabaseFunctions.add_credits(user=user_mentioned,amt=amt)  
                        await ctx.send(f"{user.mention} gave {user_mentioned.mention}, {amt} credits.")        

#================================================================================
#                _____                _       
#                |  ___|              | |      
#                | |____   _____ _ __ | |_ ___ 
#                |  __\ \ / / _ \ '_ \| __/ __|
#                | |___\ V /  __/ | | | |_\__ \
#                \____/ \_/ \___|_| |_|\__|___/      
#================================================================================
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


    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload): 
        DatabaseFunctions = self.bot.get_cog('DatabaseFunctions') 
        channel=self.bot.get_channel(payload.channel_id) 
        user=self.bot.get_user(payload.user_id)
        message= await channel.fetch_message(payload.message_id)
        emoji=payload.emoji  
        all_reacts=message.reactions

                  
        if user.bot:#if reaction is by a bot
            return
        #Upvote add Karma
        if str(emoji) == config.upvote_reaction and message.author != user:
            amt = random.randint(0,2)
            await DatabaseFunctions.add_karma(user=message.author,amt=amt)
            await DatabaseFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="upvote",num=1)
        #Downvote remove Karma
        elif str(emoji) == config.downvote_reaction and message.author != user:
            amt = random.randint(-3,-1)
            await DatabaseFunctions.add_karma(user=message.author,amt=amt)
            await DatabaseFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="downvote",num=1)

        #if any post has 10 or more upvotes, award that posts author 100 credits
        for reaction in all_reacts:
            if str(emoji) == config.upvote_reaction and reaction.count >= 10:
                amt=100
                await DatabaseFunctions.add_credits(user=message.author,amt=amt)
                return
        #awards
        for award in awards_list:
            if str(emoji) == award.reaction_id:
                async with self.bot.pool.acquire() as connection:
                    async with connection.transaction():
                        await DatabaseFunctions.create_account(user)
                        user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                        user_account=dict(user_account)
                        if user_account["credits"] < award.cost:
                            await message.remove_reaction(emoji, user)
                            await message.channel.send(f"{user.mention} You don't have enough credits to buy this {award.name} award. Try earning some credits first.",delete_after=5)
                        
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
                                    confirm_reaction,confirm_user = await self.bot.wait_for('reaction_add',check=check_accept_or_reject, timeout=60)#pylint: disable=unused-argument 
                                    #disables the confirm_user unusesd argument error

                                except asyncio.TimeoutError:
                                    await check_message.edit(embed=discord.Embed(title="Timeout!",description=f"{user.mention}, did not react after 60 seconds. Award is cancelled.",color = 0xFFD700))

                                else:
                                    if str(confirm_reaction.emoji) == '✅':
                                        await check_message.delete()
                                        await message.channel.send(f"{user.mention} gave {message.author.mention} a {award.name} award.")

                                        embed = discord.Embed(title=f"You received an {award.name} Award!",description=f"{user.mention} liked your [post]({message.jump_url}) so much that the gave it the {award.name} award.",color = 0xFFD700)
                                        embed.set_thumbnail(url=str(emoji.url))
                                        embed.set_footer(icon_url= user.avatar_url,text=f"Given by {user.mention} • {self.bot.user.name} ")

                                        try:await message.author.send(embed=embed)
                                        except:pass
                                        
                                        if award.starboard_post:#starboard_post is a boolean value
                                            await self.award_post_to_starboard(message=message,channel=message.channel,user=user,award=award)

                                        await DatabaseFunctions.add_karma(user=message.author,amt=award.karma_given_to_receiver)
                                        await DatabaseFunctions.add_karma(user=user,amt=award.karma_given_to_giver)
                                        await DatabaseFunctions.add_credits(user=user,amt = -award.cost)
                                        await DatabaseFunctions.add_credits(user=message.author,amt = award.credits_given_to_receiver)
                                        await DatabaseFunctions.add_awards(user_recieving=message.author,user_giving=user,award_name=award.name)

                                    

                                    
                                    elif str(confirm_reaction.emoji) == '❌':
                                        await check_message.delete()
                                        await message.remove_reaction(emoji, user)
                                        await message.channel.send("Award was cancelled.",delete_after=5)
                                    else:
                                        await message.channel.send("Well, you should not be able to see this. Something went wrong")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):  
        DatabaseFunctions = self.bot.get_cog('DatabaseFunctions') 
        channel=self.bot.get_channel(payload.channel_id) 
        user=self.bot.get_user(payload.user_id)
        message= await channel.fetch_message(payload.message_id)
        emoji=payload.emoji  
        if user.bot:#if reaction is by a bot
            return

        if str(emoji) == config.upvote_reaction and message.author != user:
            amt = random.randint(-3,-1)
            await DatabaseFunctions.add_karma(user=message.author,amt=amt)
            await DatabaseFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="upvote",num=-1)

        elif str(emoji) == config.downvote_reaction and message.author != user:
            amt = random.randint(0,2)
            await DatabaseFunctions.add_karma(user=message.author,amt=amt)
            await DatabaseFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="downvote",num=+1)

    async def award_post_to_starboard(self,message,channel,user,award):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                starboard_channel=self.bot.get_channel(config.starboard_channel_id) 
                star_message = await connection.fetchrow("SELECT * FROM starboard WHERE root_message_id=$1",message.id)
                if star_message == None:
                    embed=discord.Embed(color =channel.guild.me.colour,timestamp=message.created_at,description=message.content)
                    embed.set_author(name=message.author.name, icon_url= f"{message.author.avatar_url}")
                    embed.add_field(name="Source:", value=f"[Jump]({message.jump_url})", inline=False)
                    if len(message.attachments): #basically if len !=0
                        embed.set_image(url=message.attachments[0].url)
                    embed.set_footer(text=f"{message.id} ")
                    StarMessage = await starboard_channel.send(f"{award.reaction_id} {channel.mention}",embed=embed)
                    # if user.bot:pass
                    #     #await ctx.send(f"{user.name} is a bot. Bots don't need accounts.")
                    # else:        
                    award_json=json.dumps({award.name:1})          
                    await connection.execute('INSERT INTO starboard (root_message_id,star_message_id,stars,awards) VALUES ($1,$2,$3,$4)',message.id,StarMessage.id,0,award_json)
                else:
                    star_message=dict(star_message)
                    awards_of_post=json.loads(star_message["awards"])
                    if award.name in awards_of_post:
                        awards_of_post[award.name]=awards_of_post[award.name] + 1
                    else:
                        awards_of_post.update({award.name:1})
                    awards_of_post_j=json.dumps(awards_of_post)
                    StarMessage= await starboard_channel.fetch_message(star_message["star_message_id"])
                    await StarMessage.edit(content=f"{awards_of_post} {channel.mention}")
                    await connection.execute("UPDATE starboard SET awards = $1 WHERE root_message_id=$2",awards_of_post_j,message.id)
   
def setup(bot):
    bot.add_cog(Economy(bot))
        