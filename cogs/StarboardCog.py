from logging import error
import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config
import utils.checks as checks

colourlist=config.embed_colours

#All reaction listeners take place in Reactions.py
    
class Starboard(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    @checks.server_is_approved()
    @commands.guild_only()
    @commands.group(name="Starboard",invoke_without_command=True,aliases=["star","sb"],help=f"Command to access starboard data.\nFormat: `{config.prefix}starboard` \nSubcommands: random\nAliases:star, sb")
    async def star(self,ctx,user:discord.Member=None):
        user= user or ctx.author
        total_stars=0
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                
                all_rows = await connection.fetch("SELECT * FROM starboard")
                for row in all_rows:
                    row=dict(row)
                    reactions=json.loads(row["reactions"])
                    total_stars= total_stars + reactions["star"]
                
                embed=discord.Embed(title=f"Starboard",description=f"Starboard stuff")
                embed.add_field(name="Total stars:",value=f"{total_stars}",inline=True)
                user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                reactions_given=json.loads(user_account["reactions_given"])
                embed.add_field(name="Stars given:",value=f'{reactions_given["star"]}',inline=True)
                reactions_received=json.loads(user_account["reactions_received"])
                embed.add_field(name="Stars received:",value=f'{reactions_received["star"]}',inline=True)

                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
                await ctx.reply(embed=embed)
    
    @star.command(name="random")
    async def star_random(self,ctx,help=f"Command to get a random message from the starboard.\nFormat: `{config.prefix}starboard random`"):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                server_info = await connection.fetchrow("SELECT * FROM server_info WHERE id=$1",ctx.guild.id)
                starboard=json.loads(server_info["starboard"])["starboard_posts"] #load the json content of the starboard column
                if len(starboard) > 0:
                    post = random.choice(starboard)
                    starboard_channel=self.bot.get_channel(config.starboard_channel_id) 
                    StarMessage = await starboard_channel.fetch_message(post["star_message_id"])
                    await ctx.reply(content=StarMessage.content,embed=StarMessage.embeds[0])
                else:
                    raise Exception("The Starboard currently doesn't have enough posts for this command. Try again later.")
                    #await ctx.reply(content="The Starboard currently doesn't have enough posts for this command. Try again later.")

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def star_reaction_add(self,payload):  
        
        
        ImportantFunctions = self.bot.get_cog('ImportantFunctions') 
        channel = self.bot.get_channel(payload.channel_id) 
        user = self.bot.get_user(payload.user_id)
        message = await channel.fetch_message(payload.message_id)
        emoji=payload.emoji 
        
        if channel.guild.id in config.APPROVED_SERVERS:#if that server is approved/that server has the settings
            if user.bot:
                return 
            
            #=============================================
            #Starboard
            #=============================================
            if str(emoji) == "⭐":
                # if message.author == user: #self star
                #     return
                # else:
                # update the reactions sent in database
                await ImportantFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="star",num=1)
                await ImportantFunctions.post_to_starboard(message=message,channel=channel,user=user,emoji=emoji,reaction_name="star")

    @commands.Cog.listener(name="on_raw_reaction_remove")
    async def star_reaction_remove(self,payload):  
        ImportantFunctions = self.bot.get_cog('ImportantFunctions') 
        channel=self.bot.get_channel(payload.channel_id) 
        user=self.bot.get_user(payload.user_id)
        message= await channel.fetch_message(payload.message_id)
        emoji=payload.emoji  
        reaction_count =await ImportantFunctions.get_reaction_count(message=message,emoji=emoji)

        if channel.guild.id in config.APPROVED_SERVERS:#if that server is approved/that server has the settings
            if user.bot:
                return
            
            if str(emoji) == "⭐":
                #update the reactions sent in database
                await ImportantFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="star",num=-1)
                async with self.bot.pool.acquire() as connection:
                    async with connection.transaction():
                        starboard_channel=self.bot.get_channel(config.starboard_channel_id)        
                        server_info = await connection.fetchrow("SELECT * FROM server_info WHERE id=$1",channel.guild.id)
                        starboard=json.loads(server_info["starboard"])#load the json content of the starboard column
                        starboard_post_list=starboard["starboard_posts"] #fetch all the posts in the starboard
                        post=None
                        for x in starboard_post_list:
                            if x["root_message_id"] == message.id:
                                post=x
            
                            
                        #if this message is not in the database/ it has not been starred earlier
                        if post == None:
                            return
                        else:  
                            stars_required_for_starboard  = (await ImportantFunctions.get_settings(channel.guild.id))["starboard_stars_required"]

                            post=dict(post)
                            StarMessage = await starboard_channel.fetch_message(post["star_message_id"])
                            reactions_of_post = post["reactions"]
                            
                            #if no reactions on message, and no awards in database
                            #only for case where no of stars required is set to 1
                            if len(message.reactions) == 0 and len(reactions_of_post) <= 1 :
                                await StarMessage.delete()
                                starboard_post_list.remove(post)
                                #Database Actions
                                post["reactions"]=reactions_of_post
                                starboard_json=json.dumps(starboard)
                                await connection.execute("UPDATE server_info SET starboard = $1 WHERE id=$2",starboard_json,channel.guild.id)
                            
                            #if stars have become lesser than required number, and no awards in database
                            elif reaction_count < stars_required_for_starboard and len(reactions_of_post) <= 1:
                                await StarMessage.delete()
                                starboard_post_list.remove(post)
                                #Database Actions
                                post["reactions"]=reactions_of_post
                                starboard_json=json.dumps(starboard)
                                await connection.execute("UPDATE server_info SET starboard = $1 WHERE id=$2",starboard_json,channel.guild.id)
                            
                            #if stars are enough
                            elif reaction_count >= stars_required_for_starboard:
                                await ImportantFunctions.post_to_starboard(message=message,channel=channel,user=user,emoji=emoji,reaction_name="star")

    #When a message in Starboard gets deleted, delete that message from the Database
    @commands.Cog.listener(name="on_raw_message_delete")
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



def setup(bot):
    bot.add_cog(Starboard(bot))