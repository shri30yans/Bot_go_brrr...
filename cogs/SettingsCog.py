import discord,random
from discord.ext import commands
import config   
    
colour_list = config.embed_colours
class Settings(commands.Cog,name="Settings",description="Bot settings"): 
    def __init__(self, bot):
        self.bot = bot
   
    
    #=============================================
    #Settings
    #=============================================
    # @commands.has_permissions(manage_guild=True) 
    # @commands.group(name="Settings",invoke_without_command=True,case_insensitive=True,help=f"Change server settings.\nFormat: `{config.default_prefixes[0]}settings subcommand` \nSubcommands: `Star_limit`, `Meme_score_to_pin`")
    # async def settings(self,ctx):
    #    raise InvalidSubcommand()
        

  

    @commands.has_permissions(manage_guild=True) 
    @commands.command(name="ChangePrefix",aliases=["newprefix","updateprefix","prefixchange"],help=f"Change the bot prefix for this server")
    async def change_prefix(self,ctx,new_prefix:str):
        new_prefix=new_prefix.rstrip()
        guild_id=ctx.guild.id
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        prefix_list = await ImportantFunctions.get_server_prefixes_string(ctx.guild.id)
        if new_prefix in prefix_list:
            await ctx.reply(f"`{new_prefix}` is the current prefix already.")
        else:
            embed = discord.Embed(title="Server prefix updated",description=f"New server prefix has been updated to `{new_prefix}`",colour = random.choice(colour_list))
            await ctx.send(embed=embed)
            ImportantFunctions = self.bot.get_cog('ImportantFunctions') 
            await ImportantFunctions.update_server_prefix(new_prefix=new_prefix,guild_id=guild_id)

        

    


def setup(bot):
    bot.add_cog(Settings(bot))