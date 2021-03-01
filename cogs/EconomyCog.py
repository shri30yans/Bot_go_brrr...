import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import config
class Economy(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Bal",aliases=["account","stats"], help='Balance of a user')
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
                    embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Star Wars Bot ")
                    await ctx.send(embed=embed)


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
                        await connection.execute('INSERT INTO info (user_id,credits) VALUES ($1,0)',user.id)


                else:
                    return
    
    async def add_credit(self,user,amt):
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

        if "Stonks".lower() in message.content.lower():
            amt= random.randint(300,100)
            await self.add_credit(user=message.author,amt=amt)



    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        upvote_limit = 8
        downvote_limit = 5
        if user.bot:
            return

        if reaction.message.channel.id == config.suggestions_channel_id:
            all_reacts=reaction.message.reactions
            for reaction in all_reacts:
                if str(reaction) == config.upvote_reaction and reaction.count >= upvote_limit+1:
                    pass
                if str(reaction) == config.downvote_reaction and reaction.count >= downvote_limit+1:
                    await reaction.message.delete()
        else:
            if str(reaction) == config.upvote_reaction:
                amt = random.randint(1,4)
                await self.add_credit(user=reaction.message.author,amt=amt)

                    
            if str(reaction) == config.downvote_reaction:
                amt = random.randint(-1,-4)
                await self.add_credit(user=reaction.message.author,amt=amt)
                
    
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
        