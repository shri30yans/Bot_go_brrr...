import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config   

colourlist=config.embed_colours

#All reaction listeners take place in Reactions.py
    
class Starboard(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot


    
    
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