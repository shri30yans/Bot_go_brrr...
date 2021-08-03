# https://viddit.red/1/?link=https%3A%2F%2Fwww.reddit.com%2Fr%2FHolUp%2Fcomments%2Fo7guog%2F18_years_old%2F

# https://www.reddit.com/r/HolUp/comments/o7guog/18_years_old/
import random,aiohttp,asyncio,discord
import lxml.html
from discord.ext import commands

class RedditDownloader(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    #@commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="download", help='Give your credits to others\nFormat: `?Give @user amount_to_give`')
    async def reddit_downloader(self,ctx,link):
        #link=str(input("Enter the Reddit post link:"))
        link_encode_dict={"/":r"%2F",":":r"%3A",}
        for x in link_encode_dict:
            link=link.replace(x,link_encode_dict[x])               
        print(link)
        fetch_link="https://viddit.red/1/?link="+ link
        html_doc=await self.get_page_html(link=fetch_link)
        doc=lxml.html.fromstring(str(html_doc))
        f=doc.xpath('//*[@id="results"]/div/div/div[3]/div[1]/div[1]/a')
        print(f)



    async def get_page_html(self,link,headers_list=[{"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"},{"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"},{"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"},{"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}],):
        headers = random.choice(headers_list)
        try:
            async with aiohttp.ClientSession(headers=headers,trust_env=True) as session:
                async with session.get(url=link) as response:
                    if response.status != 200:
                        print(f'Server returned {response.status} link:{link}')
                        return False
                    else:
                        html = await response.text()
                        return html
        except asyncio.TimeoutError:
            return False

def setup(bot):
    bot.add_cog(RedditDownloader(bot))