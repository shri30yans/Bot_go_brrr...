import os,discord,platform,random,json,asyncio,re
from discord.ext import commands
import config
import core.checks as checks
from datetime import datetime

colourlist=config.embed_colours

class Moderation(commands.Cog,name="Moderation",description="Perform moderation commands."): 
    def __init__(self, bot):
        self.bot = bot
        self.bot.launch_time = datetime.utcnow()

    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.command(name="Delete",aliases=['del', 'clear'], help=f'Deletes messages')
    async def delete(self,ctx,num:int):
        
        if num>=100:
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.add_field(name="Too many messages deleted.",value=f"You can delete a maximum of 100 messages at one go to prevent excessive deleting. ") 
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.reply(embed=embed,delete_after=4)
            ctx.command.reset_cooldown(ctx)

        else:
            await ctx.channel.purge(limit=num+1,bulk=True)
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.add_field(name="Deleted",value=f"Deleted {num} message(s)") 
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.send(embed=embed,delete_after=4)
    
    # @commands.has_permissions(manage_messages=True)
    # @commands.cooldown(1, 10, commands.BucketType.user)
    # @commands.command(name="Warn", help=f'Warns a user to stop doing a certain activity')
    # async def warn(self,ctx, members: commands.Greedy[discord.Member], *, reason='violation of rules',require_var_positional=True):
    #         warned_names=""
    #         disabled_dm=""
    #         for mbr in members:
                
    #             if mbr == ctx.author: 
    #                 pass
                
    #             elif mbr.bot: 
    #                 pass
                
    #             elif mbr.top_role < ctx.author.top_role or ctx.author==ctx.guild.owner:
    #                 embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
    #                 embed.add_field(name="<:warn:789487083802460200> | Warning",value=f"You have been warned for \"**{reason}**\" in \"**{ctx.guild.name}**\". Repeated violation of rules could lead to a ban. Please ensure such behaviour is not repeated again.") 

    #                 author_avatar=ctx.author.avatar_url
    #                 embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ") 
    #                 try:
    #                     await mbr.send(embed=embed)
    #                     warned_names=warned_names+mbr.name+", "
    #                 except:
    #                     disabled_dm=disabled_dm+mbr.name+", "


    #             else: pass
            
    #         embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
    #         if warned_names=="":
    #             if disabled_dm != "":
    #                 #Nobody was warned
    #                 ctx.command.reset_cooldown(ctx)
    #                 embed.add_field(name="⚠️ | Warn Command not Executed",value=f"\"**{disabled_dm}**\" has either blocked the bot or has disabled DM's.")
    #             else:
    #                 embed.add_field(name="⚠️ | Warn Command not Executed",value=f"Nobody was warned.This could be the cause of :\n • Mentioned user is not found.\n • Mentioned user is are above/equal to your role.\n • Mentioned User is a bot\n • You mentioned yourself (in that case you need to go get your brain checked up).")
    #         else:
    #             if disabled_dm=="":
    #                 embed.add_field(name="⚠️ | Warn Command Executed",value=f"Warned \"**{warned_names}**\" for \"**{reason}**\".")
    #             else:
    #                 embed.add_field(name="⚠️ | Warn Command Executed",value=f"Warned \"**{warned_names}**\" for \"**{reason}**\".")
    #         embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")    
    #         await ctx.reply(embed=embed)
        
    
    # @commands.has_permissions(ban_members=True)
    # @commands.bot_has_permissions(ban_members=True)
    # @commands.cooldown(1,5, commands.BucketType.user)
    # @commands.command(name="Ban", help=f'Bans a user"')
    # async def ban(self,ctx, members: commands.Greedy[discord.Member], *, reason='violation of rules',require_var_positional=True):
    #         warned_names=""
    #         for mbr in members:
    #             if mbr == ctx.author: 
    #                 pass
                
    #             elif mbr.top_role < ctx.author.top_role or ctx.author==ctx.guild.owner:
    #                 embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
    #                 embed.add_field(name="🚫 | Banned",value=f"You have been banned for \"**{reason}**\" in \"**{ctx.guild.name}**\".") 
    #                 author_avatar=ctx.author.avatar_url
    #                 embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ") 
                    
    #                 try:
    #                     await mbr.send(embed=embed)
    #                 except:
    #                     pass

    #                 try:
    #                     await ctx.guild.ban(mbr)
    #                 except:
    #                     await ctx.send("Failed to Ban!")
                
    #             else:pass
            
    #         embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
    #         if warned_names=="":
    #             embed.add_field(name="🚫 | Ban command not Executed",value=f"Nobody was banned.This could be the cause of :\n • Mentioned user is not found.\n • Mentioned user is are above/equal to your role.\n • You mentioned yourself (in that case you need to go get your brain checked up).\n**Make sure the user you are trying to kick is below my highest role.**")
    #             ctx.command.reset_cooldown(ctx)
    #         else:
    #             embed.add_field(name="🚫 | Banned command Executed",value=f" \"**{warned_names}**\"was banned for \"**{reason}**\".")
    #         #embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} •{self.bot.user.name}")    
    #         await ctx.send(embed=embed)
           
    # @commands.has_permissions(kick_members=True)
    # @commands.bot_has_permissions(kick_members=True)
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # @commands.command(name="Kick", help=f'Kicks a user')
    # async def kick(self,ctx, members: commands.Greedy[discord.Member], *, reason='violation of rules',require_var_positional=True):
    #         warned_names=""
    #         for mbr in members:
                
    #             if mbr == ctx.author: pass
                
    #             elif mbr.top_role < ctx.author.top_role or ctx.author==ctx.guild.owner:
    #                     embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
    #                     embed.add_field(name=":boot: | Kicked",value=f"You have been kicked from \"**{ctx.guild.name}**\" for \"**{reason}**\".") 
    #                     author_avatar=ctx.author.avatar_url
    #                     embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name}") 
                        
    #                     try:await mbr.send(embed=embed)
    #                     except: pass
                        
    #                     try : await mbr.kick(reason=reason)
    #                     except : await ctx.send("Failed to Kick!")
    #                     warned_names=warned_names+mbr.name+", "

    #             else: pass
            
    #         embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
    #         if warned_names=="":
    #             ctx.command.reset_cooldown(ctx)
    #             embed.add_field(name=":boot: | Kick command not Executed",value=f"Nobody was kicked.This could be the cause of :\n • Mentioned user is not found.\n • Mentioned user is are above/equal to your role.\n • You mentioned yourself (in that case you need to go get your brain checked up). \n **Make sure the user you are trying to kick is below my highest role.**")
    #         else:
    #             embed.add_field(name=":boot: | Kick command Executed",value=f" \"**{warned_names}**\"was kicked for \"**{reason}**\".")
    #         #embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")    
    #         await ctx.reply(embed=embed)
    
   
    # @checks.server_is_approved()
    # @commands.has_permissions(manage_roles=True)
    # @commands.bot_has_permissions(manage_roles=True)
    # #@commands.cooldown(1, 10, commands.BucketType.user)
    # @commands.command(name="Mute", help=f'Mutes a user. Time can be entered in (s|m|h|d), Default time is 10 mins.',require_var_positional=True)
    # async def mute(self,ctx,members: commands.Greedy[discord.Member],time:str="5m"):
    #         warned_names=""
    #         pos = ["s","m","h","d"]
    #         time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}
    #         unit = time[-1]
    #         if unit not in pos:
    #             await ctx.send(f"You didn't answer with a proper unit. Use (s|m|h|d) next time!")
    #             return
    #         try:
    #             val = int(time[:-1])
    #         except:
    #             await ctx.send(f"The time can only be an integer. Please enter an integer next time.")
    #             return
    #         time_secs= val * time_dict[unit]
            
    #         role = discord.utils.get(ctx.guild.roles, id=config.muted_role_id)
    #         if role == None:
    #             role = discord.utils.get(ctx.guild.roles, name="Muted")
    #             if role == None:
    #                 await ctx.send("The muted role was not found.")
    #                 return
    #         #role = discord.utils.get(ctx.guild.roles, name="Muted")
            
    #         for mbr in members:
                
    #             if mbr == ctx.author: pass
                
    #             elif mbr.top_role < ctx.author.top_role or ctx.author==ctx.guild.owner:
                    
    #                 embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
    #                 embed.add_field(name=":mute: | Muted",value=f"You have been muted from \"**{ctx.guild.name}**\" for \"**{time}**\".") 
    #                 embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ") 
                    
    #                 try:await mbr.send(embed=embed)
    #                 except: 
    #                     pass
    #                     #print("Cound not send Dm")
                    
    #                 try: 
    #                     await mbr.add_roles(role)
    #                     warned_names=warned_names+mbr.mention+", "
    #                 except : 
    #                     await ctx.send("Failed to mute!")
    #             else: pass
            
    #         embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
    #         if warned_names=="":
    #             ctx.command.reset_cooldown(ctx)
    #             embed.add_field(name=":mute: | Mute command not executed",value=f"Nobody was muted.This could be the cause of :\n • Mentioned user is not found.\n • Mentioned user is are above/equal to your role.\n • You mentioned yourself \n **Make sure the mentioned user and the mute role is below my highest role.**")
    #         else:
    #             embed.add_field(name=":mute: | Mute command executed",value=f"**{warned_names}** was muted for **{time}**!")
    #         embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} •{self.bot.user.name} ")    
    #         await ctx.send(embed=embed)

    #         await asyncio.sleep(int(time_secs))
    #         for mbr in members:
    #             try : 
    #                 await mbr.remove_roles(role)

    #             except : 
    #                 await ctx.send("Failed to unmute!")
   
    # @commands.guild_only()
    # @commands.has_permissions(manage_roles=True)
    # @commands.bot_has_permissions(manage_roles=True)
    # @commands.cooldown(1, 10, commands.BucketType.user)
    # @commands.command(name="Createmuterole", help=f'Mutes a user \n \"{config.default_prefixes[0]}Mute @User 5m\" or \"{config.default_prefixes[0]} mute @User @User 10m\". Time can be entered in (s|m|h|d), Default time is 10 mins.')
    # async def createmuterole(self,ctx):
    #     embed=discord.Embed(title='Creating Muted role',description="Creating the role...")
    #     embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")   
    #     message=await ctx.send(embed=embed)
    #     mute_role = await ctx.guild.create_role(name="Muted", reason="Muted role")
    #     embed=discord.Embed(title='Creating Muted role',description="Setting permissions...")
    #     embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")   
    #     await message.edit(embed=embed)
    #     for channel in ctx.guild.channels:
    #         await channel.set_permissions(mute_role, send_messages=False)
    #     embed=discord.Embed(title='Creating Muted role',description=f"Created a muted role: {mute_role.mention}")
    #     embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")   
    #     await message.edit(embed=embed)


    # @checks.server_is_approved()
    # @commands.has_permissions(manage_roles=True)
    # @commands.bot_has_permissions(manage_roles=True)
    # @commands.cooldown(1, 10, commands.BucketType.user)
    # @commands.command(name="Unmute", help=f'Unmutes a user.',require_var_positional=True)
    # async def unmute(self,ctx,members: commands.Greedy[discord.Member]):
    #         warned_names=""
    #         role = discord.utils.get(ctx.guild.roles, id=config.muted_role_id)
    #         if role == None:
    #             role = discord.utils.get(ctx.guild.roles, name="Muted")
    #             if role == None:
    #                 embed = discord.Embed(title=f"Muted role not found.",description=f"Name your muted role \"Muted\". ")
    #                 await ctx.send(embed=embed)
    #                 return  

    #         for mbr in members:
                
    #             if mbr == ctx.author: pass
                
    #             elif mbr.top_role < ctx.author.top_role or ctx.author==ctx.guild.owner:                  
    #                 try : 
    #                     await mbr.remove_roles(role)
    #                     warned_names=warned_names+mbr.mention+", "
    #                 except : 
    #                     await ctx.send("Failed to unmute!")
    #             else: pass
            
    #         embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
    #         if warned_names=="":
    #             ctx.command.reset_cooldown(ctx)
    #             embed.add_field(name=":speaker:  | Unmute command not executed",value=f"Nobody was unmuted. This could be the cause of :\n • Mentioned user is not found.\n • Mentioned user is are above/equal to your role.\n • You mentioned yourself. \n **Make sure the mentioned user and the mute role is below my highest role.**")
    #         else:
    #             embed.add_field(name=":speaker:  | Unmute command executed",value=f"**{warned_names}** was unmuted,")
    #         embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")    
            await ctx.send(embed=embed)



    # async def text_input_function(self,ctx,title:str,text:str):
    #     question_embed=await ctx.send(embed=discord.Embed(title =title,description=text,color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} •{self.bot.user.name} "))
    #     try:
    #         text= await self.bot.wait_for('message', timeout=30.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
    #     except asyncio.TimeoutError:
    #         await question_embed.edit(embed=discord.Embed(title ="Timeout Error",description="You took too much time, ya retarded monkey",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} "))
    #     else: 
    #         if len(text.content)> 50:
    #             embed=discord.Embed(title="<:warn:789487083802460200> | Too many Characters ",color = random.choice(colourlist))
    #             embed.add_field(name="Type only 50 characters in your sentence.",value=f"You typed {len(text.content)} letters. Type the text again.", inline=False)
    #             embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
    #             await ctx.send(embed=embed)
    #             return await self.text_input_function(ctx,title,text)
    #         else:
    #             return str(text.content)


           

def setup(bot):
    bot.add_cog(Moderation(bot))
        