from core.StarboardFunctions import StarboardFunctions
from logging import error
import json
from utils.ErrorHandler import InvalidSubcommand
from discord.ext import commands
import config,discord
import core.checks as checks
import random,asyncio

colourlist=config.embed_colours

#All reaction listeners take place in Reactions.py
    
class Starboard(commands.Cog,name="Starboard",description="Starboard functions"): 
    def __init__(self, bot):
        self.bot = bot


    @commands.guild_only()
    @commands.group(name="Starboard",invoke_without_command=True,case_insensitive=True,aliases=["star","sb"],help=f"Change starboard settings.")
    async def starboard(self,ctx):
        raise InvalidSubcommand()

    @checks.CheckIfSetupNotCommandUsedBefore()
    @starboard.command(name="Setup",help=f"Setup a starboard for that server.")
    async def starboard_setup(self,ctx):
        StarboardFunctions = self.bot.get_cog('StarboardFunctions')
        starboard_info = await StarboardFunctions.get_starboard_info(ctx.guild.id)
        starboard_channel = self.bot.get_channel(starboard_info["starboard_channel_id"])
        async def exit_command(message,user,reason):
            embed = discord.Embed(title="Setup command exited",description=f"{reason}",color = random.choice(colourlist),timestamp=ctx.message.created_at,colour=random.choice(colourlist))
            embed.set_footer(icon_url= user.avatar_url,text=f"Requested by {user.name} • {self.bot.user.name}")
            await message.edit(embed = embed)
        
        async def timeout_error(message,user):
            embed = discord.Embed(title="Time limit exceeded",description=f"{user.name} took too much time to reply to this message. This action is cancelled.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.set_footer(icon_url= user.avatar_url,text=f"Requested by {user.name} • {self.bot.user.name}")
            await message.edit(embed = embed)

        async def channel_setup():
            embed = discord.Embed(title=f"Starboard setup",description="This command will take you through the steps to configure your starboard.",colour=random.choice(colourlist))
            embed.add_field(name="How would you like to set a Starboard channel",value="`➕`  Create a new starboard channel\n`✏️`  Modify an existing channel\n You can select `❌` to cancel.")
            message = await ctx.reply(embed = embed)
            await message.add_reaction("➕")
            await message.add_reaction("✏️")
            await message.add_reaction("❌")


            def check(reaction,user):
                return (str(reaction.emoji) in ["➕","✏️","❌"]) and (user == ctx.author)

            try:
                reaction,user = await self.bot.wait_for('reaction_add',check=check, timeout=60)

            except asyncio.TimeoutError:
                await timeout_error(message = message,user = ctx.author)

            else:
                if str(reaction) in ['➕']:
                    await message.clear_reactions()
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False),
                        ctx.guild.me: discord.PermissionOverwrite(send_messages=True)
                    }
                    channel = await ctx.guild.create_text_channel(name="starboard",overwrites = overwrites)
                    embed = discord.Embed(title="New Starboard channel created",description=f"A new starboard channel {channel.mention} has been created.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
                    embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
                    await message.edit(embed = embed)
                    return channel


                elif str(reaction) in ['✏️']:
                    await message.clear_reactions()
                    embed = discord.Embed(title="Enter the text channel",description=f"Mention the channel or type it's ID.\nCancel setup command by typing `cancel`.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
                    embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
                    await message.edit(embed = embed)

                    #Retries are the number of chances to input a text channel correctly
                    async def ask_channel_name(ctx,message,retries):
                        try:
                            channelmessage = await self.bot.wait_for('message', check=lambda m:(m.author == ctx.author), timeout=120)

                        except asyncio.TimeoutError:
                            await timeout_error(message = message,user = ctx.author)



                        else:
                            if channelmessage.content.lower() in ["cancel","exit"]:
                                await exit_command(message=message,user=ctx.author,reason=f"{ctx.author.name} exited the command.")
                                return
                            try:
                                channel= await commands.TextChannelConverter().convert(ctx,channelmessage.content)
                                return channel
                            except:
                                if retries > 0:
                                    embed = discord.Embed(title="Invalid channel entered",description=f"You entered a Invalid Text channel.\nMention the channel or type it's ID.\nCancel setup command by typing `cancel`.\nRetries left: `{retries}`",color = random.choice(colourlist),timestamp=ctx.message.created_at)
                                    embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
                                    await message.edit(embed = embed)
                                    retries -= 1
                                    return (await ask_channel_name(ctx,message,retries))
                                else:
                                    await exit_command(message=message,user=ctx.author,reason=f"{ctx.author.mention} reached the maximum number of retries.")
                                    return

                    
                    return (await ask_channel_name(ctx,message=message,retries=3))
                    

                    
                elif str(reaction) in ['❌']:
                    await message.clear_reactions()
                    await exit_command(message=message,user=ctx.author,reason=f"{ctx.author.name} exited the command.")
                    return

        async def star_limit_setup():
            embed = discord.Embed(title="Enter Star limit",description=f"Enter the number of stars required for a post to be sent to starboard.\nCancel setup command by typing `cancel`.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
            message = await ctx.send(embed = embed)

            #Retries are the number of chances to input a text channel correctly
            async def ask_star_limit(ctx,retries):
                try:
                    starlimitmessage = await self.bot.wait_for('message', check=lambda m:(m.author == ctx.author), timeout=120)

                except asyncio.TimeoutError:
                    await timeout_error(message = message,user = ctx.author)


                else:
                    if starlimitmessage.content.lower() in ["cancel","exit"]:
                        await exit_command(message=message,user=ctx.author,reason=f"{ctx.author.name} exited the command.")
                        return
                    try:
                        star_limit = int(starlimitmessage.content)
                        if star_limit <= 0:
                            raise Exception
                        return star_limit
                    except:
                        if retries > 0:
                            embed = discord.Embed(title="Invalid star limit entered",description=f"You entered an invalid star limit\nThe star limit needs to be a positive integer.\nCancel setup command by typing `cancel`.\nRetries left: `{retries}`",color = random.choice(colourlist),timestamp=ctx.message.created_at)
                            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
                            await message.edit(embed = embed)
                            retries -= 1
                            return (await ask_star_limit(ctx,retries))
                        else:
                            await exit_command(message=message,user=ctx.author,reason=f"{ctx.author.mention} reached the maximum number of retries.")
                            return

            
            return (await ask_star_limit(ctx,retries=3)) 
                
    
        if starboard_channel is None:
            channel = await channel_setup()
            if channel:
                pass
            else:
                return
            
            star_limit = await star_limit_setup()
            if star_limit:
                pass
            else:
                return

            #Reaches this point if channel and star_limit has been set
            embed = discord.Embed(title="Setup command executed.",description=f"Starboard Channel: {channel.mention}\nStars required: {star_limit}",color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.set_thumbnail(url=str(ctx.guild.icon_url))
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
            await ctx.reply(embed = embed)
            guild_id = ctx.guild.id
            starboard_info = await StarboardFunctions.get_starboard_info(guild_id)
            starboard_info["starboard_channel_id"] = channel.id
            starboard_info["stars_required"]=star_limit
            await StarboardFunctions.update_starboard(starboard_info,guild_id)

                



        

           
        
    @checks.CheckIfStarboardExists()
    @starboard.command(name="Random",help=f"Command to get a random message from the starboard.")
    async def star_random(self,ctx):
        StarboardFunctions = self.bot.get_cog('StarboardFunctions')
        starboard_info = await StarboardFunctions.get_starboard_info(ctx.guild.id)
        starboard_posts_list =  starboard_info["starboard_posts"]
        starboard_channel = self.bot.get_channel(starboard_info["starboard_channel_id"])

         #load the json content of the starboard column
        if len(starboard_posts_list) > 0:
            post = random.choice(starboard_posts_list)
            StarMessage = await starboard_channel.fetch_message(post["star_message_id"])
            await ctx.reply(content=StarMessage.content,embed=StarMessage.embeds[0])
        else:
            await ctx.reply("The Starboard currently doesn't have enough posts for this command. Try again later.")
    
    # @starboard.command(name="Stats")
    # async def starboard_stats(self,ctx,user):
    #     user= user or ctx.author
    #     total_stars=0
    #     #ImportantFunctions = self.bot.get_cog('ImportantFunctions')
    #     UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
    #     # starboard_posts_list = (await ImportantFunctions.get_starboard_info(ctx.guild.id))["starboard_posts"]
    #     reactions_given, reactions_received =await UserDatabaseFunctions.get_user_reactions(user)
    #     embed=discord.Embed(title=f"Starboard",)
    #     embed.add_field(name="Total stars:",value=f"{total_stars}",inline=True)

    #     embed.add_field(name="Stars given:",value=f'{reactions_given["star"]}',inline=True)
    #     embed.add_field(name="Stars received:",value=f'{reactions_received["star"]}',inline=True)
    #     embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
    #     await ctx.reply(embed = embed)
    
    @checks.CheckIfStarboardExists()
    @starboard.command(name="Channel",help=f"Command to change the starboard channel.")
    async def starboard_change_channel(self,ctx,channel:discord.TextChannel=None):
        user=ctx.author
        guild_id=ctx.guild.id 
        StarboardFunctions = self.bot.get_cog('StarboardFunctions')
        starboard_info = await StarboardFunctions.get_starboard_info(ctx.guild.id)
        starboard_channel = self.bot.get_channel(starboard_info["starboard_channel_id"])
        if channel is None:
            embed = discord.Embed(title=f"Starboard channel",color = 0xFFD700)
            embed.add_field(name=f"The Starboard channel is currently {starboard_channel.mention}.",value=f"This can be changed by mentioning a channel to change it to.")
            embed.set_footer(icon_url= user.avatar_url,text=f"Requested by {user.name} • {self.bot.user.name} ")
            await ctx.reply(embed=embed)
            return

        elif channel == starboard_channel:
            embed = discord.Embed(title=f"Change Starboard channel",color = 0xFFD700)
            embed.add_field(name="You have already set it to this channel.",value=f"The Starboard channel is currently {channel.mention}.")
            embed.set_footer(icon_url= user.avatar_url,text=f"Requested by {user.name} • {self.bot.user.name} ")
            await ctx.reply(embed=embed)
            return
        else:
            embed = discord.Embed(title=f"Change Starboard channel?",description="React with `✅` to give the confirm and `❌` to cancel.",color = 0xFFD700)
            embed.add_field(name="Note:",value=f"Changing the starboard channel will **delete** all the previous posts information in the previous channel.\nAny future stars on those post's will not be updated.\nAre you sure you want to change the Starboard channel from {starboard_channel.mention} to {channel.mention}?")
        
            embed.set_thumbnail(url=str(ctx.guild.icon_url)) 
            embed.set_footer(icon_url= user.avatar_url,text=f"Requested by {user.name} • {self.bot.user.name} ")
            message = await ctx.reply(embed=embed)
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            
            def check_accept_or_reject(confirm_reaction,confirm_user):
                return str(confirm_reaction.emoji) in ['✅', '❌'] and user == confirm_user

            try:
                confirm_reaction,confirm_user = await self.bot.wait_for('reaction_add',check=check_accept_or_reject, timeout=60)#pylint: disable=unused-argument 
                #disables the confirm_user unusesd argument error

            except asyncio.TimeoutError:
                #await message.delete()
                await message.edit(embed=discord.Embed(title="Timeout!",description=f"{user.mention}, did not react after 60 seconds.This action is cancelled.",color = 0xFFD700))

            else:
                if str(confirm_reaction.emoji) == '✅':
                    await message.clear_reactions()
                    embed = discord.Embed(title=f"Set Starboard Channel",color = 0xFFD700)
                    embed.add_field(name="The Starboard channel has succesfully been set.",value=f"Current starboard channel: {channel.mention}")
                    embed.set_thumbnail(url=str(ctx.guild.icon_url)) 
                    embed.set_footer(icon_url= user.avatar_url,text=f"Requested by {user.name} • {self.bot.user.name} ")
                    message=await message.edit(embed=embed)
                    #print(channel.name,channel.id)
                    starboard_info["starboard_channel_id"] = channel.id
                    starboard_info["starboard_posts"]=[]
                    await StarboardFunctions.update_starboard(starboard_info,guild_id)

                elif str(confirm_reaction.emoji) == '❌':
                    await message.clear_reactions()
                    embed = discord.Embed(title=f"Set Starboard Channel",color = 0xFFD700)
                    embed.add_field(name="This action has been cancelled",value=f"No changes were made to the Starboard")
                    embed.set_thumbnail(url=str(ctx.guild.icon_url)) 
                    embed.set_footer(icon_url= user.avatar_url,text=f"Requested by {user.name} • {self.bot.user.name} ")
                    message=await message.edit(embed=embed)
    
    @checks.CheckIfStarboardExists()
    @starboard.command(name="Limit",aliases = ["required","number"],help=f"Command to change the amount of stars that sends a post in the starboard.")
    async def starboard_change_limit(self,ctx,stars_limit:int=None):
        user=ctx.author
        guild_id=ctx.guild.id
        StarboardFunctions = self.bot.get_cog('StarboardFunctions')
        starboard_info = await StarboardFunctions.get_starboard_info(ctx.guild.id)
        stars_required = starboard_info["stars_required"]
        
        if stars_limit is None:
            title="Starboard star limit"
            name=f"Current stars required: {stars_required}"
            value=f"{stars_required} are required to post a message to starboard. Use `starboard limit <new_limit>` to change this."
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)

        elif (stars_limit > 100) or (stars_limit <=0 ):
            title="Invalid Star limit"
            name=f"The Star limit entered is Invalid."
            value=f"Star's required to post to starboard must be between 1 and 100."
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)

        
        elif stars_limit == stars_required:
            title="Starboard star limit"
            name=f"The star limit is already set to {stars_limit}"
            value=f"The Starboard star limit is currently {stars_limit}."
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)
        
        else:  
            title="Starboard star limit"
            name=f"The star limit is now changed."
            value=f"The Starboard star limit is currently {stars_limit}."
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)
        
            starboard_info["stars_required"]=stars_limit
            StarboardFunctions = self.bot.get_cog('StarboardFunctions')
            await StarboardFunctions.update_starboard_key(starboard_info=starboard_info,starboard_info_key="stars_required",value=stars_limit,guild_id=guild_id)

    @checks.CheckIfStarboardExists()
    @starboard.command(name="Self",aliases=["selfstar"],help=f"Command to toggle the abilty to star your own posts.")
    async def starboard_change_self(self,ctx,value:bool=None):
        user=ctx.author
        guild_id=ctx.guild.id
        
        StarboardFunctions = self.bot.get_cog('StarboardFunctions')
        starboard_info = await StarboardFunctions.get_starboard_info(ctx.guild.id)
        self_star = starboard_info["self_star"]
        print(self_star)
        
        if value is None:
            if self_star:
                value=f"User's can star their own message.\nUse `starboard self False` to change this."
            else:
                value=f"User's cannot star their own message.\nUse `starboard self True` to change this."
            title="Starboard Self Star"
            name=f"Current Self star setting:{self_star}"
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)
        
        elif self_star is value:
            if self_star:
                value=f"User's can already star their own messages.\nUse `starboard self False` to change this."
            else:
                value=f"User's cannot star their own messages.\nUse `starboard self True` to change this."
            title="Starboard Self Star"
            name=f"Starboard Self star is already set to {self_star}"
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)
        
        else:
            self_star = value
            title="Starboard Self star"
            name=f"Self star: {self_star}"
            if self_star == False:
                value=f"User's can no longer star their own message."
            
            elif self_star == True:
                value=f"User's can now star their own message."
            
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)
                

            await StarboardFunctions.update_starboard_key(starboard_info=starboard_info,starboard_info_key="self_star",value=self_star,guild_id=guild_id)

    @checks.CheckIfStarboardExists()
    @starboard.command(name="Lock",aliases=["enable","disable"],help=f"Command to toggle locking the Starboard. If Starboard channel is locked no other messages can be sent to it.")
    async def starboard_change_lock(self,ctx,value:bool=None):
        user=ctx.author
        guild_id=ctx.guild.id
        
        StarboardFunctions = self.bot.get_cog('StarboardFunctions')
        starboard_info = await StarboardFunctions.get_starboard_info(ctx.guild.id)
        lock = starboard_info["lock"]
        if value is None:
            if lock:
                value=f"Starboard is currently locked. No messages can be sent to the starboard.\nUse `starboard Lock False` to change this."
            else:
                value=f"Starboard is unlocked.\nUse `starboard Lock True` to change this."

            title="Starboard Lock"
            name=f"Current Lock setting:{lock}"
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)
        
        elif lock is value:
            if lock:
                value=f"Starboard is currently locked. No messages can be sent to the starboard.\nUse `starboard Lock False` to change this."
            else:
                value=f"Starboard is unlocked.\nUse `starboard Lock True` to change this."

            title="Starboard Lock"
            name=f"Starboard Lock is already set to {lock}"
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)
        
        else:
            lock = value
            title="Starboard Lock"
            name=f"Lock: {lock}"
            if lock == False:
                value=f"Starboard has been unlocked and is working again."              
            
            elif lock == True:
                value=f"Starboard has been locked. No other messages can be sent to the starboard."
            
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)

            await StarboardFunctions.update_starboard_key(starboard_info=starboard_info,starboard_info_key="lock",value=lock,guild_id=guild_id)

    @checks.CheckIfStarboardExists()
    @starboard.command(name="NSFW Channel settings",aliases=["nsfwchannelpost","postnsfw","nsfw","nsfwchannel"],help=f"Command to send posts from a NSFW channel to the starboard. By default any posts starred in a NSFW channel are not posted in the Starboard")
    async def starboard_change_nsfw_channel_settings(self,ctx,value:bool=None):
        user=ctx.author
        guild_id=ctx.guild.id
        
        StarboardFunctions = self.bot.get_cog('StarboardFunctions')
        starboard_info = await StarboardFunctions.get_starboard_info(ctx.guild.id)
        nsfw = starboard_info["nsfw"]
        if value is None:
            if nsfw:
                value=f"Posts in NSFW channels are sent to the Starboard.\nUse `starboard NSFW False` to change this."
            else:
                value=f"Posts in NSFW channels cannot be sent to the Starboard.\nUse `starboard NSFW True` to change this."

            title="Starboard NSFW channel settings"
            name=f"Current NSFW channel settings: {nsfw}"
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)

        elif nsfw is value:
            if nsfw:
                value=f"Posts in NSFW channels are sent to the Starboard.\nUse `starboard NSFW False` to change this."
            else:
                value=f"Posts in NSFW channels cannot be sent to the Starboard.\nUse `starboard NSFW True` to change this."

            title="Starboard NSFW channel settings"
            name=f"Starboard NSFW channel settings is already set to: {nsfw}"
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)
        else:
            nsfw = value
            title="Starboard NSFW channel settings"
            name=f"Post from NSFW channels: {nsfw}"
            if nsfw == False:
                value=f"Posts in NSFW channels can now also be sent to the Starboard."
                
            
            elif nsfw == True:
                value=f"Posts in NSFW channels cannot be sent to the Starboard."
            
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)

        await StarboardFunctions.update_starboard_key(starboard_info=starboard_info,starboard_info_key="nsfw",value=nsfw,guild_id=guild_id)

    @checks.CheckIfStarboardExists()
    @starboard.command(name="Private Channel settings",aliases=["privatechannelpost","postprivate","private","privatechannel"],help=f"Command to send posts from a private channel to the starboard. By default any posts starred in a private channel are not posted in the Starboard")
    async def starboard_change_private_channel_settings(self,ctx,value:bool=None):
        user=ctx.author
        guild_id=ctx.guild.id
        
        StarboardFunctions = self.bot.get_cog('StarboardFunctions')
        starboard_info = await StarboardFunctions.get_starboard_info(ctx.guild.id)
        private_channel = starboard_info["private_channel"]
        
        if value is None:
            if private_channel:
                value=f"Posts in private channels can be sent to the Starboard.\nUse `starboard Private Channel settings False` to change this."
            else:
                value=f"Posts in private channels cannot be sent to the Starboard.\nUse `starboard Private Channel settings True` to change this."             
            
            title=f"Starboard Private channel settings"
            name=f"Current Starboard Private channel settings: {private_channel}"
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)
        
        elif private_channel is value:
            if private_channel:
                value=f"Posts in private channels can be sent to the Starboard.\nUse `starboard Private Channel settings False` to change this."
            else:
                value=f"Posts in private channels cannot be sent to the Starboard.\nUse `starboard Private Channel settings True` to change this."
                
            title=f"Starboard Private channel settings"
            name=f"Starboard Private channel settings is already set to: {private_channel}"
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)
        
        else:
            private_channel = value
            title="Starboard Private channel settings"
            name=f"Starboard Private channel settings: {private_channel}"
            if private_channel == False:
                value=f"Posts in private channels cannot be sent to the Starboard."                
            
            elif private_channel == True:
                value=f"Posts in private channels can now also be sent to the Starboard."
            await self.send_embed_message_for_starboard_settings(ctx,user=user,title=title,name=name,value=value)

            await StarboardFunctions.update_starboard_key(starboard_info=starboard_info,starboard_info_key="private_channel",value=private_channel,guild_id=guild_id)
        

    async def send_embed_message_for_starboard_settings(self,ctx,user,title,name,value):
        embed = discord.Embed(title=title,color = 0xFFD700)
        embed.add_field(name=name,value=value)
        embed.set_thumbnail(url=str(ctx.guild.icon_url)) 
        embed.set_footer(icon_url= user.avatar_url,text=f"Requested by {user.name} • {self.bot.user.name} ")
        await ctx.reply(embed=embed)

               
   
    @commands.Cog.listener(name="on_raw_reaction_add")
    async def star_reaction_add(self,payload):    
        StarboardFunctions = self.bot.get_cog('StarboardFunctions') 
        emoji=payload.emoji 
        user = self.bot.get_user(payload.user_id)
        guild_id=payload.guild_id
        sb_emoji=await StarboardFunctions.get_server_starboard_emoji(guild_id)
        
        if user.bot:
            #if a bot has sent the reaction
            return 
        
        #=============================================
        #Starboard
        #=============================================
        elif str(emoji) in sb_emoji:
            
            #UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
            channel = self.bot.get_channel(payload.channel_id) 
            user = self.bot.get_user(payload.user_id)
            message = await channel.fetch_message(payload.message_id)
            await StarboardFunctions.post_to_starboard(message=message,channel=channel,user=user,emoji=emoji,reaction_name="star")

    @commands.Cog.listener(name="on_raw_reaction_remove")
    async def star_reaction_remove(self,payload):  
        StarboardFunctions = self.bot.get_cog('StarboardFunctions') 
        emoji=payload.emoji 
        user = self.bot.get_user(payload.user_id)
        guild_id=payload.guild_id
        sb_emoji=await StarboardFunctions.get_server_starboard_emoji(guild_id)
        
        if user.bot:
            #if a bot has sent the reaction
            return 
        
        #=============================================
        #Starboard
        #=============================================
        elif str(emoji) in sb_emoji:
            
            #UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
            channel = self.bot.get_channel(payload.channel_id) 
            user = self.bot.get_user(payload.user_id)
            message = await channel.fetch_message(payload.message_id)
            await StarboardFunctions.post_to_starboard(message=message,channel=channel,user=user,emoji=emoji,reaction_name="star")





def setup(bot):
    bot.add_cog(Starboard(bot))