import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap,re
from discord.ext import commands,tasks
import config

colourlist=config.embed_colours
    
class Fun(commands.Cog,name="Productivity or some shit"):
    def __init__(self, bot):
        self.bot = bot    
    
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Concentrate",aliases=["concentratationmode","studytime","failinginexams","sendhelp"], help=f'Removes access to all channels for a specified time period. \nFormat: `{config.prefix}Concentratation mode 5m`\n Time can be entered in (s|m|h|d), Default time is 10 mins.\nAliases:`"ConcentratationMode"`, `"StudyTime"`, `"FailinginExams"`,`"sendhelp"`')
    async def concentrate(self,ctx,members: commands.Greedy[discord.Member],time:str="5m"):
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
            
            role = discord.utils.get(ctx.guild.roles, id=816290318785576991)
            if role == None:
                role = discord.utils.get(ctx.guild.roles, name="Concentration Mode")
                if role == None:
                    await ctx.send("The Concentration role was not found.")
                    return
                
            try: 
                await ctx.author.add_roles(role)
            except : 
                await ctx.send("Concentration Mode failed. Check my perms.")   
            #else:pass
            embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.add_field(name=f":mute: | Concentration Mode activated for {ctx.message.author}",value=f"**{ctx.message.author}** was put on concentration mode for **{time}**!")
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} •{self.bot.user.name} ")    
            await ctx.send(embed=embed)
            

            await asyncio.sleep(int(time_secs))
            try:
                await ctx.author.remove_roles(role)
            except: 
                await ctx.send("Failed to remove concentration mode!")

    #Listeners
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return

        elif message.channel.id==config.suggestions_channel_id:
            if message.content.startswith("//"):
                return
            else:
                await message.add_reaction(config.upvote_reaction)
                await message.add_reaction(config.downvote_reaction)

        elif message.channel.id==config.meme_channel_id and len(message.attachments) !=0:
            await message.add_reaction(config.upvote_reaction)
            await message.add_reaction(config.downvote_reaction)

    #When a message in Starboard gets deleted, delete that message from the Database
    @commands.Cog.listener()
    async def on_raw_message_delete(self,payload): 
        channel=self.bot.get_channel(payload.channel_id)
        if channel.guild.id in config.APPROVED_SERVERS:#if that server is approved/that server has the settings
            if channel.id == config.starboard_channel_id:#if the message was deleted in the starboard channel
                async with self.bot.pool.acquire() as connection:
                    async with connection.transaction(): 
                        server_info = await connection.fetchrow("SELECT * FROM server_info WHERE id=$1",channel.guild.id)
                        starboard=json.loads(server_info["starboard"]) #load the json content of the starboard column
                        starboard_post_list=starboard["starboard_posts"] #fetch all the posts in the starboard
                        post=None
                        for x in starboard_post_list:
                            if payload.message_id == x["star_message_id"]:
                                starboard_post_list.remove(x)
                            starboard_json=json.dumps(starboard)
                            await connection.execute("UPDATE server_info SET starboard = $1 WHERE id=$2",starboard_json,channel.guild.id)

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Remind",aliases=['reminder', 'remindme'], help=f'Sets up a reminder that will remind you after a given a time.\nFormat: `{config.prefix}remind time reason`\nAliases: DP, Avatar')
    async def remind(self, ctx, time, *, message=None):
        if message == None:
            message = ". . ." #set the message if message is None
        else:
            role_check = re.search("<@&.*>$",message)#regex
            if "@everyone" in message :
                message=message.replace("@everyone","everyone")
            elif "@here" in message:
                message=message.replace("@here","here")
            elif role_check:
                await ctx.send("Your message has a role mention. Please try the command again without the mention.")
                #role_id=message.replace("<@&","").replace(">","")
            else:
                message=message
        async def convert(time): #let's start convert the time provided
            pos = ['s', 'm', 'h', 'd'] #valid units
            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24} #attribute for each unit

            unit = time[-1] #get only the unit, not the number (s, m, h, d)

            if unit not in pos: #if unit not in pos list
                await ctx.reply(f"You didn't answer with a proper unit. Use (s|m|h|d) next time!")
                return
            try:
                val = int(time[:-1]) #try get the number before the unit (1s, 1=Number, s=Unit)
            except:
                await ctx.reply(f"The time can only be an integer. Please enter an integer next time.")
                return
            
            return val * time_dict[unit] #get the value of the time * the provided unit
        
        converted_time = await convert(time) #idk
        if converted_time:#making sure it is not None
            time_format = "" #let's start make the str more sweet
            ttt = time[-1]
            if ttt == "s":
                time_format = "second(s)"
            elif ttt == "m":
                time_format = "minute(s)"
            elif ttt == "h":
                time_format = "hour(s)"
            elif ttt == "d":
                time_format = "day(s)"

            final_time = f"{time[:-1]} " + time_format #make the str adding the number (1) + our time_format based on the Unit (s)

            await ctx.reply(f"Alright {ctx.author.mention}, in {final_time}: {message}") #send this if all is good
            await asyncio.sleep(converted_time) #wait for time provided (number)
            await ctx.send(f"{ctx.author.mention}, **{final_time}** ago: {message}\n{ctx.message.jump_url}") #send this when asyncio.sleep() has done







def setup(bot):
    bot.add_cog(Fun(bot))