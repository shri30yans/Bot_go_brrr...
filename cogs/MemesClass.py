import os, sys, discord, platform, random, aiohttp, json,time,asyncio
from discord.ext import commands,tasks
import praw,prawcore
colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
            0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]

reddit = praw.Reddit(
     client_id="us0vshvKCbFtaQ",
     client_secret="gAgY9u07CSK3nUqWRkCPbvvvqSvEzA",
     user_agent="u/Shri30yans Yeet Bot",
 )

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Meme",aliases=['memes'], help='Posts a top meme from a random subreddit \n\"Yeet meme\" \n Alias:memes')
    async def meme(self,ctx):
        memes_subreddits_list=["memes","dankmemes"]
        random_subreddit=random.choice(memes_subreddits_list)
        submission = reddit.subreddit(random_subreddit).random()
        #embed = discord.Embed(title = submission.title,description=f"<:reddit_upvote:779666235687829514>  {submission.score}  <:reddit_downvote:779666235612856320>",color = random.choice(colourlist),timestamp=ctx.message.created_at,url=submission.url)
        embed = discord.Embed(title = submission.title,color = random.choice(colourlist),url=submission.url)
        embed.set_image(url=submission.url)
        
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"\U0001f7e2  {submission.score}  \U0001f534  • Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)



        '''async with aiohttp.ClientSession() as cs:
            memes_subreddits_list=["memes","dankmemes"]
            random_subreddit=random.choice(memes_subreddits_list)
            url="https://www.reddit.com/r/"+ random_subreddit
            url=url + "/new.json?sort=hot"

            async with cs.get(url) as r:
                res = await r.json()
                embed = discord.Embed(title = "Meme", color = random.choice(colourlist),timestamp=ctx.message.created_at)
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                author_avatar=ctx.author.avatar_url
                embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                #embed.set_footer(text = f"r/{random_subreddit} | Yeet Bot |")
                await ctx.send(embed=embed)'''
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="HolUp",aliases=['holdup'], help='Posts a top meme from the Holup subreddit \n\"Yeet holup\" \n Alias: holdup ')
    async def holup(self,ctx):
        submission = reddit.subreddit("holup").random()
        embed = discord.Embed(title = submission.title,color = random.choice(colourlist),url=submission.url)
        embed.set_image(url=submission.url)
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"\U0001f7e2  {submission.score}  \U0001f534  • Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)
    
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="RedSearch",aliases=['redditsearch'], help='Posts a random post from a subreddit \n\" +RedSearch meme\" \n Alias: RedditSearch ')
    async def reddit_search(self,ctx,subreddit_entered):
        try:
            submission = reddit.subreddit(subreddit_entered).random()
            if submission.over_18 == True and not ctx.channel.is_nsfw():
                embed = discord.Embed(title ="NSFW Post",description=f"The requested post is NSFW. Please use this in a NSFW channel.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
                author_avatar=ctx.author.avatar_url
                embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed) #stops NSFW posts from showing up
            else:
                    embed = discord.Embed(title = submission.title,color = random.choice(colourlist),url=submission.url)
                    embed.set_image(url=submission.url)
                    author_avatar=ctx.author.avatar_url
                    embed.set_footer(icon_url= author_avatar,text=f"\U0001f7e2  {submission.score}  \U0001f534  • Requested by {ctx.message.author} • Yeet Bot ")
                    await ctx.send(embed=embed)

        except prawcore.exceptions.NotFound:
            embed = discord.Embed(title ="Invalid Subreddit",description=f"Enter a valid subreddit you noob <:YB_you_noob:775389521700585502> .",color = random.choice(colourlist),timestamp=ctx.message.created_at)
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(embed=embed) #stops NSFW posts from showing up

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="FBI", help='Sends the FBI open up! meme video \n\"Yeet FBI\"')
    async def FBI(self,ctx):
        await ctx.send("https://www.youtube.com/watch?v=4wX2xBOuzRg&ab_channel=MoeLester")
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="NoYou",aliases=['nou', 'uno'], help='No You! \n\"Yeet NoYou\" \n Aliases:nou, uno ')
    async def no_u(self,ctx):
        FBI_list=["https://media1.tenor.com/images/250955750a396a0b260279170b148079/tenor.gif?itemid=14951171","https://media3.giphy.com/media/MQwnNsDJ1MJZ0E0w1u/giphy.gif"
                    "https://media2.giphy.com/media/TEFUs4Qf0hEMLVWv4Z/giphy.gif?cid=ecf05e4767272b3fdf5004baebafec97fad5b7e76bde694a&rid=giphy.gif"]
        link= random.choice(FBI_list)
        embed = discord.Embed(title = "NO YOU!", color = random.choice(colourlist),timestamp=ctx.message.created_at)
        embed.set_image(url=link)
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)
    
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="69",aliases=['nice'], help='Sends a random nice gif \n\"Yeet 69\" \nAliases:nice ')
    async def Nice_69(self,ctx):
        nice_gif_list=[ "https://media.giphy.com/media/3M9CR4S2KFNyOIqHGg/giphy.gif",
                "https://media.giphy.com/media/8Odq0zzKM596g/giphy.gif",
                "https://media.giphy.com/media/3oFyDq6BEAim8LG836/giphy.gif",
                "https://tenor.com/Ydrb.gif",
                "https://tenor.com/5oUV.gif",
                "https://tenor.com/vz2N.gif",
                "https://tenor.com/sbue.gif",
                "https://tenor.com/K418.gif",
                "https://tenor.com/sbvk.gif"]
        response = random.choice(nice_gif_list)
        await ctx.send(response)
    

    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Exist",aliases=['life'], help='Yeet Bot having existensial crisis \n\"Yeet exist\" \nAliases:life ' )
    async def exist(self,ctx):
        existential_crisis_vids_list=["https://media.giphy.com/media/XhWvodKpLzk40/giphy.gif",
                                    "https://media.giphy.com/media/ZaKcIYMjNYNf4lEuC7/giphy.gif",
                                    "https://media1.tenor.com/images/fc3d4f85a97f6be145a1a55d1628fa43/tenor.gif?itemid=8715600","https://tenor.com/vr9m.gif",
                                    "https://tenor.com/xRPe.gif","https://tenor.com/AlaC.gif",
                                    "https://media.giphy.com/media/JDfQEoSR7Rpgk/giphy.gif",]
        link= random.choice(existential_crisis_vids_list)
        embed = discord.Embed(title = "What is life?", color = random.choice(colourlist),timestamp=ctx.message.created_at)
        embed.set_image(url=link)
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        #embed.set_author(name=str(ctx.author),icon_url=str(ctx.author.avatar_url_as(static_format="png", size=2048)))
        await ctx.send(embed=embed)
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Lmao", help='Sends lmao emojis \n\"Yeet lmao\"')
    async def lmao(self,ctx):
        await ctx.send("<:DiCaprio_laugh:774181368544100352><:my:774181665093976094><a:bootyshake:774181372230500362><:out:774181367034281987>")

def setup(bot):
    bot.add_cog(Memes(bot))