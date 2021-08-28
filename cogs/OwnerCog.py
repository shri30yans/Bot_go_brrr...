import discord,json,asyncio
from discord.ext import commands
import config   
from utils.ErrorHandler import InvalidSubcommand
import random

colour_list = config.embed_colours
    
class Owner(commands.Cog,name="Owner",description="Owner Commands"): 
    def __init__(self, bot):
        self.bot = bot
    
    @commands.is_owner()
    @commands.command(name="stuff",help=f"stuff")
    async def stuff(self,ctx):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                no_polls='{}'
                await connection.execute("UPDATE info SET cooldown = $1",no_polls)
                await connection.execute("UPDATE info SET awards_received = $1",no_polls)
                embed = discord.Embed(title="stuff done.",description=f"yes you read that right")
                await ctx.send(embed=embed)


    #=============================================
    #Add
    #=============================================
    @commands.is_owner()
    @commands.group(name="Add",invoke_without_command=True,case_insensitive=True,help=f"This command is used to add Karma or Credits to users.")
    async def add(self,ctx):
        raise InvalidSubcommand()
    
    @commands.is_owner()
    @add.command(name="Credits",aliases=["credit","creds","cred"],help=f"Add credit's to a user",require_var_positional=True)#require_var_positional=True makes sure input is not empty
    async def add_credits(self,ctx,users: commands.Greedy[discord.Member],amt:int):
        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        given_to_users=""
        for user in users:
            await UserDatabaseFunctions.add_credits(user=user,amt=amt)
            given_to_users=given_to_users + user.mention +", "
        
        embed = discord.Embed(title=f"Add Credit's command executed.",description=f"{amt} credits have been added for {given_to_users}.",colour = random.choice(colour_list))
        await ctx.send(embed=embed)
    
    @commands.is_owner()
    @add.command(name="Karma",aliases=["karm"],help=f"Add karma to a user",require_var_positional=True)#require_var_positional=True makes sure input is not empty
    async def add_karma(self,ctx,users: commands.Greedy[discord.Member],amt:int):
        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        given_to_users=""
        for user in users:
            await UserDatabaseFunctions.add_karma(user=user,amt=amt)
            given_to_users = given_to_users + user.mention +", "
        
        embed = discord.Embed(title=f"Add Karma command executed.",description=f"{amt} karma have been added for {given_to_users}.",colour = random.choice(colour_list))
        await ctx.send(embed=embed)


    #=============================================
    #Set
    #=============================================
    @commands.is_owner()
    @commands.group(name="Set",invoke_without_command=True,case_insensitive=True,help=f"This command is used to set Karma or Credits to a particular number.")
    async def set_to(self,ctx):
        raise InvalidSubcommand()

    @commands.is_owner()
    @set_to.command(name="Credits",aliases=["credit","creds","cred"],help=f"Set's the credits of a user",require_var_positional=True)#require_var_positional=True makes sure input is not empty
    async def set_credits(self,ctx,users: commands.Greedy[discord.Member],amt:int):
        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        given_to_users=""
        for user in users:
            if user.bot:
                return
            else:
                await UserDatabaseFunctions.has_account(user)
                async with self.bot.pool.acquire() as connection:
                    async with connection.transaction():
                        await connection.execute("UPDATE info SET credits = $1 WHERE user_id=$2",amt,user.id)
                        given_to_users=given_to_users + user.mention +", "
        
        embed = discord.Embed(title=f"Set Credits command executed.",description=f"{given_to_users}'s credit has been set to {amt}",colour = random.choice(colour_list))
        await ctx.send(embed=embed)


    @commands.is_owner()
    @set_to.command(name="Karma",aliases=["karm"],help=f"Set's the karma of a user",require_var_positional=True)#require_var_positional=True makes sure input is not empty
    async def set_karma(self,ctx,users: commands.Greedy[discord.Member],amt:int):
        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        given_to_users=""
        for user in users:
            if user.bot:
                return
            else:
                await UserDatabaseFunctions.has_account(user)
                async with self.bot.pool.acquire() as connection:
                    async with connection.transaction():
                        await connection.execute("UPDATE info SET karma = $1 WHERE user_id=$2",amt,user.id)
                        given_to_users=given_to_users + user.mention +", "
        
        embed = discord.Embed(title=f"Set Karma command executed.",description=f"{given_to_users}'s karma has been set to {amt}",colour = random.choice(colour_list))
        await ctx.send(embed=embed)


    #=============================================
    #Reset
    #=============================================
    @commands.is_owner()
    @commands.group(name="Reset",invoke_without_command=True,case_insensitive=True,help=f"Reset information.")
    async def reset(self,ctx):
        raise InvalidSubcommand()

    @commands.is_owner()
    @reset.command(name="All",aliases=["both"],help=f"Resets the both the Info and Starboard tables.\nFormat: `{config.default_prefixes[0]}reset all`")
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
                    embed = discord.Embed(title="Starboard and Info Table resetted.",description=f"Both the tables have resetted.",colour = random.choice(colour_list))
                    await ctx.send(embed=embed)
    
    @commands.is_owner()
    @reset.command(name="Starboard",aliases=["sb"],help=f"Resets the both the Starboard table.")
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
    async def reset_info(self,ctx,help=f"Resets the both the Info table."):
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
                    embed = discord.Embed(title="Info Table resetted.",description=f"The entire Info table has been resetted.",colour = random.choice(colour_list))
                    await ctx.send(embed=embed)

    @commands.is_owner()
    @reset.command(name="Polls",aliases=["poll"],help=f"Resets all the Polls")
    async def reset_all_polls(self,ctx):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                no_polls='{"polls": []}'
                await connection.execute("UPDATE server_info SET ongoing_polls = $1 WHERE id=$2",no_polls,ctx.guild.id)
                embed = discord.Embed(title="All Poll's have been resetted.",description=f"Any ongoing poll's will no longer work.",colour = random.choice(colour_list))
                await ctx.send(embed=embed)
    
    @commands.is_owner()
    @reset.command(name="Karma",help=f"Resets the karma for all users.")
    async def reset_karma(self,ctx,amt=0):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("UPDATE info SET karma = $1",amt)
                embed = discord.Embed(title="Set Karma command executed.",description=f"Karma for all users has been set to {amt}",colour = random.choice(colour_list))
                await ctx.send(embed=embed)

    @commands.is_owner()
    @reset.command(name="Credits",aliases=["creds","credit","cred","bal","balance"],help=f"Resets the credits for all users.")
    async def reset_credits(self,ctx,amt=0):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("UPDATE info SET credits = $1",amt)
                embed = discord.Embed(title="Set Credits command executed.",description=f"Credits for all users has been set to {amt}",colour = random.choice(colour_list))
                await ctx.send(embed=embed)  

    #=============================================
    #Bot functions
    #=============================================
    @commands.is_owner()
    @commands.command(name="Leave",help=f"Leave a guild. Leaves the current guild if no guild id is mentioned")
    async def leave(self,ctx,guild:discord.Guild=None):
        guild = guild or ctx.guild
        user = ctx.author
        embed = discord.Embed(title=f"Leave command executed.",description=f"Left {guild.name}",colour = random.choice(colour_list))
        embed.set_thumbnail(url=str(ctx.guild.icon_url)) 
        embed.set_footer(icon_url= user.avatar_url,text=f"Requested by {user.name} • {self.bot.user.name} ")
        await ctx.send(embed=embed)
        await guild.leave()

    @commands.is_owner()
    @commands.command(name="Nickname",aliases=["nick"],help=f"Change the bot nickname in that server.")
    async def change_nickname(self,ctx,new_nickname:str):
        user = ctx.author
        embed = discord.Embed(title=f"Nickname command executed.",description=f"{self.bot.user.mentions}'s nickname has been changed to {new_nickname}",colour = random.choice(colour_list))
        embed.set_thumbnail(url=str(ctx.guild.icon_url)) 
        embed.set_footer(icon_url= user.avatar_url,text=f"Requested by {user.name} • {self.bot.user.name} ")
        await ctx.send(embed=embed)
        await ctx.guild.me.edit(nick=new_nickname)
    


def setup(bot):
    bot.add_cog(Owner(bot))