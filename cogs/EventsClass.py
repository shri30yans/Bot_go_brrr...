import os, sys, discord, platform, random, aiohttp, json,time,asyncio
from discord.ext import commands,tasks
import config
import cogs.EconomyCog as EconomyCog
colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
            0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]




class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.status_update.start()#pylint: disable=no-member
        # Ignore this error.It is a linter warning.
  



        #except Exception as error:
            #return'''
        
        
        #await self.bot.process_commands(message)







    # @commands.Cog.listener() #if in cog
    # async def on_message(self,message):
        
    #         #stringmsg=message.content.lower()
            
    #         if message.author == self.bot.user:
    #             return

    #         elif message.author.id == 682899218695847974:
    #             await message.add_reaction("<:Reaction_BAN:748810314375495720>")
            
    #         await self.bot.process_commands(message)


    # @tasks.loop(seconds=300)
    # async def status_update(self):
    #     await self.bot.wait_until_ready()
    #     await self.bot.change_presence(status = discord.Status.online, activity =discord.Activity(type = discord.ActivityType.listening, name = f' to \"Yeet help\" in {str(len(self.bot.guilds))} Servers with {str(len(self.bot.users) + 1)} users.'))


    # @commands.Cog.listener()
    # async def on_command_completion(self,ctx):
    #     #await ctx.message.add_reaction("\U00002705")
    #     fullCommandName = ctx.command.qualified_name
    #     split = fullCommandName.split(" ")
    #     executedCommand = str(split[0])
    #     embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
    #     embed.add_field(name="Command Executed",value=f"Executed {executedCommand} command in {ctx.guild.name} by {ctx.message.author} (ID: {ctx.message.author.id})") 
    #     author_avatar=ctx.author.avatar_url
    #     embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
    #     commands_updates_channel=self.bot.get_channel(780683552827899904) 
    #     await commands_updates_channel.send(embed=embed) 
    
    # @commands.Cog.listener()
    # async def on_guild_join(self,guild): #when the bot joins a new guild)
    #     embed=discord.Embed(color = random.choice(colourlist))
    #     embed.add_field(name="New Guild! Yeet!",value=f"Just joined {guild.name}! (ID: {guild.id}. \n I am now in {str(len(self.bot.guilds))} servers! )") 
    #     embed.set_thumbnail(url=str(guild.icon_url))
    #     #author_avatar=ctx.author.avatar_url
    #     #embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
    #     new_guild_updates_channel=self.bot.get_channel(780683709179232256)
    #     await new_guild_updates_channel.send(embed=embed)

    # #discord.on_guild_remove(guild)
    # @commands.Cog.listener()
    # async def on_guild_remove(self,guild): #when the bot leaves a guild)
    #     embed=discord.Embed(color = random.choice(colourlist))
    #     embed.add_field(name="Oh no",value=f"Just left {guild.name}. <:sadcat_thumbsup:780697920395280425> (ID: {guild.id}. \n I am now in {str(len(self.bot.guilds))} servers. )") 
    #     embed.set_thumbnail(url=str(guild.icon_url))
    #     #author_avatar=ctx.author.avatar_url
    #     #embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
    #     left_guild_updates_channel=self.bot.get_channel(780706537664413706)
    #     await left_guild_updates_channel.send(embed=embed)
    
# @commands.Cog.listener()
#     async def on_message(self,message): #When @Yeet Bot in message
#         if bot.user in message.mentions:
#             embed = discord.Embed(title="Yeet Bot",description="Hi! I am Yeet Bot, the biggest gangsta in this server.\n My prefix is \"yeet\" and \"y\". Type \"yeet help\" to get started.  ",color = random.choice(colourlist))
#             embed.set_footer(text="Yeet Bot | Developed by Shri30yans")
#             await message.channel.send(embed=embed)

#     bot.snipes = {}

# @commands.Cog.listener()
#     async def on_message_delete(self,message):
#         if (message.author.id== 571957935270395925):
#             return 
#         elif (message.author.id== bot.user.id):
#             return 
#         else:
#             bot.snipes[message.channel.id] = message
            
            

# @bot.event#@commands.Cog.listener() if in cog
#     async def on_message(message):
        
#             stringmsg=message.content.lower()
            
#             if message.author == bot.user:
#                 return
#             if "lol" in stringmsg:
#             if autotrigger_mode==True:
#                     #response = "Not funny, lol"
#                     #await message.channel.send(response)
#                     await message.channel.send("<:okboomer:774171875906682890>")
#             if "tahir" in stringmsg:
#                 if autotrigger_mode==True:
#                     response = "Tahir = Dum. lol"
#                     await message.channel.send(response)
        
#             if stringmsg == "f":
#                 if autotrigger_mode==True:
#                     response = "F in the chat, Bois"
#                     await message.channel.send(response)
            
#             if "yeet" in stringmsg:
#                 if autotrigger_mode==True:
#                     response = "Yeet!"
#                     await message.channel.send(response)
#                     await message.channel.send("https://www.youtube.com/watch?v=vYTB4grjw9o&ab_channel=CyclingScientist") 
#                     #await message.channel.send(file=yeet_mp3)#yeetmp3
            
#             await bot.process_commands(message)

def setup(bot):
    bot.add_cog(Events(bot))