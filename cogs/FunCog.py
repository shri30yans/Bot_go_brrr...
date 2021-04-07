import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import config

colourlist=config.embed_colours
    
class Fun(commands.Cog,name="Productivity or some shit"):
    def __init__(self, bot):
        self.bot = bot    
    
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Concentrate",aliases=["concentratationmode","studytime","failinginexams","sendhelp"], help=f'Makes sure you concentrate \n \"{config.prefix}Concentratation mode 5m\". Time can be entered in (s|m|h|d), Default time is 10 mins.Aliases:"ConcentratationMode","StudyTime","FailinginExams","sendhelp"')
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


def setup(bot):
    bot.add_cog(Fun(bot))