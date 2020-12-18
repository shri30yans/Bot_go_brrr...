import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks

colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
            0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]

class Utility(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
   
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Invite", help='Sends Invite link for bot \n Yeet invite ')
    async def invite(self,ctx):
        embed= discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
        #insert_field_at(index, *, name, value, inline=True)¶
        embed.add_field(name="You can invite me here:",value="[Direct Invite](https://discord.com/api/oauth2/authorize?client_id=750236220595896370&permissions=8&scope=bot) \n[Top.gg Invite](https://top.gg/bot/750236220595896370) \n[DBL Invite](https://discordbotlist.com/bots/yeet-bot) ",inline=False)
        embed.add_field(name="Join our Discord Support Server:",value="[Discord Server](https://discord.gg/C3XkFwrdER)",inline=False)
        embed.add_field(name="Mail for business enquiries:",value="yeetbotdev@gmail.com",inline=False)
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)
    
    
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
        embed.add_field(name="Support server",value=f"[Join the support server.](https://top.gg/bot/750236220595896370/vote)",inline=False)
        embed.add_field(name="Vote",value=f"[Top.gg Vote](https://top.gg/bot/750236220595896370/vote)",inline=False)
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
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        await message.edit(embed=embed)



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
        