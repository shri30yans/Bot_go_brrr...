import discord,json,random
from discord.ext import commands
import utils.awards as awards
import utils.badges as badges
import config   
from datetime import datetime
import asyncio

colourlist=config.embed_colours

class StarboardFunctions(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    async def post_to_starboard(self,message,channel,user,emoji,reaction_name): 
        guild_id = message.guild.id
        starboard_info = await self.get_starboard_info(guild_id)
        starboard_post_list = starboard_info["starboard_posts"]
        starboard_stars_required = starboard_info["stars_required"]
        channel_id=starboard_info["starboard_channel_id"]
        starboard_channel = self.bot.get_channel(channel_id)
        self_star = starboard_info["self_star"]
        lock = starboard_info["lock"]
        private_channel = starboard_info["private_channel"]
        nsfw = starboard_info["nsfw"]
        sb_emoji = await self.get_server_starboard_emoji(guild_id)
        
        #if the lock value for the starboard is true
        if lock:
            return
        elif  channel_id is None:
            return
        
        elif (starboard_channel is None) and (channel_id is not None):
            #if the starboard channel is None, but a channel is stored in the database (Starboard channel is deleted), reset the stored information
            starboard_info["starboard_channel_id"] = None
            starboard_info["starboard_posts"]=[]
            await self.update_starboard(starboard_info,guild_id)
            return

        elif (channel.is_nsfw()) and (nsfw is False): 
            #NSFW channel is set to false and the channel is a NSFW channel
            return
        elif (channel.overwrites_for(channel.guild.default_role).view_channel is False) and (private_channel is False): 
            #Private channel settings is set to false and the channel is a private channel
            return
        elif message.author.bot:
            return
        else:
            async def get_star_reaction_count(message,emoji):
                if len(message.reactions) == 0:
                    #If the message doesn't have any reactions
                    reaction_count=0
                    return reaction_count
                    
                else:
                    for x in message.reactions:
                        if str(x.emoji) == str(emoji):
                            reaction = x
                            users_who_have_reacted = await reaction.users().flatten()
                            if (not(self_star) and (message.author in users_who_have_reacted)):
                                reaction_count = reaction.count -1
                            else:
                                reaction_count = reaction.count
                            return reaction_count
                    
                    else:
                        #This returns if the message has reactions but there are no reactions that we wanted to get the count of
                        reaction_count = 0
                        return reaction_count

            reaction_count = await get_star_reaction_count(message=message,emoji=emoji)
                    
            post=None
            for x in starboard_post_list:
                if x["root_message_id"] == message.id:
                    post=x
                    break
            
            
            if post is None: 
                #if message is not previously in starboard/ message is not in database ie new message 
                if str(emoji) in sb_emoji:
                    if reaction_count < starboard_stars_required:
                        #if reaction is star but reaction count is less than the set limit it will be returned
                        return

                    await self.create_new_starboard_post(sb_emoji=sb_emoji,message=message,channel=channel,starboard_channel=starboard_channel,starboard_post_list=starboard_post_list,starboard_info=starboard_info,guild_id=guild_id,reaction_count=reaction_count)
                
            else: 

                #message exists in starboard/is present in the database
                try:
                    StarMessage = await starboard_channel.fetch_message(post["star_message_id"])
                except:
                    #In case the starboard message was deleted, this deletes it from the database
                    starboard_post_list.remove(post)
                    await self.update_starboard_key(starboard_info=starboard_info,starboard_info_key="starboard_posts",value=starboard_post_list,guild_id=guild_id)
                    return
                    
                reactions_of_post = post["reactions"]
                if str(emoji) in sb_emoji:
                #if stars have become lesser than required number, and there are no awards in database
                    if (reaction_count < starboard_stars_required and len(reactions_of_post) <= 1 ):
                        await StarMessage.delete()
                        starboard_post_list.remove(post)
                        await self.update_starboard_key(starboard_info=starboard_info,starboard_info_key="starboard_posts",value=starboard_post_list,guild_id=guild_id)
                    
                    #if stars are enough to stay on the starboard, update it
                    elif reaction_count >= starboard_stars_required:
                        await self.update_starboard_post(sb_emoji=sb_emoji,post=post,reaction_name=reaction_name,channel=channel,starboard_channel=starboard_channel,starboard_post_list=starboard_post_list,starboard_info=starboard_info,guild_id=guild_id,reaction_count=reaction_count)



    async def create_new_starboard_post(self,sb_emoji,message,channel,starboard_channel,starboard_post_list,starboard_info,guild_id,reaction_count):
        reactions_of_post={}    
        reactions_of_post["star"] = reaction_count

    
        #Embed
        reaction_id_string = await self.formatted_starboard_awards_string(reactions_of_post=reactions_of_post,sb_emoji=sb_emoji)
        reaction_id_string = reaction_id_string + channel.mention

        if (channel.is_nsfw()) is False:
            embed=discord.Embed(color =random.choice(colourlist),timestamp=message.created_at,description=message.content)
        
        elif (channel.is_nsfw()) and (starboard_channel.is_nsfw()):
            embed=discord.Embed(color = random.choice(colourlist),timestamp=message.created_at,description=message.content)

        else:
            embed=discord.Embed(color = random.choice(colourlist),timestamp=message.created_at,description="`This post is in a NSFW channel.\nUse the Jump link to view that post here or make the Starboard channel a NSFW channel for future posts.`" )
        
        embed.set_author(name=message.author.name, icon_url= f"{message.author.avatar_url}")
        embed.add_field(name="Source:", value=f"[Jump]({message.jump_url} \"See the starred post.\")", inline=False)
        
        if len(message.attachments) and (channel.is_nsfw() is False): #basically if len !=0 or if attachments are there
            embed.set_image(url=message.attachments[0].url)
        

        embed.set_footer(text=f"{message.id}")
        
        StarMessage = await starboard_channel.send(content=f"{reaction_id_string}",embed=embed)

        #Database Actions
        starboard_post_info={"root_message_id":message.id ,"star_message_id":StarMessage.id ,"reactions":reactions_of_post}
        starboard_post_list.append(starboard_post_info)
        await self.update_starboard_key(starboard_info=starboard_info,starboard_info_key="starboard_posts",value=starboard_post_list,guild_id=guild_id)

    
    async def update_starboard_post(self,post,sb_emoji,reaction_name,channel,starboard_channel,starboard_post_list,starboard_info,guild_id,reaction_count):
        StarMessage = await starboard_channel.fetch_message(post["star_message_id"])      
        reactions_of_post=post["reactions"]
        reactions_of_post[reaction_name.lower()] = reaction_count
        
        #Embed
        reaction_id_string = await self.formatted_starboard_awards_string(reactions_of_post=reactions_of_post,sb_emoji=sb_emoji)
        reaction_id_string = reaction_id_string + channel.mention
        await StarMessage.edit(content=f"{reaction_id_string}")
        
        #Database Actions
        starboard_post_list.remove(post)
        post["reactions"]=reactions_of_post
        starboard_post_list.append(post)
        await self.update_starboard_key(starboard_info=starboard_info,starboard_info_key="starboard_posts",value=starboard_post_list,guild_id=guild_id)
              

                
    async def formatted_starboard_awards_string(self,reactions_of_post,sb_emoji):
        #used to arrange the award and stars in order so that the order in starboard is [ternion,argentinum,platinum,gold....star]
        ordered_reactions_of_post={}
        for x in list(awards.awards_list.values())[::-1]:
            try:
                ordered_reactions_of_post[x.name]=reactions_of_post[x.name]
            except:
                pass
        try:
            #if post has stars
            ordered_reactions_of_post["star"]=reactions_of_post["star"]
        except:
            pass        

        reaction_id_string=""
        for r in ordered_reactions_of_post:
            if r == "star":
                reaction_id = sb_emoji[0]
            
            reaction_id_string = reaction_id_string + f"{ordered_reactions_of_post[r]} {reaction_id}   "

        return reaction_id_string
                
     
    async def get_starboard_info(self,guild_id):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        await ImportantFunctions.get_server_settings(guild_id)
        try:
            starboard_info=json.loads(self.bot.Info_Table[guild_id]["starboard"])
            return starboard_info
        except:
            return

    async def update_starboard(self,starboard_info,guild_id):
        starboard_info_j=json.dumps(starboard_info)
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        await ImportantFunctions.update_server_settings_key_cache(guild_id,key="starboard",value=starboard_info_j)
        
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("UPDATE server_info SET starboard = $1 WHERE id=$2",starboard_info_j,guild_id)

    async def get_server_starboard_emoji(self,guild_id):
        try:
            starboard_info = await self.get_starboard_info(guild_id)
            return starboard_info["emoji"]
        except:
            return

    async def update_starboard_key(self,starboard_info,starboard_info_key,value,guild_id):
        starboard_info[starboard_info_key] = value
        await self.update_starboard(starboard_info,guild_id)

    
   

        




    

def setup(bot):
    bot.add_cog(StarboardFunctions(bot))