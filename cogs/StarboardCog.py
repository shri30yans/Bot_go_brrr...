import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config   
    
class Starboard(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):  
        DatabaseFunctions = self.bot.get_cog('DatabaseFunctions') 
        channel=self.bot.get_channel(payload.channel_id) 
        user=self.bot.get_user(payload.user_id)
        message= await channel.fetch_message(payload.message_id)
        emoji=payload.emoji  
        all_reacts=message.reactions

        
        #starboard
        for reaction in all_reacts:
            if str(emoji) == "⭐":
                #update the reactions sent in database
                await DatabaseFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="star",num=1)
                async with self.bot.pool.acquire() as connection:
                    async with connection.transaction():
                        starboard_channel=self.bot.get_channel(config.starboard_channel_id) 
                        star_message = await connection.fetchrow("SELECT * FROM starboard WHERE root_message_id=$1",message.id)
                        
                        if star_message == None and reaction.count >= config.stars_required_for_starboard:
                            embed=discord.Embed(color = channel.guild.me.colour,timestamp=message.created_at,description=message.content)
                            embed.set_author(name=message.author.name, icon_url= f"{message.author.avatar_url}")
                            embed.add_field(name="Source:", value=f"[Jump]({message.jump_url})", inline=False)
                            if len(message.attachments): #basically if len !=0
                                embed.set_image(url=message.attachments[0].url)
                            embed.set_footer(text=f"{message.id} ")
                            StarMessage = await starboard_channel.send(f"{reaction.count} ⭐ {channel.mention}",embed=embed)                    
                            # if user.bot:pass
                            #     #await ctx.send(f"{user.name} is a bot. Bots don't need accounts.")
                            # else:                 
                            empty_json=json.dumps({})          
                            await connection.execute('INSERT INTO starboard (root_message_id,star_message_id,stars,awards) VALUES ($1,$2,$3,$4)',message.id,StarMessage.id,0,empty_json)
                        
                        elif star_message != None and reaction.count >= config.stars_required_for_starboard:
                            star_message=dict(star_message)
                            #star_message["stars"] = reaction.count
                            StarMessage= await starboard_channel.fetch_message(star_message["star_message_id"])
                            await StarMessage.edit(content=f"{reaction.count} ⭐ {channel.mention}")
                            await connection.execute("UPDATE starboard SET stars = $1 WHERE root_message_id=$2",reaction.count,message.id)
                        
                        else:pass
                        #means stars are less that the required number 
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):  
        DatabaseFunctions = self.bot.get_cog('DatabaseFunctions') 
        channel=self.bot.get_channel(payload.channel_id) 
        user=self.bot.get_user(payload.user_id)
        message= await channel.fetch_message(payload.message_id)
        emoji=payload.emoji  
        all_reacts = message.reactions
        if user.bot:
            return


        if str(emoji) == "⭐":
            #update the reactions sent in database
            await DatabaseFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="star",num=-1)
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    starboard_channel=self.bot.get_channel(config.starboard_channel_id) 
                    star_message = await connection.fetchrow("SELECT * FROM starboard WHERE root_message_id=$1",message.id)                 
                    #if this message is not in the database/ it has not been starred earlier
                    if star_message == None:
                        return
                        
                    star_message=dict(star_message)
                    StarMessage= await starboard_channel.fetch_message(star_message["star_message_id"])

                    if len(all_reacts) == 0 :
                        await StarMessage.delete()
                        await connection.execute("DELETE FROM starboard WHERE root_message_id=$1",message.id)
            
                    for reaction in all_reacts:
                        if reaction.count < config.stars_required_for_starboard:
                            await StarMessage.delete()
                            await connection.execute("DELETE FROM starboard WHERE root_message_id=$1",message.id)
                        
                        elif reaction.count >= config.stars_required_for_starboard:
                            await StarMessage.edit(content=f"{reaction.count} ⭐ {channel.mention}")
                            await connection.execute("UPDATE starboard SET stars = $1 WHERE root_message_id=$2",reaction.count,message.id)
    


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
    async def star(self,ctx):
        total_stars=0
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                
                all_rows = await connection.fetch("SELECT * FROM starboard")
                for row in all_rows:
                    row=dict(row)
                    total_stars= total_stars + row["stars"]
                
                embed=discord.Embed(title=f"Starboard",description=f"Starboard stuff")
                embed.add_field(name="Total stars:",value=f"{total_stars}",inline=True)
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