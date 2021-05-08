import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config   
    
class OwnerCog(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
    
    @commands.is_owner()
    @commands.group(name="Add",invoke_without_command=True,case_insensitive=True)
    async def add(self,ctx):
        await ctx.send("Add what? Apples? Oranges? Enter a valid subcommand. Current Options: Credits, Karma.")
    
    @commands.is_owner()
    @add.command(name="Credits",aliases=["credit","creds","cred"])
    async def add_credits(self,ctx,users: commands.Greedy[discord.Member],amt:int):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        given_to_users=""
        for user in users:
            await ImportantFunctions.create_account(user)
            await ImportantFunctions.add_credits(user=user,amt=amt)
            given_to_users=given_to_users + user.mention +", "
        
        await ctx.send(f"{amt} credits has been added to {given_to_users}'s accounts.")
    
    @commands.is_owner()
    @add.command(name="Karma",aliases=["karm"])
    async def add_karma(self,ctx,users: commands.Greedy[discord.Member],amt:int):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        given_to_users=""
        for user in users:
            await ImportantFunctions.create_account(user)
            await ImportantFunctions.add_karma(user=user,amt=amt)
            given_to_users=given_to_users + user.mention +", "
        
        await ctx.send(f"{amt} karma has been added to {given_to_users}'s accounts.")

    
    @commands.is_owner()
    @commands.group(name="Set",invoke_without_command=True,case_insensitive=True)
    async def set_to(self,ctx):
        await ctx.send("Set to what? Apples? Oranges? Enter a valid subcommand. Current Options: Credits, Karma")
    
    @commands.is_owner()
    @set_to.command(name="Credits",aliases=["credit","creds","cred"])
    async def set_credits(self,ctx,users: commands.Greedy[discord.Member],amt:int):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        given_to_users=""
        for user in users:
            await ImportantFunctions.create_account(user)
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    if user.bot:
                        return
                    else: 
                        await ImportantFunctions.create_account(user)
                        await connection.execute("UPDATE info SET credits = $1 WHERE user_id=$2",amt,user.id)
                        given_to_users=given_to_users + user.mention +", "
        
        await ctx.send(f"{given_to_users}'s credits have been set to {amt}.")
    
    @commands.is_owner()
    @set_to.command(name="Karma",aliases=["karm"])
    async def set_karma(self,ctx,users: commands.Greedy[discord.Member],amt:int):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        given_to_users=""
        for user in users:
            await ImportantFunctions.create_account(user)
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    if user.bot:
                        return
                    else: 
                        await ImportantFunctions.create_account(user)
                        await connection.execute("UPDATE info SET karma = $1 WHERE user_id=$2",amt,user.id)
                        given_to_users=given_to_users + user.mention +", "
        
        await ctx.send(f"{given_to_users}'s karma have been set to {amt}.")



    @commands.is_owner()
    @commands.group(name="Reset",invoke_without_command=True,case_insensitive=True,help="Reset a table by removing all rows.")
    async def reset(self,ctx):
        await ctx.send("Enter a valid subcommand.")

    @commands.is_owner()
    @reset.command(name="All",aliases=["both"])
    async def reset_starboard(self,ctx):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("DELETE FROM starboard")
                await connection.execute("DELETE FROM info")
                await ctx.send("Starboard and Info Table has been resetted.")
    
    @commands.is_owner()
    @reset.command(name="Starboard",aliases=["sb"])
    async def reset_both_tables(self,ctx):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("DELETE FROM starboard")
                await ctx.send("Starboard has been resetted.")

    
    @commands.is_owner()
    @reset.command(name="Info")
    async def reset_info(self,ctx):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("DELETE FROM info")
                await ctx.send("Info table has been resetted.")
    
    @commands.is_owner()
    @reset.command(name="Karma")
    async def reset_karma(self,ctx,amt=0):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("UPDATE info SET karma = $1",amt)
                await ctx.send(f"Karma for all users has been set to {amt}")

    @commands.is_owner()
    @reset.command(name="Credits",aliases=["creds","credit","cred","bal","balance"])
    async def reset_credits(self,ctx,amt=0):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("UPDATE info SET credits = $1",amt)
                await ctx.send(f"Credits for all users has been set to {amt}")
    
    
    @commands.is_owner()
    @commands.group(name="Settings",invoke_without_command=True,case_insensitive=True,help="Change server settings. Current Options: Star_limit, Meme_score_to_pin")
    async def settings(self,ctx):
        await ctx.send("Enter a valid subcommand. Current Options: Star_limit, Meme_score_to_pin")
    
    
    @commands.is_owner()
    @settings.command(name="star_limit",aliases=["stars_required","stars"])
    async def settings_change_star_limit(self,ctx,amt:int):
        server=ctx.guild
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("UPDATE server_info SET starboard_stars_required = $1 WHERE id = $2",amt,server.id)
                await ctx.send(f"Starboard star limit to pin has been updated to {amt}.")

    @commands.is_owner()
    @settings.command(name="Meme_score_to_pin",aliases=["score","score_to_pin"])
    async def settings_change_meme_score_to_pin(self,ctx,amt:int):
        server=ctx.guild
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("UPDATE server_info SET meme_score_required_to_pin = $1 WHERE id = $2",amt,server.id)
                await ctx.send(f"Meme score required to pin has been updated to {amt}.")






                



            


    


    

def setup(bot):
    bot.add_cog(OwnerCog(bot))