import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap,re
from discord.ext import commands,tasks
import config

colourlist=config.embed_colours

class Utility(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    # @commands.cooldown(1, 3, commands.BucketType.user)
    # @commands.command(name="Invite", help='Sends Invite link for bot \n sw invite ')
    # async def invite(self,ctx):
    #     embed= discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
    #     #insert_field_at(index, *, name, value, inline=True)¶
    #     embed.add_field(name="You can invite me here:",value="[Direct Invite](https://discord.com/oauth2/authorize?client_id=787894718474223616&permissions=0&scope=bot)",inline=False)
    #     #embed.add_field(name="Join our Discord Support Server:",value="[Discord Server](https://discord.gg/C3XkFwrdER)",inline=False)
    #     #embed.add_field(name="Mail for business enquiries:",value="yeetbotdev@gmail.com",inline=False)
    #     author_avatar=ctx.author.avatar_url
    #     embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
    #     await ctx.send(embed=embed)
    
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Info",aliases=['botinfo'], help=f'Returns bot information \n {config.prefix}Info \nAliases: serverstats ')
    async def info(self,ctx):
        embed=discord.Embed(title="Bot Info",color = random.choice(colourlist),timestamp=ctx.message.created_at)
        embed.add_field(name="Created by:",value=f"Shri30yans",inline=False)
        embed.add_field(name="Prefix",value=f"{config.prefix}",inline=False)
        embed.add_field(name="Servers:",value=f"{str(len(self.bot.guilds))}",inline=False)
        embed.add_field(name="Users:",value=f"{str(len(self.bot.users) + 1)}",inline=False)
        embed.add_field(name="Logged in as:",value=f"{self.bot.user.name}",inline=False)
        embed.add_field(name="Discord.py API version:",value=f"{discord.__version__}",inline=False)
        embed.add_field(name="Python version:",value=f"{platform.python_version()}",inline=False)
        embed.add_field(name="Running on:",value=f"{platform.system()} {platform.release()} ({os.name})",inline=False)
        #embed.add_field(name="Support server",value=f"[Join the support server.](https://top.gg/bot/750236220595896370/vote)",inline=False)
        #embed.add_field(name="Vote",value=f"[Top.gg Vote](https://top.gg/bot/750236220595896370/vote)",inline=False)
        embed.set_thumbnail(url=str(self.bot.user.avatar_url)) 
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
        await ctx.reply(embed=embed)
        

    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Ping", help=f'Tells the Ping of a server \n{config.prefix}ping')
    async def ping(self,ctx):
        """ Pong! """
        message = await ctx.reply(embed=discord.Embed(title="Ping",description=":Pong!  :ping_pong:",color = random.choice(colourlist),timestamp=ctx.message.created_at))
        ping = (message.created_at.timestamp() - ctx.message.created_at.timestamp()) * 1000
        embed=discord.Embed(title="Ping",description=f'Pong!  :ping_pong:  \nBot latency: {int(ping)}ms\nWebsocket latency: {round(self.bot.latency * 1000)}ms',color = random.choice(colourlist),timestamp=ctx.message.created_at)
        embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
        await message.edit(embed=embed)
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="ServerInfo",aliases=['serverstats','server'], help=f'Finds server stats \nFormat: {config.prefix}stats \nAliases: serverstats, server ')
    async def stats(self,ctx):
            #f-strings
            guild_owner=str(ctx.guild.owner)
            embed=discord.Embed(title="Server Stats",color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.add_field(name="Name",value=f"{ctx.guild.name}",inline=False)
            if (ctx.message.author.id == ctx.guild.owner_id):
                embed.add_field(name="Owner",value="You are the owner of this server.",inline=False)
            else:
                embed.add_field(name="Owner",value=f"{guild_owner}, is the owner of this server.")   
            
            #Member calculator
            no_of_members=0
            no_of_bots=0
            for member in ctx.guild.members:
                if member.bot:
                    no_of_bots=no_of_bots+1
                else:
                    no_of_members=no_of_members+1

            embed.add_field(name="Region",value=f"{str(ctx.guild.region).capitalize() }",inline=False)
            embed.add_field(name="Members",value=f"Members in server: {no_of_members}")
            embed.add_field(name="Bots",value=f"Bots in server: {no_of_bots}",inline=False)
            embed.add_field(name="Roles",value=f"Number of roles: {len(ctx.guild.roles)}")
            created_at_time=self.time_format_function(ctx.guild.created_at)
            embed.add_field(name="Creation date",value=f"{created_at_time}",inline=False) 
            embed.set_thumbnail(url=str(ctx.guild.icon_url)) 
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.reply(embed=embed)
    
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.command(name="Delete",aliases=['del', 'clear'], help=f'Deletes messages \nFormat: `{config.prefix}delete <number_of _messages>` \n Aliases: clear, del')
    async def delete(self,ctx,num:int):
        if num>100:
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.add_field(name="Too many messages deleted.",value=f"You can delete a maximum of 100 messages at one go to prevent excessive deleting. ") 
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.reply(embed=embed,delete_after=4)

        else:
            await ctx.channel.purge(limit=num+1,bulk=True)
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.add_field(name="Deleted",value=f"Deleted {num} message(s)") 
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.reply(embed=embed,delete_after=4)
    

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Whois",aliases=["userinfo"], help=f'Shows information of a user \nFormat: `{config.prefix}whois @User`\nAliases: userinfo')
    async def whois(self,ctx,user:discord.Member=None):
        if (user == None):
            user_mention= ctx.author
        else:
            user_mention=user
        embed=discord.Embed(title = f"{user_mention.name}",color =random.choice(colourlist), timestamp=ctx.message.created_at)
        embed.add_field(name="Status:",value=f"{user_mention.raw_status.capitalize()}")
        joined_on_time=self.time_format_function(user_mention.joined_at)
        embed.add_field(name="Joined server at:",value=f"{joined_on_time}")
        embed.add_field(name="Nickname:",value=f"{user_mention.nick}")
        
        roles_mention_form=[]
        for role in user_mention.roles:
            roles_mention_form.append(role.mention)
        roles_mention_form.pop(0)
        roles_mention_form.reverse()
        roles_mention_string =  ' '.join(roles_mention_form)
        embed.add_field(name="Roles:",value=f"{roles_mention_string}")
        made_on_time=self.time_format_function(user_mention.created_at)
        embed.add_field(name="Account made on:",value=f"{made_on_time}")
        embed.add_field(name="User ID:",value=f"{user_mention.id}")
        #embed.add_field(name="",value=f"{user_mention.}")
        #embed.add_field(name="",value=f"{user_mention.}")
        #embed.add_field(name="",value=f"{user_mention.}")
        embed.set_thumbnail(url=str(user_mention.avatar_url)) 

        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
        await ctx.reply(embed=embed)
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="PFP",aliases=['dp', 'avatar','av'], help=f'Shows the avatar of a user \nFormat: `{config.prefix}pfp @User`\nAliases: DP, Avatar ')
    async def pfp(self,ctx,user:discord.Member=None):
        if (user == None):
            user_mention= ctx.author
        else:
            user_mention=user
        embed=discord.Embed(title = f"Avatar of {user_mention.name}", color =random.choice(colourlist), timestamp=ctx.message.created_at)
        embed.set_image(url=user_mention.avatar_url)
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
        await ctx.send(embed=embed)    
            
    '''@commands.group(name="settings", help='control bot settings',invoke_without_command=True,case_insensitive=True)
    async def settings(self,ctx):
        embed=discord.Embed(color = random.choice(colourlist))
        embed.add_field(name="No Setting specified",value=f"Enter a setting, dumbass")
        embed.set_footer(text="| {self.bot.user.name} |")
        await ctx.send(embed=embed)'''
    
    @commands.has_permissions(manage_messages=True)
    #@commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Warn", help=f'Warns a user to stop doing a certain activity \n \"{config.prefix}Warn @User <reason>\" or \"{config.prefix}Warn @User @User <reason>\"')
    async def warn(self,ctx, members: commands.Greedy[discord.Member], *, reason='violation of rules'):
            warned_names=""
            disabled_dm=""
            for mbr in members:
                
                if mbr == ctx.author: 
                    pass
                
                elif mbr.bot: 
                    pass
                
                elif mbr.top_role < ctx.author.top_role or ctx.author==ctx.guild.owner:
                    embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
                    embed.add_field(name="<:warn:789487083802460200> | Warning",value=f"You have been warned for \"**{reason}**\" in \"**{ctx.guild.name}**\". Repeated violation of rules could lead to a ban. Please ensure such behaviour is not repeated again.") 

                    author_avatar=ctx.author.avatar_url
                    embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ") 
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
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")    
            await ctx.reply(embed=embed)
        
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    #@commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Ban", help=f'Bans a user \n\"{config.prefix}Ban @User <reason>\" or \"{config.prefix}Ban @User @User <reason>\"')
    async def ban(self,ctx, members: commands.Greedy[discord.Member], *, reason='violation of rules'):
            warned_names=""
            for mbr in members:
                if mbr == ctx.author: 
                    pass
                
                elif mbr.top_role < ctx.author.top_role or ctx.author==ctx.guild.owner:
                    embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
                    embed.add_field(name="<a:YB_Wumpus_Ban:781419747878633492> | Banned",value=f"You have been banned for \"**{reason}**\" in \"**{ctx.guild.name}**\".") 
                    author_avatar=ctx.author.avatar_url
                    embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ") 
                    
                    try:
                        await mbr.send(embed=embed)
                    except:
                        pass

                    try:
                        await ctx.guild.ban(mbr)
                    except:
                        await ctx.send("Failed to Ban!")
                
                else:pass
            
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            if warned_names=="":
                embed.add_field(name="<a:YB_Wumpus_Ban:781419747878633492> | Ban command not Executed",value=f"Nobody was banned.This could be the cause of :\n • Mentioned user is not found.\n • Mentioned user is are above/equal to your role.\n • You mentioned yourself (in that case you need to go get your brain checked up).\n**Make sure the user you are trying to kick is below my highest role.**")
            else:
                embed.add_field(name="<a:YB_Wumpus_Ban:781419747878633492> | Banned command Executed",value=f" \"**{warned_names}**\"was banned for \"**{reason}**\".")
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} •{self.bot.user.name}")    
            await ctx.send(embed=embed)
           
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    #@commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Kick", help=f'Kicks a user \n \"{config.prefix}Kick @User <reason>\" or \"{config.prefix}Kick @User @User <reason>\"')
    async def kick(self,ctx, members: commands.Greedy[discord.Member], *, reason='violation of rules'):
            warned_names=""
            for mbr in members:
                
                if mbr == ctx.author: pass
                
                elif mbr.top_role < ctx.author.top_role or ctx.author==ctx.guild.owner:
                        embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
                        embed.add_field(name=":boot: | Kicked",value=f"You have been kicked from \"**{ctx.guild.name}**\" for \"**{reason}**\".") 
                        author_avatar=ctx.author.avatar_url
                        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name}") 
                        
                        try:await mbr.send(embed=embed)
                        except: pass
                        
                        try : await mbr.kick(reason=reason)
                        except : await ctx.send("Failed to Kick!")
                        warned_names=warned_names+mbr.name+", "

                else: pass
            
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            if warned_names=="":
                embed.add_field(name=":boot: | Kick command not Executed",value=f"Nobody was kicked.This could be the cause of :\n • Mentioned user is not found.\n • Mentioned user is are above/equal to your role.\n • You mentioned yourself (in that case you need to go get your brain checked up). \n **Make sure the user you are trying to kick is below my highest role.**")
            else:
                embed.add_field(name=":boot: | Kick command Executed",value=f" \"**{warned_names}**\"was kicked for \"**{reason}**\".")
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")    
            await ctx.reply(embed=embed)
    
    @commands.has_permissions(manage_messages=True)
    #@commands.cooldown(1, 10, commands.BucketType.user)
    @commands.group(name="Giveaway", help=f'Creates a giveaway \n \"{config.prefix}giveaway\"',invoke_without_command=True)
    async def giveaway(self,ctx):
        channel = await self.text_input_function(ctx,title="Which channel do you want your giveaway to be in?",text="Mention the channel in which the giveaway would be created.")
        channel=await commands.TextChannelConverter().convert(ctx,channel)
        prize = await self.text_input_function(ctx,title="What is the prize for the Giveaway?",text="Enter what is the prize.")
        no_of_winners = int(await self.text_input_function(ctx,title="How many winners do you want?",text="Enter a number. Negative numbers and Zero is not allowed."))
        if no_of_winners < 0 :
            await ctx.reply("You can't have a negative winner, dude.")
        elif no_of_winners == 0 :
            await ctx.reply("No winner? You need to have atleast 1 winner, dumbo.")
        time = await self.text_input_function(ctx,title="How long will the giveaway last?",text="Enter the time")
        pos = ["s","m","h","d"]
        time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}
        unit = time[-1]
        if unit not in pos:
            await ctx.reply(f"You didn't answer with a proper unit. Use (s|m|h|d) next time!")
            return
        try:
            val = int(time[:-1])
        except:
            await ctx.reply(f"The time can only be an integer. Please enter an integer next time.")
            return

        time_secs= val * time_dict[unit]
        #print(channel)
        #giveaway_msg = await channel.send(f"{prize} is being given away for {time}")
        embed=discord.Embed(title=f":gift: |  Giveaway!",description=f"{prize}",color = 0xFF0000)
        if no_of_winners == 1:
            embed.add_field(name="React with :tada: to enter!",value=f"{no_of_winners} winner")
        elif no_of_winners > 1:
            embed.add_field(name="React with :tada: to enter!",value=f"{no_of_winners} winners")
        embed.set_footer(text=f"Ends in {time} • {self.bot.user.name} ")    
        giveaway_msg = await channel.send(embed=embed)
        await giveaway_msg.add_reaction("\U0001f389")
        await asyncio.sleep(int(time_secs))
        # print(giveaway_msg.reactions)
        # winner=random.choice(giveaway_msg.reactions)
        # await ctx.send(f"{winner.user.mention} won the giveaway")
        new_msg = await channel.get_message(giveaway_msg.id)
        giveaway_msg = new_msg
        users = await giveaway_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        if no_of_winners > len(users):
            no_of_winners = len(users)
        winner = random.sample(users,k=no_of_winners)
        winner_list=""
        for user in winner:
            winner_list= winner_list + user.mention
        embed=discord.Embed(title=f":tada: |  Giveaway ended.",description=f"{prize}",color = 0xFF0000)
        embed.add_field(name=f":trophy: Winner: ",value=f"{winner_list} won {prize}!")
        embed.set_footer(text=f"Ended • {self.bot.user.name} ")    
        await giveaway_msg.edit(embed=embed)
        await channel.send(f"Congratulations! {winner_list} won {prize}!")

    # @commands.has_permissions(manage_messages=True)
    # #@commands.cooldown(1, 10, commands.BucketType.user)
    # @giveaway_msg.group(name="reroll", help=f'Reroll a giveaway. \n \"{config.prefix}reroll giveaway_message_id\"')
    # async def reroll_giveaway(self,ctx,giveaway_msg_id):
    #     giveaway_msg = await channel.get_message(giveaway_msg_id)
    #     users = await giveaway_msg.reactions[0].users().flatten()
    #     users.pop(users.index(self.bot.user))
    #     if no_of_winners > len(users):
    #         no_of_winners = len(users)
    #     winner = random.sample(users,k=no_of_winners)
    #     winner_list=""
    #     for user in winner:
    #         winner_list= winner_list + user.mention
    #     embed=discord.Embed(title=f":tada: |  Giveaway ended.",description=f"{prize}",color = 0xFF0000)
    #     embed.add_field(name=f":trophy: Winner: ",value=f"{winner_list} won {prize}!")
    #     embed.set_footer(text=f"Ended • {self.bot.user.name} ")    
    #     await giveaway_msg.edit(embed=embed)
    #     await channel.send(f"Congratulations! {winner_list} won {prize}!")
    
    @commands.has_permissions(manage_messages=True)
    #@commands.cooldown(1, 10, commands.BucketType.user)
    @commands.group(name="Poll", help=f'Creates a poll \n \"{config.prefix}poll [Question] Option1,Option2,Option3\"',require_var_positional=True)#require_var_positional=True makes sure input is not empty
    async def poll(self,ctx,*arguments):
        number_emojis=[
                    "1\N{variation selector-16}\N{combining enclosing keycap}",
                    "2\N{variation selector-16}\N{combining enclosing keycap}",
                    "3\N{variation selector-16}\N{combining enclosing keycap}",
                    "4\N{variation selector-16}\N{combining enclosing keycap}",
                    "5\N{variation selector-16}\N{combining enclosing keycap}",
                    "6\N{variation selector-16}\N{combining enclosing keycap}",
                    "7\N{variation selector-16}\N{combining enclosing keycap}",
                    "8\N{variation selector-16}\N{combining enclosing keycap}",
                    "9\N{variation selector-16}\N{combining enclosing keycap}",
                    "\N{keycap ten}",]

        response =  ' '.join(arguments)
        result = re.search('\[(.*)\]', response) #regex to find string between [ ]
        question = result.group(1)
        options = response.replace(f"[{question}]","").split(",")
        
        if len(options) > 10:
            await ctx.send("You inputted too many options. Maximum options is 10.")
        
        elif len(options) <= 1:
            await ctx.send("You inputted too less options. Minimum options is 2.")


        #Proper outcome. There is a question and 1-10 Options
        elif question !=None:
            embed=discord.Embed(title=f"{question.capitalize()}",color = random.choice(colourlist),timestamp=ctx.message.created_at)
            
            optionnum=0
            for option in options:
                bar_string, percent=self.bar_generator(count=0,total=len(options))
                embed.add_field(name=f"{number_emojis[optionnum]} {option.lstrip().capitalize()}",value=f"`{bar_string}` | {percent}% | (0)",inline=False)
                optionnum +=1
            
            embed.set_footer(text=f"You may choose only one option • {self.bot.user.name} ") 
            PollMessage = await ctx.send(embed=embed)
            
            for num in range(0,len(options)):#react with the options
                reaction=number_emojis[num]
                await PollMessage.add_reaction(reaction)
            
            await PollMessage.add_reaction("\U0000274c")

            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():

                    server_info = await connection.fetchrow("SELECT * FROM server_info WHERE id=$1",ctx.guild.id)
                    ongoing_polls=json.loads(server_info["ongoing_polls"])
                    
                    ongoing_polls_list=ongoing_polls["polls"]
                    ongoing_polls_list.append(PollMessage.id)
                    
                    ongoing_polls_j=json.dumps(ongoing_polls)
                    await connection.execute("UPDATE server_info SET ongoing_polls = $1 WHERE id=$2",ongoing_polls_j,ctx.guild.id)

        else:
            await ctx.send("Invalid syntax")
     

    async def update_poll(self,PollMessage,emoji,user,type_of_event):    #type of event = reaction_add, reaction_remove
        #print("update",str(emoji))      
        if str(emoji)== "\U0000274c" and type_of_event =="reaction_add":#If cross is selected
            member=PollMessage.guild.get_member(user.id)
            if member.guild_permissions.manage_messages == True or user.id == self.bot.owner_id:
                embed=PollMessage.embeds[0]
                embed.description=f"This poll is ended."
                embed.set_footer(text=f"Ended by {user.name} • {self.bot.user.name} ")
                #embed.insert_field_at(0, name="", value="", inline=True)
                await PollMessage.edit(embed=embed)
                await PollMessage.clear_reactions()

                async with self.bot.pool.acquire() as connection:
                    async with connection.transaction():
                        server_info = await connection.fetchrow("SELECT * FROM server_info WHERE id=$1",PollMessage.guild.id)
                        ongoing_polls=json.loads(server_info["ongoing_polls"]) #load the json content of  ongoing_polls
                        ongoing_polls_list=ongoing_polls["polls"] #fetch the list of all ids
                        ongoing_polls_list.remove(PollMessage.id)  #remove that id           
                        ongoing_polls_j=json.dumps(ongoing_polls) #change back to json
                        await connection.execute("UPDATE server_info SET ongoing_polls = $1 WHERE id=$2",ongoing_polls_j,PollMessage.guild.id)   
            else:
                #user with no manage_message perms react = delete their reaction
                await PollMessage.remove_reaction(emoji, user)

        else:  
            number_emojis=[
                    "1\N{variation selector-16}\N{combining enclosing keycap}",
                    "2\N{variation selector-16}\N{combining enclosing keycap}",
                    "3\N{variation selector-16}\N{combining enclosing keycap}",
                    "4\N{variation selector-16}\N{combining enclosing keycap}",
                    "5\N{variation selector-16}\N{combining enclosing keycap}",
                    "6\N{variation selector-16}\N{combining enclosing keycap}",
                    "7\N{variation selector-16}\N{combining enclosing keycap}",
                    "8\N{variation selector-16}\N{combining enclosing keycap}",
                    "9\N{variation selector-16}\N{combining enclosing keycap}",
                    "\N{keycap ten}",]

            # reaction_count=0
            # for reaction in PollMessage.reactions:
            #     reacted_users = await reaction.users().flatten()
            #     if user in reacted_users and str(reaction.emoji) in number_emojis:
            #         reaction_count+=1
            # print(reaction_count)
            # if reaction_count >1:
            #     await user.send("You can only react to one option. Please uncheck your current choice then select another option.")
            #     await PollMessage.remove_reaction(emoji, user)


            # if type_of_event == "reaction_add":          
            #     for reaction in PollMessage.reactions:#checks all reactions of message
            #         if (str(reaction.emoji) in number_emojis) and (str(reaction.emoji) != str(emoji)) and reaction_count > 1 :
            #             print("del",str(reaction.emoji),str(emoji))
            #             await PollMessage.remove_reaction(reaction.emoji, user)

            reactions_count_dict={}
            total_reactions=0
            for r in PollMessage.reactions:
                if r.me and str(r.emoji) in number_emojis :
                    reactions_count_dict[str(r.emoji)] = r.count-1
                    total_reactions+=r.count-1  


            embed=PollMessage.embeds[0]
            embed_fields=embed.fields
            for x in embed_fields:
                count=reactions_count_dict[x.name[0:3]]
                bar_string, percent=self.bar_generator(count=count,total=total_reactions)                
                embed.set_field_at(embed_fields.index(x),name=f"{x.name}", value=f"`{bar_string}` | {percent}% | ({count})", inline=False)
            await PollMessage.edit(embed=embed)

    def bar_generator(self,count,total):
        if total == 0 :#prevent zero division error
            total = 1
        percent=round(count/total * 100,1)
        bar_count=round(percent/100*20)
        bars_string='█' * bar_count
        bars_string=bars_string + " " * (20-len(bars_string))
        return bars_string,percent

   
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    #@commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Mute", help=f'Mutes a user \n \"{config.prefix}Mute @User 5m\" or \"{config.prefix} mute @User @User 10m\". Time can be entered in (s|m|h|d), Default time is 10 mins.')
    async def mute(self,ctx,members: commands.Greedy[discord.Member],time:str="5m"):
            warned_names=""
            pos = ["s","m","h","d"]
            time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}
            unit = time[-1]
            if unit not in pos:
                await ctx.send(f"You didn't answer with a proper unit. Use (s|m|h|d) next time!")
                return
            try:
                val = int(time[:-1])
            except:
                await ctx.send(f"The time can only be an integer. Please enter an integer next time.")
                return
            time_secs= val * time_dict[unit]
            
            role = discord.utils.get(ctx.guild.roles, id=config.muted_role_id)
            if role == None:
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                if role == None:
                    await ctx.send("The muted role was not found.")
                    return
            #role = discord.utils.get(ctx.guild.roles, name="Muted")
            
            for mbr in members:
                
                if mbr == ctx.author: pass
                
                elif mbr.top_role < ctx.author.top_role or ctx.author==ctx.guild.owner:
                    
                    embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
                    embed.add_field(name=":mute: | Muted",value=f"You have been muted from \"**{ctx.guild.name}**\" for \"**{time}**\".") 
                    author_avatar=ctx.author.avatar_url
                    embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ") 
                    
                    try:await mbr.send(embed=embed)
                    except: 
                        pass
                        #print("Cound not send Dm")
                    
                    try: 
                        await mbr.add_roles(role)
                        warned_names=warned_names+mbr.mention+", "
                    except : 
                        await ctx.send("Failed to mute!")
                else: pass
            
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            if warned_names=="":
                embed.add_field(name=":mute: | Mute command not executed",value=f"Nobody was muted.This could be the cause of :\n • Mentioned user is not found.\n • Mentioned user is are above/equal to your role.\n • You mentioned yourself \n **Make sure the mentioned user and the mute role is below my highest role.**")
            else:
                embed.add_field(name=":mute: | Mute command executed",value=f"**{warned_names}** was muted for **{time}**!")
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} •{self.bot.user.name} ")    
            await ctx.send(embed=embed)

            await asyncio.sleep(int(time_secs))
            for mbr in members:
                try : 
                    await mbr.remove_roles(role)

                except : 
                    await ctx.send("Failed to unmute!")
    
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Createmuterole", help=f'Mutes a user \n \"{config.prefix}Mute @User 5m\" or \"{config.prefix} mute @User @User 10m\". Time can be entered in (s|m|h|d), Default time is 10 mins.')
    async def createmuterole(self,ctx):
        embed=discord.Embed(title='Creating Muted role',description="Creating the role...")
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")   
        message=await ctx.send(embed=embed)
        mute_role = await ctx.guild.create_role(name="Muted", reason="Muted role")
        embed=discord.Embed(title='Creating Muted role',description="Setting permissions...")
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")   
        await message.edit(embed=embed)
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False)
        embed=discord.Embed(title='Creating Muted role',description=f"Created a muted role: {mute_role.mention}")
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")   
        await message.edit(embed=embed)


        # mute_role = await ctx.guild.create_role(name="No Emojis", reason="Spin the Wheel")
        # await message.edit(embed=embed)
        # for channel in ctx.guild.channels:
        #     await channel.set_permissions(mute_role, add_reactions=False, use_external_emojis=False)
        # embed=discord.Embed(title='Creating role',description=f"Created a role: {mute_role.mention}")
        # embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")   
        # await message.edit(embed=embed)





    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Unmute", help=f'Unmutes a user \n \"{config.prefix}Unmute @User 5m\" or \"{config.prefix}unmute @User @User 10m\".')
    async def unmute(self,ctx,members: commands.Greedy[discord.Member]):
            warned_names=""
            role = discord.utils.get(ctx.guild.roles, id=config.muted_role_id)
            if role == None:
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                if role == None:
                    embed = discord.Embed(title=f"Muted role not found.",description=f"Name your muted role \"Muted\". ")
                    await ctx.send(embed=embed)
                    return  

            for mbr in members:
                
                if mbr == ctx.author: pass
                
                elif mbr.top_role < ctx.author.top_role or ctx.author==ctx.guild.owner:                  
                    try : 
                        await mbr.remove_roles(role)
                        warned_names=warned_names+mbr.mention+", "
                    except : 
                        await ctx.send("Failed to unmute!")
                else: pass
            
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            if warned_names=="":
                embed.add_field(name=":speaker:  | Unmute command not executed",value=f"Nobody was unmuted. This could be the cause of :\n • Mentioned user is not found.\n • Mentioned user is are above/equal to your role.\n • You mentioned yourself. \n **Make sure the mentioned user and the mute role is below my highest role.**")
            else:
                embed.add_field(name=":speaker:  | Unmute command executed",value=f"**{warned_names}** was unmuted,")
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")    
            await ctx.send(embed=embed)

    async def text_input_function(self,ctx,title:str,text:str):
        question_embed=await ctx.send(embed=discord.Embed(title =title,description=text,color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} •{self.bot.user.name} "))
        try:
            text= await self.bot.wait_for('message', timeout=30.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            await question_embed.edit(embed=discord.Embed(title ="Timeout Error",description="You took too much time, ya retarded monkey",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} "))
        else: 
            if len(text.content)> 50:
                embed=discord.Embed(title="<:warn:789487083802460200> | Too many Characters ",color = random.choice(colourlist))
                embed.add_field(name="Type only 50 characters in your sentence.",value=f"You typed {len(text.content)} letters. Type the text again.", inline=False)
                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
                await ctx.send(embed=embed)
                return await self.text_input_function(ctx,title,text)
            else:
                return str(text.content)


    
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
        