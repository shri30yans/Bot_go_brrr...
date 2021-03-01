import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks

colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
            0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]

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
    #     embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
    #     await ctx.send(embed=embed)
    
    
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
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Delete",aliases=['del', 'clear'], help='Deletes messages \n Yeet delete <number_of _messages> \n Aliases: clear, del')
    async def delete(self,ctx,num:int):
        if ctx.message.author.guild_permissions.manage_messages == True or ctx.author.id == 571957935270395925 :
            if ctx.me.guild_permissions.manage_messages == True:
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
            else:
                embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
                embed.add_field(name="No Permissions",value=f"Yeet Bot doesn't have permission to delete messages. Please ask your server Adminstrator's to update the Manage Messages permission to use this command.") 
                author_avatar=ctx.author.avatar_url
                embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")   
                await ctx.send(embed=embed,delete_after=4)
        else:
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.add_field(name="No Permissions",value=f"{ctx.author.mention} You need the Manage Messages permission to use this command.") 
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")   
            await ctx.send(embed=embed,delete_after=4)
    
    '''@commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Translate", help="Performs a wikipedia search \n Yeet translate Yeet ")
    async def translate(self,ctx,*arguments:str):
        
        translator = Translator()
        response=translator.translate(arguments)

            
        embed = discord.Embed(title = "Translate", color = random.choice(colourlist),timestamp=ctx.message.created_at)
        embed.add_field(name="Translate",value=response)
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)'''


            
            

            #print(response.text)

    # @commands.cooldown(1, 3, commands.BucketType.user)
    # @commands.command(name="Vote", help='Where to vote for me. \n Yeet Vote')
    # async def vote(self,ctx):
    #     # vote_gifs=["https://media.tenor.com/images/a5721ade2ad3e7a1a3b45e73b1cd7ed1/tenor.gif",
    #     #             "https://media1.tenor.com/images/5c9138f8641b2fcfec578c435f05eb7c/tenor.gif?itemid=8850374",
    #     #             "https://media1.tenor.com/images/6531e425d01ecb64f5f98671b3b0748e/tenor.gif?itemid=8098999",
    #     #             "https://media1.tenor.com/images/298bfa6dfd5d4539b0d7cff77b030918/tenor.gif?itemid=13876326",
    #     #             "https://media1.tenor.com/images/887f922eed1f9739842d10102ecd650e/tenor.gif?itemid=17361623",
    #     #             "https://media1.tenor.com/images/b2d694309cd638f5b96efa7d9c3cde2a/tenor.gif?itemid=13202036",
    #     #             "https://media.tenor.com/images/be8559bc58ab754e11333ee79a013e1f/tenor.gif",
    #     #             "https://media.tenor.com/images/dc3308583e3dca9ca0e494c0a58c493d/tenor.gif",

    #     #             ]
    #     embed=discord.Embed(title="Vote",description="[If you like Yeet Bot, vote for me on Top.gg to support me.](https://top.gg/bot/750236220595896370/vote)",color = random.choice(colourlist),timestamp=ctx.message.created_at)
    #     author_avatar=ctx.author.avatar_url
    #     #embed.set_image(url=str(random.choice(vote_gifs))) 
    #     embed.set_thumbnail(url="https://qph.fs.quoracdn.net/main-qimg-156cdd2c7c801fff00c4d2a2f6f9b843")
    #     embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
    #     await ctx.send(embed=embed)



    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Whois",aliases=["userinfo"], help='Shows information of a user \n Yeet whois @User')
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
        #roles_mention_form.append(role.mention for role in user_mention.roles)
        for role in user_mention.roles:
            roles_mention_form.append(role.mention)
        #del roles_mention_form[0 :1] 
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
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="PFP",aliases=['dp', 'avatar'], help='Shows the avatar of a user \n Yeet pfp @User\n Aliases: DP, Avatar ')
    async def pfp(self,ctx,user:discord.Member=None):
        if (user == None):
            user_mention= ctx.author
        else:
            user_mention=user
        embed=discord.Embed(title = f"Avatar of {user_mention.name}", color =random.choice(colourlist), timestamp=ctx.message.created_at)
        embed.set_image(url=user_mention.avatar_url)
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)    
            
    '''@commands.group(name="settings", help='control bot settings',invoke_without_command=True,case_insensitive=True)
    async def settings(self,ctx):
        embed=discord.Embed(color = random.choice(colourlist))
        embed.add_field(name="No Setting specified",value=f"Enter a setting, dumbass")
        embed.set_footer(text="| Yeet Bot |")
        await ctx.send(embed=embed)'''
    
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
                embed.add_field(name="<a:YB_Wumpus_Ban:781419747878633492> | Ban command not Executed",value=f"Nobody was banned.This could be the cause of :\n • Mentioned user is not found.\n • Mentioned user is are above/equal to your role.\n • You mentioned yourself (in that case you need to go get your brain checked up).\n**Make sure the user you are trying to kick is below my highest role.**")
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
                embed.add_field(name=":boot: | Kick command not Executed",value=f"Nobody was kicked.This could be the cause of :\n • Mentioned user is not found.\n • Mentioned user is are above/equal to your role.\n • You mentioned yourself (in that case you need to go get your brain checked up). \n **Make sure the user you are trying to kick is below my highest role.**")
            else:
                embed.add_field(name=":boot: | Kick command Executed",value=f" \"**{warned_names}**\"was kicked for \"**{reason}**\".")
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")    
            await ctx.send(embed=embed)
    
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Giveaway", help='Creates a giveaway \n \"Yeet giveaway\"')
    async def giveaway(self,ctx):
        channel = await self.text_input_function(ctx,title="Which channel do you want your giveaway to be in?",text="Mention the channel in which the giveaway would be created.")
        channel=await commands.TextChannelConverter().convert(ctx,channel)
        prize = await self.text_input_function(ctx,title="What is the prize for the Giveaway?",text="Enter what is the prize.")
        no_of_winners = int(await self.text_input_function(ctx,title="How many winners do you want?",text="Enter a number. Negative numbers and Zero is not allowed."))
        if no_of_winners < 0 :
            await ctx.send("You can't have a negative winner, dude.")
        elif no_of_winners == 0 :
            await ctx.send("No winner? You need to have atleast 1 winner, dumbo.")
        time = await self.text_input_function(ctx,title="How long will the giveaway last?",text="Enter the time")
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
        #print(channel)
        #giveaway_msg = await channel.send(f"{prize} is being given away for {time}")
        embed=discord.Embed(title=f":gift: |  Giveaway!",description=f"{prize}",color = 0xFF0000)
        if no_of_winners == 1:
            embed.add_field(name="React with :tada: to enter!",value=f"{no_of_winners} winner")
        elif no_of_winners > 1:
            embed.add_field(name="React with :tada: to enter!",value=f"{no_of_winners} winners")
        embed.set_footer(text=f"Ends in {time} • Yeet Bot ")    
        giveaway_msg = await channel.send(embed=embed)
        await giveaway_msg.add_reaction("\U0001f389")
        await asyncio.sleep(int(time_secs))
        # print(giveaway_msg.reactions)
        # winner=random.choice(giveaway_msg.reactions)
        # await ctx.send(f"{winner.user.mention} won the giveaway")
        new_msg = await channel.fetch_message(giveaway_msg.id)
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
        embed.set_footer(text=f"Ended • Yeet Bot ")    
        await giveaway_msg.edit(embed=embed)
        await channel.send(f"Congratulations! {winner_list} won {prize}!")
    
    # @commands.has_permissions(manage_messages=True)
    # @commands.cooldown(1, 10, commands.BucketType.user)
    # @commands.command(name="Poll", help='Creates a giveaway \n \"Yeet giveaway\"')
    # async def poll(self,ctx):
    #     channel = await self.text_input_function(ctx,title="Which channel do you want your giveaway to be in?",text="Mention the channel in which the giveaway would be created.")
    #     channel =await commands.TextChannelConverter().convert(ctx,channel)
    #     embed=discord.Embed(title="Poll",description=f"React to this message to participate in this poll.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
    #     option_count=1
    #     while True:
    #         question = poll_text_input_function(option_count)
    #         await question.edit(embed=discord.Embed(title ="Poll",description=f"React to this message for the choice \"{question}\"",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
    #         embed.add_field(name=f"Option {option_count}:",value=question)

    #     async def poll_text_input_function(option_count):
    #         question_embed=await ctx.send(embed=discord.Embed(title ="Poll",description=f"What's option {option_count}?",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
    #         try:
    #             text= await self.bot.wait_for('message', timeout=30.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
    #         except asyncio.TimeoutError:
    #             await question_embed.edit(embed=discord.Embed(title ="Timeout Error",description="You took too much time, ya retarded monkey",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
    #         else: 
    #             if len(text.content)> 50:
    #                 embed=discord.Embed(title="<:warn:789487083802460200> | Too many Characters ",description="How many letters will you type, you retard?",color = random.choice(colourlist))
    #                 embed.add_field(name="Type only 50 characters in your sentence.",value=f"You typed {len(text.content)} letters, dumbshit! Type the text again.", inline=False)
    #                 embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
    #                 await ctx.send(embed=embed)
    #                 return await poll_text_input_function(option_count)
    #             else:
    #                 return str(text.content)
                
                


   
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Mute", help='Mutes a user \n \"Yeet Mute @User 5m\" or \"Yeet mute @User @User 10m\". Time can be entered in (s|m|h|d), Default time is 10 mins.')
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
            
            #role = discord.Guild.get_role(self,role_id=748786284385796123)
            role = discord.utils.get(ctx.guild.roles, id=748786284385796123)
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
                    embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ") 
                    
                    try:await mbr.send(embed=embed)
                    except: 
                        pass
                        #print("Cound not send Dm")
                    
                    try : 
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
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")    
            await ctx.send(embed=embed)

            await asyncio.sleep(int(time_secs))
            for mbr in members:
                try : 
                    await mbr.remove_roles(role)

                except : 
                    await ctx.send("Failed to mute!")


    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Unmute", help='Unmutes a user \n \"Yeet Unmute @User 5m\" or \"Yeet unmute @User @User 10m\".')
    async def unmute(self,ctx,members: commands.Greedy[discord.Member]):
            warned_names=""
            #role = discord.Guild.get_role(self,role_id=748786284385796123)
            role = discord.utils.get(ctx.guild.roles, id=748786284385796123)
            if role == None:
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                if role == None:
                    await ctx.send("The muted role was not found.")
                    return
            #role = discord.utils.get(ctx.guild.roles, name="Muted")
            
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
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")    
            await ctx.send(embed=embed)

        



    async def text_input_function(self,ctx,title:str,text:str):
        question_embed=await ctx.send(embed=discord.Embed(title =title,description=text,color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        try:
            text= await self.bot.wait_for('message', timeout=30.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            await question_embed.edit(embed=discord.Embed(title ="Timeout Error",description="You took too much time, ya retarded monkey",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        else: 
            if len(text.content)> 50:
                embed=discord.Embed(title="<:warn:789487083802460200> | Too many Characters ",description="How many letters will you type, you retard?",color = random.choice(colourlist))
                embed.add_field(name="Type only 50 characters in your sentence.",value=f"You typed {len(text.content)} letters, dumbshit! Type the text again.", inline=False)
                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
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
        