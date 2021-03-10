import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config   
    
class DatabaseFunctions(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    async def create_account(self,user:discord.Member):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                if user_account == None:
                    if user.bot:pass
                        #await ctx.send(f"{user.name} is a bot. Bots don't need accounts.")
                    else: 
                        # create an account   
                        empty_json=json.dumps({})   
                        reactions=json.dumps({"upvote":0,"downvote":0,"star":0}) 

                        await connection.execute('INSERT INTO info (user_id,credits,karma,awards_received,awards_given,reactions_received,reactions_given) VALUES ($1,0,0,$2,$3,$4,$5)',user.id,empty_json,empty_json,reactions,reactions)


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

    async def add_awards(self,user_recieving,user_giving,award_name:str):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                if user_recieving.bot:pass
                else:
                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user_recieving.id)
                    user_account= dict(user_account)
                    awards_received=json.loads(user_account["awards_received"])
                    if award_name in awards_received:
                        awards_received[award_name]=awards_received[award_name] + 1
                    else:
                        awards_received.update({award_name:1})
                    awards_update=json.dumps(awards_received)
                    await connection.execute("UPDATE info SET awards_received = $1 WHERE user_id=$2",awards_update,user_recieving.id)

                if user_giving.bot:pass
                else:
                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user_giving.id)
                    user_account= dict(user_account)
                    awards_given=json.loads(user_account["awards_given"])
                    if award_name in awards_given:
                        awards_given[award_name]=awards_given[award_name] + 1
                    else:
                        awards_given.update({award_name:1})
                    awards_update=json.dumps(awards_given)
                    await connection.execute("UPDATE info SET awards_given = $1 WHERE user_id=$2",awards_update,user_giving.id)

    async def add_reactions(self,user_recieving,user_giving,reaction_name:str,num):
        await self.create_account(user=user_recieving)
        await self.create_account(user=user_giving)
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                if user_recieving.bot:pass
                else:

                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user_recieving.id)
                    user_account= dict(user_account)
                    reactions_received=json.loads(user_account["reactions_received"])
                    reactions_received[reaction_name]=reactions_received[reaction_name] + num
                    reactions_update=json.dumps(reactions_received)
                    await connection.execute("UPDATE info SET reactions_received = $1 WHERE user_id=$2",reactions_update,user_recieving.id)
                    #print("Recieving",user_recieving.name,reactions_update)
                
                if user_giving.bot:pass
                else:
                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user_giving.id)
                    user_account= dict(user_account)
                    reactions_given=json.loads(user_account["reactions_given"])
                    reactions_given[reaction_name]=reactions_given[reaction_name] + num
                    reactions_update=json.dumps(reactions_given)
                    await connection.execute("UPDATE info SET reactions_given = $1 WHERE user_id=$2",reactions_update,user_giving.id)
                    #print("Giving",user_giving.name,reactions_update)


def setup(bot):
    bot.add_cog(DatabaseFunctions(bot))