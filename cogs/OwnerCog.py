import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config   
    
class OwnerCog(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
    
    @commands.is_owner()
    @commands.group(name="Add",hidden=True,invoke_without_command=True,case_insensitive=True)
    async def add(self,ctx):
        await ctx.send("Add what? Apples? Oranges? Enter a valid subcommand.")
    
    @commands.is_owner()
    @add.command(name="Credits",aliases=["credit","creds","cred"])
    async def add_credits(self,ctx,users: commands.Greedy[discord.Member],amt:int):
        DatabaseFunctions = self.bot.get_cog('DatabaseFunctions')
        given_to_users=""
        for user in users:
            await DatabaseFunctions.create_account(user)
            await DatabaseFunctions.add_credits(user=user,amt=amt)
            given_to_users=given_to_users + user.mention +", "
        
        await ctx.send(f"{amt} credits has been added to {given_to_users}'s accounts.")
    
    @commands.is_owner()
    @add.command(name="Karma",aliases=["karm"])
    async def add_karma(self,ctx,users: commands.Greedy[discord.Member],amt:int):
        DatabaseFunctions = self.bot.get_cog('DatabaseFunctions')
        given_to_users=""
        for user in users:
            await DatabaseFunctions.create_account(user)
            await DatabaseFunctions.add_karma(user=user,amt=amt)
            given_to_users=given_to_users + user.mention +", "
        
        await ctx.send(f"{amt} karma has been added to {given_to_users}'s accounts.")

    
    @commands.is_owner()
    @commands.group(name="Set",hidden=True,invoke_without_command=True,case_insensitive=True)
    async def set_to(self,ctx):
        await ctx.send("Set to what? Apples? Oranges? Enter a valid subcommand.")
    
    @commands.is_owner()
    @set_to.command(name="Credits",aliases=["credit","creds","cred"])
    async def set_credits(self,ctx,users: commands.Greedy[discord.Member],amt:int):
        DatabaseFunctions = self.bot.get_cog('DatabaseFunctions')
        given_to_users=""
        for user in users:
            await DatabaseFunctions.create_account(user)
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    if user.bot:
                        return
                    else: 
                        await DatabaseFunctions.create_account(user)
                        await connection.execute("UPDATE info SET credits = $1 WHERE user_id=$2",amt,user.id)
                        given_to_users=given_to_users + user.mention +", "
        
        await ctx.send(f"{given_to_users}'s credits have been set to {amt}.")
    
    @commands.is_owner()
    @set_to.command(name="Karma",aliases=["karm"])
    async def set_karma(self,ctx,users: commands.Greedy[discord.Member],amt:int):
        DatabaseFunctions = self.bot.get_cog('DatabaseFunctions')
        given_to_users=""
        for user in users:
            await DatabaseFunctions.create_account(user)
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    if user.bot:
                        return
                    else: 
                        await DatabaseFunctions.create_account(user)
                        await connection.execute("UPDATE info SET karma = $1 WHERE user_id=$2",amt,user.id)
                        given_to_users=given_to_users + user.mention +", "
        
        await ctx.send(f"{given_to_users}'s karma have been set to {amt}.")


    


    

def setup(bot):
    bot.add_cog(OwnerCog(bot))