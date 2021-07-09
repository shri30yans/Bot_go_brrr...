import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config   
    
class OwnerCog(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
    
    #=============================================
    #Add
    #=============================================
    @commands.is_owner()
    @commands.group(name="Add",invoke_without_command=True,case_insensitive=True,help=f"This command is used to add Karma or Credits to users.\nFormat: `{config.prefix}set subcommand user1 user2 amt`\nSubcommands: credits, karma")
    async def add(self,ctx):
        embed = discord.Embed(title="Invalid subcommand.",description=f"Enter a valid subcommand. Current Options:`Credits`, `Karma`,")
        await ctx.send(embed=embed)
    
    @commands.is_owner()
    @add.command(name="Credits",aliases=["credit","creds","cred"],help=f"Add credit's to a user\nFormat: `{config.prefix}add credits user1 user2 user3 amount_to_add`",require_var_positional=True)#require_var_positional=True makes sure input is not empty
    async def add_credits(self,ctx,users: commands.Greedy[discord.Member],amt:int):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        given_to_users=""
        for user in users:
            await ImportantFunctions.create_account(user)
            await ImportantFunctions.add_credits(user=user,amt=amt)
            given_to_users=given_to_users + user.mention +", "
        
        embed = discord.Embed(title=f"Add Credit's command executed.",description=f"{amt} credits have been added for {given_to_users}.")
        await ctx.send(embed=embed)
    
    @commands.is_owner()
    @add.command(name="Karma",aliases=["karm"],help=f"Add karma to a user\nFormat: `{config.prefix}add karma user1 user2 user3 amount_to_add`",require_var_positional=True)#require_var_positional=True makes sure input is not empty
    async def add_karma(self,ctx,users: commands.Greedy[discord.Member],amt:int):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        given_to_users=""
        for user in users:
            await ImportantFunctions.create_account(user)
            await ImportantFunctions.add_karma(user=user,amt=amt)
            given_to_users = given_to_users + user.mention +", "
        
        embed = discord.Embed(title=f"Add Karma command executed.",description=f"{amt} karma have been added for {given_to_users}.")
        await ctx.send(embed=embed)


    #=============================================
    #Set
    #=============================================
    @commands.is_owner()
    @commands.group(name="Set",invoke_without_command=True,case_insensitive=True,help=f"This command is used to set Karma or Credits to a particular number.\nFormat: `{config.prefix}set subcommand user1 user2 amt`\nSubcommands: credits, karma")
    async def set_to(self,ctx):
        embed = discord.Embed(title="Invalid subcommand.",description=f"Enter a valid subcommand. Current Options:`Credits`, `Karma`,")
        await ctx.send(embed=embed)
    
    @commands.is_owner()
    @set_to.command(name="Credits",aliases=["credit","creds","cred"],help=f"Set's the credits of a user\nFormat: `{config.prefix}set credits user1 user2 user3 amount_to_set_to`",require_var_positional=True)#require_var_positional=True makes sure input is not empty
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
        
        embed = discord.Embed(title=f"Set Credits command executed.",description=f"{given_to_users}'s credit has been set to {amt}")
        await ctx.send(embed=embed)


    @commands.is_owner()
    @set_to.command(name="Karma",aliases=["karm"],help=f"Set's the karma of a user\nFormat: `{config.prefix}set karma user1 user2 user3 amount_to_set_to`",require_var_positional=True)#require_var_positional=True makes sure input is not empty
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
        
        embed = discord.Embed(title=f"Set Karma command executed.",description=f"{given_to_users}'s karma has been set to {amt}")
        await ctx.send(embed=embed)



    #=============================================
    #Reset
    #=============================================
    @commands.is_owner()
    @commands.group(name="Reset",invoke_without_command=True,case_insensitive=True,help=f"Reset information.\nFormat: `{config.prefix}reset subcommand`\nSubcommands: `All`, `Starboard`,`Info`,`Polls`,`Karma`,`Credits`")
    async def reset(self,ctx):
        embed = discord.Embed(title="Invalid subcommand.",description=f"Enter a valid subcommand. Options: `All`, `Starboard`,`Info`,`Polls`,`Karma`,`Credits`,")
        await ctx.send(embed=embed)

    @commands.is_owner()
    @reset.command(name="All",aliases=["both"],help=f"Resets the both the Info and Starboard tables.\nFormat: `{config.prefix}reset all`")
    async def reset_starboard(self,ctx):
        embed=discord.Embed(title="Reset Table confirmation",description="To confirm that you would like to delete the **Starboard** table type `confirm`.\nType `cancel` to cancel resetting`")
        message=await ctx.send(embed=embed)
        try:
            reply_message = await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel and ctx.content.lower() in["confirm","cancel","exit"]))
        except asyncio.TimeoutError:
            message.delete()
        else: 
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute("DELETE FROM starboard")
                    await connection.execute("DELETE FROM info")
                    embed = discord.Embed(title="Starboard and Info Table resetted.",description=f"Both the tables have resetted.")
                    await ctx.send(embed=embed)
    
    @commands.is_owner()
    @reset.command(name="Starboard",aliases=["sb"],help=f"Resets the both the Starboard table.\nFormat: `{config.prefix}reset starboard`")
    async def reset_both_tables(self,ctx):
        embed=discord.Embed(title="Reset Table confirmation",description="To confirm that you would like to delete the **Starboard** table type `confirm`.\nType `cancel` to cancel resetting`")
        message=await ctx.reply(embed=embed)
        try:
            reply_message = await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel and ctx.content.lower() in["confirm","cancel","exit"]))
        except asyncio.TimeoutError:
            message.delete()
        else: 
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    server_info = await connection.fetchrow("SELECT * FROM server_info WHERE id=$1",ctx.guild.id)
                    starboard=json.loads(server_info["starboard"]) #load the json content of the starboard column
                    starboard["starboard_posts"]=[]
                    starboard_json=json.dumps(starboard)
                    await connection.execute("UPDATE server_info SET starboard = $1 WHERE id=$2",starboard_json,ctx.guild.id)
                    #embed=discord.Embed(title="Reset Table confirmation",description="To confirm that you would like to delete the **Starboard** table type `confirm`.\nType `cancel` to cancel resetting`")
                    #await message.edit()
    @commands.is_owner()
    @reset.command(name="Info")
    async def reset_info(self,ctx,help=f"Resets the both the Info table.\nFormat: `{config.prefix}reset info`"):
        embed=discord.Embed(title="Reset Table confirmation",description="To confirm that you would like to delete the **Starboard** table type `confirm`.\nType `cancel` to cancel resetting`")
        message=await ctx.send(embed=embed)
        try:
            reply_message = await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel and ctx.content.lower() in["confirm","cancel","exit"]))
        except asyncio.TimeoutError:
            message.delete()
        else: 
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute("DELETE FROM info")
                    embed = discord.Embed(title="Info Table resetted.",description=f"The entire Info table has been resetted.")
                    await ctx.send(embed=embed)

    @commands.is_owner()
    @reset.command(name="Polls",aliases=["poll"],help=f"Resets all the Polls\nFormat: `{config.prefix}reset karma`")
    async def reset_all_polls(self,ctx):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                no_polls='{"polls": []}'
                await connection.execute("UPDATE server_info SET ongoing_polls = $1 WHERE id=$2",no_polls,ctx.guild.id)
                embed = discord.Embed(title="All Poll's have been resetted.",description=f"Any ongoing poll's will no longer work.")
                await ctx.send(embed=embed)
    
    @commands.is_owner()
    @reset.command(name="Karma",help=f"Resets the karma for all users.\nFormat: `{config.prefix}reset karma`")
    async def reset_karma(self,ctx,amt=0):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("UPDATE info SET karma = $1",amt)
                embed = discord.Embed(title="Set Karma command executed.",description=f"Karma for all users has been set to {amt}")
                await ctx.send(embed=embed)

    @commands.is_owner()
    @reset.command(name="Credits",aliases=["creds","credit","cred","bal","balance"],help=f"Resets the credits for all users.\nFormat: `{config.prefix}reset credits`\nAliases: creds, credit, cred, bal, balance")
    async def reset_credits(self,ctx,amt=0):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("UPDATE info SET credits = $1",amt)
                embed = discord.Embed(title="Set Credits command executed.",description=f"Credits for all users has been set to {amt}")
                await ctx.send(embed=embed)  
    
    #=============================================
    #Settings
    #=============================================
    @commands.is_owner()
    @commands.group(name="Settings",invoke_without_command=True,case_insensitive=True,help=f"Change server settings.\nFormat: `{config.prefix}settings subcommand` \nSubcommands: Star_limit, Meme_score_to_pin")
    async def settings(self,ctx):
        embed = discord.Embed(title="Invalid subcommand.",description=f"Enter a valid subcommand. Options: `Star_limit`, `Meme_score_to_pin`")
        await ctx.send(embed=embed)
        
    
    @commands.is_owner()
    @settings.command(name="star_limit",aliases=["stars_required","stars"],help=f"Change the number of stars required to post it on the starboard.\nFormat: `{config.prefix}settings star_limit number_of_stars`\nAliases: stars_required, stars")
    async def settings_change_star_limit(self,ctx,amt:int):
        server=ctx.guild
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("UPDATE server_info SET starboard_stars_required = $1 WHERE id = $2",amt,server.id)
                embed = discord.Embed(title="Starboard limit changed.",description=f"The Starboard star limit to send a post to starboard has been updated to {amt}.")
                await ctx.send(embed=embed)

    @commands.is_owner()
    @settings.command(name="Meme_score_to_pin",aliases=["score","score_to_pin","meme_score"],help=f"Change the meme score required to pin it.\nFormat: `{config.prefix}settings meme_score_to_pin meme_score_required`\nAliases: score, score_to_pin, meme_score")
    async def settings_change_meme_score_to_pin(self,ctx,amt:int):
        server=ctx.guild
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("UPDATE server_info SET meme_score_required_to_pin = $1 WHERE id = $2",amt,server.id)
                embed = discord.Embed(title="Meme score needed to pin changed.",description=f"Meme score required to pin has been updated to {amt}.")
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(OwnerCog(bot))