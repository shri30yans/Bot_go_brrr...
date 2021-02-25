import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks

colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
            0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]

class Utility(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
   
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Invite", help='Sends Invite link for bot \n sw invite ')
    async def invite(self,ctx):
        embed= discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
        #insert_field_at(index, *, name, value, inline=True)¶
        embed.add_field(name="You can invite me here:",value="[Direct Invite](https://discord.com/oauth2/authorize?client_id=787894718474223616&permissions=0&scope=bot)",inline=False)
        #embed.add_field(name="Join our Discord Support Server:",value="[Discord Server](https://discord.gg/C3XkFwrdER)",inline=False)
        #embed.add_field(name="Mail for business enquiries:",value="yeetbotdev@gmail.com",inline=False)
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)
    
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    
    @commands.command(name="Info",aliases=['botinfo'], help='Returns bot information \n Yeet Info \nAliases: serverstats ')
    async def info(self,ctx):
        embed=discord.Embed(title="Bot Info",color = random.choice(colourlist),timestamp=ctx.message.created_at)
        embed.add_field(name="Created by:",value=f"Shri30yans",inline=False)
        embed.add_field(name="Prefix",value=f"\"**Yeet**\" or \"**y**\"",inline=False)
        embed.add_field(name="Servers:",value=f"{str(len(self.bot.guilds))}",inline=False)
        embed.add_field(name="Users:",value=f"{str(len(self.bot.users) + 1)}",inline=False)
        embed.add_field(name="Logged in as:",value=f"{self.bot.user.name}",inline=False)
        embed.add_field(name="Discord.py API version:",value=f"{discord.__version__}",inline=False)
        embed.add_field(name="Python version:",value=f"{platform.python_version()}",inline=False)
        embed.add_field(name="Running on:",value=f"{platform.system()} {platform.release()} ({os.name})",inline=False)
        #embed.add_field(name="Support server",value=f"[Join the support server.](https://top.gg/bot/750236220595896370/vote)",inline=False)
        #embed.add_field(name="Vote",value=f"[Top.gg Vote](https://top.gg/bot/750236220595896370/vote)",inline=False)
        embed.set_thumbnail(url=str(self.bot.user.avatar_url)) 
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)
        
    
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Ping", help='Tells the Ping of a server \n Yeet ping')
    async def ping(self,ctx):
        """ Pong! """
        message = await ctx.send(embed=discord.Embed(title="Ping",description=":Pong!  :ping_pong:",color = random.choice(colourlist),timestamp=ctx.message.created_at))
        ping = (message.created_at.timestamp() - ctx.message.created_at.timestamp()) * 1000
        embed=discord.Embed(title="Ping",description=f'Pong!  :ping_pong:  \nBot latency: {int(ping)}ms\nWebsocket latency: {round(self.bot.latency * 1000)}ms',color = random.choice(colourlist),timestamp=ctx.message.created_at)
        embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        await message.edit(embed=embed)
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="ServerInfo",aliases=['serverstats','server'], help='Finds server stats \n Yeet stats \nAliases: serverstats ')
    async def stats(self,ctx):
            #f-strings
            guild_owner=str(ctx.guild.owner)
            embed=discord.Embed(title="Server Stats",color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.add_field(name="Name",value=f"{ctx.guild.name}",inline=False)
            if (ctx.message.author.id == ctx.guild.owner_id):
                embed.add_field(name="Owner",value="You are the owner of this server.",inline=False)
            #await message.channel.send("<:okboomer:774171875906682890>")
            else:
                #embed.add_field(name="Owner",value=f"{guild_owner}, is the owner of this server.",inline=False)
                embed.add_field(name="Owner",value=f"{guild_owner}, is the owner of this server.")
            #Region Convert
            region=str(ctx.guild.region)    
            
            #Member calculator
            no_of_members=0
            no_of_bots=0
            for member in ctx.guild.members:
                if member.bot:
                    no_of_bots=no_of_bots+1
                else:
                    no_of_members=no_of_members+1

            embed.add_field(name="Region",value=f"{region.capitalize() }",inline=False)
            embed.add_field(name="Mandalorians",value=f"Members in server: {no_of_members}")
            embed.add_field(name="Droids",value=f"Bots in server: {no_of_bots}",inline=False)
            embed.add_field(name="Roles",value=f"Number of roles: {len(ctx.guild.roles)}")
            created_at_time=self.time_format_function(ctx.guild.created_at)
            embed.add_field(name="Creation date",value=f"{created_at_time}",inline=False) 
            embed.set_thumbnail(url=str(ctx.guild.icon_url)) 
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(embed=embed)
    
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Delete",aliases=['del', 'clear'], help='Deletes messages \n Yeet delete <number_of _messages> \n Aliases: clear, del')
    async def delete(self,ctx,num:int):
        if ctx.author.id== 571957935270395925:
            await ctx.channel.purge(limit=num+1,bulk=True)
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.add_field(name="Deleted",value=f"Deleted {num} message(s)") 
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(embed=embed,delete_after=4)
        
        elif num>=50:
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.add_field(name="Too many messages deleted.",value=f"You can delete a maximum of 50 messages at one go to prevent excessive deleting. ") 
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(embed=embed,delete_after=4)

        else:
            await ctx.channel.purge(limit=num+1,bulk=True)
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.add_field(name="Deleted",value=f"Deleted {num} message(s)") 
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(embed=embed,delete_after=4)

    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Warn", help='Warns a user to stop doing a certain activity \n \"Yeet Warn @User <reason>\" or \"Yeet Warn @User @User <reason>\"')
    async def warn(self,ctx, members: commands.Greedy[discord.Member], *, reason='violation of rules'):
            warned_names=""
            disabled_dm=""
            for mbr in members:
                
                if mbr == ctx.author: pass
                
                elif mbr.bot: pass
                
                elif mbr.top_role < ctx.author.top_role or ctx.author==ctx.guild.owner:
                    embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
                    embed.add_field(name="<:warn:789487083802460200> | Warning",value=f"You have been warned for \"**{reason}**\" in \"**{ctx.guild.name}**\". Repeated violation of rules could lead to a ban. Please ensure such behaviour is not repeated again.") 

                    author_avatar=ctx.author.avatar_url
                    embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ") 
                    try:
                        await mbr.send(embed=embed)
                        warned_names=warned_names+mbr.name+", "
                    except:
                        disabled_dm=disabled_dm+mbr.name+", "


                else: pass
            
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            if warned_names=="":
                if disabled_dm != "":
                    embed.add_field(name="<:warn:789487083802460200> | Warn Command not Executed",value=f"\"**{disabled_dm}**\" has either blocked the bot or has disabled DM's.")
                else:
                    embed.add_field(name="<:warn:789487083802460200> | Warn Command not Executed",value=f"Nobody was warned.This could be the cause of :\n • Mentioned user is not found.\n • Mentioned user is are above/equal to your role.\n • Mentioned User is a bot\n • You mentioned yourself (in that case you need to go get your brain checked up).")
            else:
                if disabled_dm=="":
                    embed.add_field(name="<:warn:789487083802460200> | Warn Command Executed",value=f"Warned \"**{warned_names}**\" for \"**{reason}**\".")
                else:
                    embed.add_field(name="<:warn:789487083802460200> | Warn Command Executed",value=f"Warned \"**{warned_names}**\" for \"**{reason}**\".")
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")    
            await ctx.send(embed=embed)
        
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Ban", help='Bans a user \n\" Yeet Ban @User <reason>\" or \"Yeet Ban @User @User <reason>\"')
    async def ban(self,ctx, members: commands.Greedy[discord.Member], *, reason='violation of rules'):
            warned_names=""
            for mbr in members:
                if mbr == ctx.author: pass
                
                elif mbr.top_role < ctx.author.top_role or ctx.author==ctx.guild.owner:
                    embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
                    embed.add_field(name="<a:YB_Wumpus_Ban:781419747878633492> | Banned",value=f"You have been banned for \"**{reason}**\" in \"**{ctx.guild.name}**\".") 
                    author_avatar=ctx.author.avatar_url
                    embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ") 
                    try:
                        await mbr.send(embed=embed)
                    except:pass

                    try :
                        await ctx.guild.ban(mbr)
                    except:
                        await ctx.send("Failed to Ban!")

                
                else:pass
            
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            if warned_names=="":
                embed.add_field(name="<a:YB_Wumpus_Ban:781419747878633492> | Ban command not Executed",value=f"Nobody was banned.This could be the cause of :\n • Mentioned user is not found.\n • Mentioned user is are above/equal to your role.\n • You mentioned yourself (in that case you need to go get your brain checked up).")
            else:
                embed.add_field(name="<a:YB_Wumpus_Ban:781419747878633492> | Banned command Executed",value=f" \"**{warned_names}**\"was banned for \"**{reason}**\".")
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")    
            await ctx.send(embed=embed)
           
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Kick", help='Kicks a user \n \"Yeet Ban @User <reason>\" or \"Yeet Kick @User @User <reason>\"')
    async def kick(self,ctx, members: commands.Greedy[discord.Member], *, reason='violation of rules'):
            warned_names=""
            for mbr in members:
                
                if mbr == ctx.author: pass
                
                elif mbr.top_role < ctx.author.top_role or ctx.author==ctx.guild.owner:
                        embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
                        embed.add_field(name=":boot: | Kicked",value=f"You have been kicked from \"**{ctx.guild.name}**\" for \"**{reason}**\".") 
                        author_avatar=ctx.author.avatar_url
                        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ") 
                        
                        try:await mbr.send(embed=embed)
                        except: pass
                        
                        try : await mbr.kick(reason=reason)
                        except : await ctx.send("Failed to Kick!")
                        warned_names=warned_names+mbr.name+", "

                else: pass
            
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            if warned_names=="":
                embed.add_field(name=":boot: | Kick command not Executed",value=f"Nobody was kicked.This could be the cause of :\n • Mentioned user is not found.\n • Mentioned user is are above/equal to your role.\n • You mentioned yourself (in that case you need to go get your brain checked up). \n Make sure the user you are trying to kick is below my highest role.")
            else:
                embed.add_field(name=":boot: | Kick command Executed",value=f" \"**{warned_names}**\"was kicked for \"**{reason}**\".")
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")    
            await ctx.send(embed=embed)
         
    



    def time_format_function(self,time):
        time_inputted = time
        time_inputted.strftime("%Y")
        time_inputted.strftime("%m")
        time_inputted.strftime("%d")
        time_inputted.strftime("%H:%M:%S")
        output_time = time_inputted.strftime("%d/%m/%Y (D/M/Y), %H:%M:%S")
        return output_time
           


def setup(bot):
    bot.add_cog(Utility(bot))
        