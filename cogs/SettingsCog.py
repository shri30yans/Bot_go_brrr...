import discord,random
from discord.ext import commands
import config   
from utils.ErrorHandler import InvalidSubcommand
    
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
    
    # @commands.guild_only()
    # @commands.group(name="Settings",invoke_without_command=True,case_insensitive=True,aliases=["usersettings","config"],help=f"Change starboard settings.")
    # async def settings(self,ctx):
    #     raise InvalidSubcommand()


    # @settings.command(name="Passive",help=f"Toggle the ability to interact with other users. `<value>` can be `True` or `False`.")
    # async def passive_mode(self,ctx,value:bool= None):
    #     user = ctx.author
    #     UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
    #     passive_mode = UserDatabaseFunctions.get_user_passive_mode(user)

    #     if value is None:
    #         if passive_mode:
    #             value=f"You are in Passive mode. You cannot interact with other users."
    #         else:
    #             value=f"You are not Passive mode. You can interact with other users."

    #         title="Passive Mode settings"
    #         name=f"Current Passive setting:{passive_mode}"
    #         await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)
        
    #     elif passive_mode is value:
    #         if passive_mode:
    #             value=f"Starboard is currently locked. No messages can be sent to the starboard.\nUse `starboard Lock False` to change this."
    #         else:
    #             value=f"Starboard is unlocked.\nUse `starboard Lock True` to change this."

    #         title="Starboard Lock"
    #         name=f"Starboard Lock is already set to {lock}"
    #         await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)
        
    #     else:
    #         passive_mode = value
    #         title="Starboard Lock"
    #         name=f"Lock: {passive_mode}"
    #         if passive_mode is False:
    #             value=f"Starboard has been unlocked and is working again."              
            
    #         elif passive_mode is True:
    #             value=f"Starboard has been locked. No other messages can be sent to the starboard."
            
    #         await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)

           # await StarboardFunctions.update_starboard_key(starboard_info=starboard_info,starboard_info_key="lock",value=lock,guild_id=guild_id)


        

    


def setup(bot):
    bot.add_cog(Settings(bot))