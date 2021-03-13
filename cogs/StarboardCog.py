import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config   

    
class Starboard(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):  
        ImportantFunctions = self.bot.get_cog('ImportantFunctions') 
        channel=self.bot.get_channel(payload.channel_id) 
        user=self.bot.get_user(payload.user_id)
        message= await channel.fetch_message(payload.message_id)
        emoji=payload.emoji 
        if user.bot:
            return 

        for x in message.reactions:
            if str(x.emoji) == str(emoji):
                reaction = x
        
        

        #starboard
        if str(emoji) == "⭐":
            # if message.author == user:
            #     return
            # else:
            # update the reactions sent in database
            await ImportantFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="star",num=1)
            await ImportantFunctions.post_to_starboard(message=message,channel=channel,user=user,reaction=reaction,type_of_reaction="Star",reaction_name="star")


                
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):  
        ImportantFunctions = self.bot.get_cog('ImportantFunctions') 
        channel=self.bot.get_channel(payload.channel_id) 
        user=self.bot.get_user(payload.user_id)
        message= await channel.fetch_message(payload.message_id)
        emoji=payload.emoji  
        if user.bot:
            return
        
        if str(emoji) == "⭐":
            #update the reactions sent in database
            await ImportantFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="star",num=-1)
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    starboard_channel=self.bot.get_channel(config.starboard_channel_id) 
                    reacted_message = await connection.fetchrow("SELECT * FROM starboard WHERE root_message_id=$1",message.id)                 
                    #if this message is not in the database/ it has not been starred earlier
                    if reacted_message == None:
                        return
                    else:    
                        for x in message.reactions:
                            if str(x.emoji) == str(emoji):
                                reaction = x


                        reacted_message=dict(reacted_message)
                        StarMessage = await starboard_channel.fetch_message(reacted_message["star_message_id"])
                        reactions_of_post = json.loads(reacted_message["reactions"])
                        
                        #if no reactions on message, and no awards in database
                        if len(message.reactions) == 0 and len(reactions_of_post) <= 1 :
                            await StarMessage.delete()
                            await connection.execute("DELETE FROM starboard WHERE root_message_id=$1",message.id)
                        
                        #if stars have become lesser than required number, and no awards in database
                        elif reaction.count < config.stars_required_for_starboard and len(reactions_of_post) <= 1:
                            await StarMessage.delete()
                            await connection.execute("DELETE FROM starboard WHERE root_message_id=$1",message.id)
                        
                        #if stars are enough
                        elif reaction.count >= config.stars_required_for_starboard:
                            await ImportantFunctions.post_to_starboard(message=message,channel=channel,user=user,reaction=reaction,type_of_reaction="Star",reaction_name="star")
                    

    @commands.Cog.listener()
    async def on_raw_message_delete(self,payload): 
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction(): 
                all_rows = await connection.fetch("SELECT * FROM starboard")
                for row in all_rows:
                    row=dict(row)
                    if payload.message_id == row["star_message_id"]:
                        await connection.execute("DELETE FROM starboard WHERE star_message_id=$1",payload.message_id)

    
    @commands.group(name="Star",invoke_without_command=True,aliases=["starboard","sb"])
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
                await ctx.send(embed=embed)
    
    @star.command(name="random")
    async def star_random(self,ctx):
         async with self.bot.pool.acquire() as connection:
        # create a transaction for that connection
            async with connection.transaction():
                starboard_channel=self.bot.get_channel(config.starboard_channel_id) 
                all_rows = await connection.fetch("SELECT * FROM starboard")
                post=random.choice(all_rows)
                post=dict(post)
                StarMessage= await starboard_channel.fetch_message(post["star_message_id"])
                await ctx.send(content=StarMessage.content,embed=StarMessage.embeds[0])


def setup(bot):
    bot.add_cog(Starboard(bot))