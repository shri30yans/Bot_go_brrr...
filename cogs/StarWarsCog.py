import os, sys, discord, platform, random, aiohttp, json,time,asyncio,urllib
from discord.ext import commands,tasks
import praw,prawcore
colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
            0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]
MemeDir = "utils/Media/Meme Templates"

reddit = praw.Reddit(
     client_id="us0vshvKCbFtaQ",
     client_secret="gAgY9u07CSK3nUqWRkCPbvvvqSvEzA",
     user_agent="u/Shri30yans Yeet Bot",
 )

class StarWarsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Meme",aliases=['memes'], help='Posts a top meme from a random subreddit \n\"Yeet meme\" \n Alias:memes')
    async def star_wars_meme(self,ctx):
        memes_subreddits_list=["starwarsmemes","PrequelMemes","OTMemes","SequelMemes"]
        random_subreddit=random.choice(memes_subreddits_list)
        submission = reddit.subreddit(random_subreddit).random()   
        if submission.over_18 == True and not ctx.channel.is_nsfw():
            embed = discord.Embed(title ="NSFW Post",description=f"The requested post is NSFW. Please use this in a NSFW channel.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(embed=embed) #stops NSFW posts from showing up
        else:
            embed = discord.Embed(title = submission.title,color = random.choice(colourlist),url=submission.url)
            embed.set_image(url=submission.url)
            embed.set_footer(icon_url=ctx.author.avatar_url,text=f"\U0001f7e2  {submission.score}  \U0001f534  • Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)
        



                # async with aiohttp.ClientSession() as cs:
                #     memes_subreddits_list=["memes","dankmemes"]
                #     random_subreddit=random.choice(memes_subreddits_list)
                #     url="https://www.reddit.com/r/"+ random_subreddit
                #     url=url + "/new.json?sort=hot"
                #     async with cs.get(url) as r:
                #         res = await r.json()
                #         embed = discord.Embed(title = "Meme", color = random.choice(colourlist),timestamp=ctx.message.created_at)
                #         embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                #         author_avatar=ctx.author.avatar_url
                #         embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                #         #embed.set_footer(text = f"r/{random_subreddit} | Yeet Bot |")
                #         await ctx.send(embed=embed)
    
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="StarWars", help='Posts a random post from the StarWars subreddit \n\" +Starwars\" \n Alias: SW ')
    async def star_wars_subreddit(self,ctx):
        submission = reddit.subreddit("Starwars").random()   
        if submission.over_18 == True and not ctx.channel.is_nsfw():
            embed = discord.Embed(title ="NSFW Post",description=f"The requested post is NSFW. Please use this in a NSFW channel.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(embed=embed) #stops NSFW posts from showing up
        else:
                embed = discord.Embed(title = submission.title,color = random.choice(colourlist),url=submission.url)
                embed.set_image(url=submission.url)
                embed.set_footer(icon_url=ctx.author.avatar_url,text=f"\U0001f7e2  {submission.score}  \U0001f534  • Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed)
    
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Wiki", help='Gets Wiki data \n\" +wiki\" \n Alias: SW ')
    async def wiki(self,ctx,keyword):
        async with aiohttp.ClientSession() as session:
            url="https://swapi.dev/api/people/?search="
            url=url+keyword
            async with session.get(url) as resp:
                response= json.loads(str(await resp.text()))
                #print(response)
                number_of_responses = response.get("count")
                if number_of_responses==0:
                    embed = discord.Embed(title ="No Search Results",description=f"Enter a different keyword or be more specific.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
                    embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(response)
    
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Quote",aliases=["quotes"], help='Gets a Star Wars Quote \n\" +quote\" \n Alias: quotes')
    async def quote(self,ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote") as resp:
                response= json.loads(str(await resp.text()))
                #print(response)
                quote = response.get("starWarsQuote")
                embed = discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
                embed = discord.Embed(title ="Star Wars Quotes",description=quote,color = random.choice(colourlist),timestamp=ctx.message.created_at)
                embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed)

    '''@commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Gif", help='Posts a StarWars gif  \n\" +gif keyword keyword\" ')
    async def star_wars_gif(self,ctx,*arguments):
        response =  ' '.join(arguments) 
        params = urllib.parse.urlencode({
                "q": f"'Star Wars' + {response}",
                "api_key": "oDTSbME4wt0vrDLJ1r1ZEL1tlxuXLFwy",
                "limit": "30",
                "rating": "pg-13"
                })
        async with aiohttp.ClientSession() as session:
            async with session.get("http://api.giphy.com/v1/gifs/search",params=params) as resp:
                response= json.loads(await resp.text())
                meta=response["meta"]["status"]
                if meta==200:
                    response=response["data"][random.randint(0,(len(response["data"]))-1)]["images"]["downsized_large"]["url"]
                    await ctx.send(response)
                else:
                    embed = discord.Embed(title ="No Search Results",description=f"Enter a different keyword or be more specific.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
                    embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                    await ctx.send(embed=embed)'''

    '''@commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="Gif", help='Posts a StarWars gif  \n\" +gif keyword keyword\" ')
    async def star_wars_gif(self,ctx,*arguments):
        apikey = "QWY99I82C6S0"  # test value
        lmt = 5
        psearch ='Star Wars' + (' '.join(arguments)) 

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.tenor.com/v1/autocomplete?key=%s&q=%s&limit=%s" % (apikey, psearch, lmt)) as resp:
                response= json.loads(await resp.text())
                #print(response)
                if response["status_code"] == 200:
                # return the search predictions
                    search_term_list = json.loads(response.content)["results"]
                    print (search_term_list)
                else:
                    # handle a possible error
                    search_term_list = []
                #response=response["data"][random.randint(0,(len(response["data"]))-1)]["images"]["downsized_large"]["url"]
                await ctx.send(response)'''
    

    
def setup(bot):
    bot.add_cog(StarWarsCommands(bot))