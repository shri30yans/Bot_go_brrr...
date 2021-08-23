import os,discord,platform,random,json,asyncio,re
from discord.enums import Status
from discord.ext import commands
import utils.awards as awards
import config
import core.checks as checks
from datetime import datetime
import time

colourlist=config.embed_colours

class Utility(commands.Cog,name="Utility",description="Utilty functions"): 
    def __init__(self, bot):
        self.bot = bot
        self.bot.launch_time = datetime.utcnow()

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






    @commands.cooldown(1,20, commands.BucketType.user)
    @commands.command(name="Prefix",aliases=["prefixes"],help=f"Get the server prefix")
    async def show_prefix(self,ctx):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        prefix = await ImportantFunctions.get_server_prefixes_string(ctx.guild.id)
        embed=discord.Embed(title="Prefix",description="A new prefix can be set by using the command `newprefix`",color = random.choice(colourlist))
        embed.add_field(name=f"Current server prefixes:",value=f"{prefix}")
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await ctx.reply(embed=embed)
    
    
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Info",aliases=['botinfo'], help=f'Returns bot information \nFormat: `{config.default_prefixes[0]}Info` \nAliases: `serverstats` ')
    async def info(self,ctx):
        embed=discord.Embed(title="Bot Info",color = random.choice(colourlist),timestamp=ctx.message.created_at)
        embed.add_field(name="Created by:",value=f"Shri30yans",inline=False)
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        prefix = await ImportantFunctions.get_server_prefixes_string(ctx.guild.id)
        embed.add_field(name="Prefix",value=f"{prefix}",inline=False)
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

    @commands.cooldown(1,10, commands.BucketType.user)
    @commands.command(name="Uptime",help=f"Shows the amount of time the bot has been up.")
    async def uptime(self,ctx):
        async def convert(seconds):
                days = seconds // (3600 *24)
                seconds %= (3600*24)
                hours = seconds // 3600
                seconds %= 3600
                minutes = seconds // 60
                seconds %= 60
                string = ""
                d={"days":days,"hours":hours,"minutes":minutes,"seconds":seconds}
                revised_d={}
                string=""
                for unit in list(d):
                    if d[unit] != 0:
                        revised_d[unit] = d[unit]
                
                for unit in list(revised_d):
                    string += f"{revised_d[unit]} {unit}"
                    if len(revised_d) > 1:
                        if list(revised_d)[-2] == unit:
                            string += " and "
                        elif list(revised_d)[-1] == unit:
                            pass
                        else:
                            string += ", "

                return string
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        string = await convert(int(delta_uptime.total_seconds()))
        await ctx.reply(f"{self.bot.user.name} has been up for {string}")
        

    
    #@commands.cooldown(1,10, commands.BucketType.user)
    @commands.command(name="Ping", help=f'Tells the Ping of a server')
    async def ping(self,ctx):
        """ Pong! """
        start = time.perf_counter()
        message = await ctx.reply(embed=discord.Embed(title=f"{config.loading_reaction}  Pinging",description="Pinging...",color = random.choice(colourlist),timestamp=ctx.message.created_at))
        end = time.perf_counter()
        typing_ping = (end - start) * 1000
        
        start = time.perf_counter()
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.fetchrow("SELECT starboard FROM server_info WHERE id=$1",ctx.guild.id)
        end = time.perf_counter()
        database_ping = (end - start) * 1000

        embed=discord.Embed(title="Ping",color = random.choice(colourlist),timestamp=ctx.message.created_at)
        embed.add_field(name="Typing",value=f"```{int(typing_ping)}ms```",inline=True)
        embed.add_field(name="Websocket",value=f"```{round(self.bot.latency * 1000)}ms```",inline=True)
        embed.add_field(name="Database",value=f"```{round(database_ping)}ms```",inline=True)
        embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
        await message.edit(embed=embed)
    
    @commands.guild_only()
    @commands.cooldown(1,10, commands.BucketType.user)
    @commands.command(name="ServerInfo",aliases=['serverstats','server'], help=f'Finds server stats')
    async def stats(self,ctx):
            embed=discord.Embed(title=f"{ctx.guild.name}",color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.add_field(name="**Information:**",
                            value=f"\n**Name** : `{ctx.guild.name}`\n**Region** : `{str(ctx.guild.region).capitalize()}`\n**ID** : `{ctx.guild.id}`\n**Owner** : `{str(ctx.guild.owner)}`",inline=False)
            
            #Member calculator
            members_offline = 0
            members_online= 0
            members_idle=0
            members_dnd=0

            no_of_bots=0
            for member in ctx.guild.members:
                if member.bot:
                    no_of_bots=no_of_bots+1
                else:
                    if str(member.status) == "online":
                        members_online+=1
                    elif str(member.status) == "dnd":
                        members_dnd+=1
                    elif str(member.status) == "idle":
                        members_idle+=1
                    elif str(member.status) == "offline": 
                        members_offline+=1

                    
                    created_at_time=self.time_format_function(ctx.guild.created_at)
            total_members= members_online+ members_offline + members_idle + members_dnd

            embed.add_field(name="**Statistics:**",
            value=f"**Members** : ``` 😀 {total_members}     Total members\n 🟢 {members_online}      Online \n 🔴 {members_dnd}      Do not disturb \n 🟠 {members_idle}      Idle \n ⚫ {members_offline}     Offline \n 🤖 {no_of_bots}     Bots```\n**Roles** : `{len(ctx.guild.roles)}`\n**Created** : `{created_at_time}`",inline=False)
            embed.set_thumbnail(url=str(ctx.guild.icon_url)) 
            embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.reply(embed=embed)
    
    @commands.cooldown(1,10, commands.BucketType.user)
    @commands.command(name="Whois",aliases=["userinfo"], help=f'Shows information of a user')
    async def whois(self,ctx,user:discord.Member=None):
        user_mention = user or ctx.author
        embed=discord.Embed(title = f"{user_mention.name}",color =random.choice(colourlist), timestamp=ctx.message.created_at)
        embed.add_field(name="Status:",value=f"`{user_mention.raw_status.capitalize()}`")
        joined_on_time=self.time_format_function(user_mention.joined_at)
        embed.add_field(name="Joined server at:",value=f"`{joined_on_time}`")
        embed.add_field(name="Nickname:",value=f"`{str(user_mention.nick)}`")
        if user_mention.is_on_mobile():
            device = "📱 Mobile"
        else:
            device = "💻 Desktop"
        embed.add_field(name="Device:",value=f"`{device}`")
        made_on_time=self.time_format_function(user_mention.created_at)
        embed.add_field(name="Account made on:",value=f"`{made_on_time}`")
        embed.add_field(name="User ID:",value=f"`{user_mention.id}`")
        #embed.add_field(name="",value=f"{user_mention.}")
        embed.set_thumbnail(url=str(user_mention.avatar_url)) 

        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
        await ctx.reply(embed=embed)
    
    @commands.cooldown(1,5, commands.BucketType.user)
    @commands.command(name="Avatar",aliases=['dp', 'pfp','av'], help=f'Shows the avatar of a user')
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
     
          
    
    # @commands.has_permissions(manage_messages=True)
    # #@commands.cooldown(1, 10, commands.BucketType.user)
    # @commands.group(name="Giveaway", help=f'Creates a giveaway',invoke_without_command=True)
    # async def giveaway(self,ctx):
    #     channel = await self.text_input_function(ctx,title="Which channel do you want your giveaway to be in?",text="Mention the channel in which the giveaway would be created.")
    #     channel=await commands.TextChannelConverter().convert(ctx,channel)
    #     prize = await self.text_input_function(ctx,title="What is the prize for the Giveaway?",text="Enter what is the prize.")
    #     no_of_winners = int(await self.text_input_function(ctx,title="How many winners do you want?",text="Enter a number. Negative numbers and Zero is not allowed."))
    #     if no_of_winners < 0 :
    #         await ctx.reply("You can't have a negative winner, dude.")
    #     elif no_of_winners == 0 :
    #         await ctx.reply("No winner? You need to have atleast 1 winner, dumbo.")
    #     time = await self.text_input_function(ctx,title="How long will the giveaway last?",text="Enter the time")
    #     pos = ["s","m","h","d"]
    #     time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}
    #     unit = time[-1]
    #     if unit not in pos:
    #         await ctx.reply(f"You didn't answer with a proper unit. Use (s|m|h|d) next time!")
    #         return
    #     try:
    #         val = int(time[:-1])
    #     except:
    #         await ctx.reply(f"The time can only be an integer. Please enter an integer next time.")
    #         return

    #     time_secs= val * time_dict[unit]
    #     #print(channel)
    #     #giveaway_msg = await channel.send(f"{prize} is being given away for {time}")
    #     embed=discord.Embed(title=f":gift: |  Giveaway!",description=f"{prize}",color = 0xFF0000)
    #     if no_of_winners == 1:
    #         embed.add_field(name="React with :tada: to enter!",value=f"{no_of_winners} winner")
    #     elif no_of_winners > 1:
    #         embed.add_field(name="React with :tada: to enter!",value=f"{no_of_winners} winners")
    #     embed.set_footer(text=f"Ends in {time} • {self.bot.user.name} ")    
    #     giveaway_msg = await channel.send(embed=embed)
    #     await giveaway_msg.add_reaction("\U0001f389")
    #     await asyncio.sleep(int(time_secs))
    #     # print(giveaway_msg.reactions)
    #     # winner=random.choice(giveaway_msg.reactions)
    #     # await ctx.send(f"{winner.user.mention} won the giveaway")
    #     new_msg = await channel.get_message(giveaway_msg.id)
    #     giveaway_msg = new_msg
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

    # @commands.has_permissions(manage_messages=True)
    # #@commands.cooldown(1, 10, commands.BucketType.user)
    # @giveaway_msg.group(name="reroll", help=f'Reroll a giveaway. \n \"{config.default_prefixes[0]}reroll giveaway_message_id\"')
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
    
    @checks.server_is_approved()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    #@commands.cooldown(1, 10, commands.BucketType.user)
    @commands.group(name="Poll", help=f'Creates a poll.\nArguments need to be in the format: \n`[Question] Option_1, Option_2, Option_3`',require_var_positional=True)#require_var_positional=True makes sure input is not empty
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
        if result is None:
            await ctx.send("You didn't mention a question. Format: `[Question] Option_1, Option_2, Option_3`")
            return
        
        question = result.group(1)
        options = response.replace(f"[{question}]","").split(",")
        
        if len(options) > 10:
            await ctx.send("You inputted too many options. Maximum number of options is 10.")
        
        elif len(options) <= 1:
            await ctx.send("You inputted too less options. Minimum number of options is 2.")
        
        elif len(question.replace(" ","")) <= 0:
            await ctx.send("You didn't mention a question. Format: `[Question] Option_1, Option_2, Option_3`")
            return


        #Proper outcome. There is a question and 1-10 Options
        elif question is not None:
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

            reaction_count_of_user=0
            for reaction in PollMessage.reactions:
                reacted_users = await reaction.users().flatten()
                if user in reacted_users and str(reaction.emoji) in number_emojis:
                    reaction_count_of_user+=1
            

            async def update_poll_bar():
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

            if reaction_count_of_user > 1:
                pass
            else:
                await update_poll_bar()


            # if type_of_event == "reaction_add":          
            #     for reaction in PollMessage.reactions:#checks all reactions of message
            #         if (str(reaction.emoji) in number_emojis) and (str(reaction.emoji) != str(emoji)) and reaction_count > 1 :
            #             print("del",str(reaction.emoji),str(emoji))
            #             await PollMessage.remove_reaction(reaction.emoji, user)

           



            

    def bar_generator(self,count,total):
        if total == 0 :#prevent zero division error
            total = 1
        percent=round(count/total * 100,1)
        bar_count=round(percent/100*20)
        bars_string='█' * bar_count
        bars_string=bars_string + " " * (20-len(bars_string))
        return bars_string,percent

   
   
   



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
        