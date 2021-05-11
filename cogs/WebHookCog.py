import discord,random,aiohttp,json,asyncio
from discord.ext import commands,tasks
# import utils.awards as awards
# import config   
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
    
class WebHook(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_message(self,message):
        print(message.content)
        if message.content.startswith(";") and message.content.endswith(";"):
            emoji=await self.get_emoji(message)
            if emoji != None:
                await message.delete()
                await self.send_message(message,emoji)

        
           
    async def send_message(self,message,emoji):
        user=message.author
        url = await self.get_webhook_url(message)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
            await webhook.send(emoji, username=user.display_name,avatar_url=user.avatar_url)
            #await webhook.send('Hello World', username=user.name,avatar_url=user.avatar_url)

    async def get_webhook_url(self,message):
        channel=message.channel
        webhook_urls= await channel.webhooks()
        print(webhook_urls)
        for webhook in webhook_urls:
            if webhook.name=="Emoji Webhook":
                return webhook.url
            else:
                webhook=await channel.create_webhook(name="Emoji Webhook", avatar=None, reason="Webhook to use animated emojis.")
                return webhook.url
    
    async def get_emoji(self,message):
        emoji_name = message.content.lower()[1:-1]
        for emoji in self.bot.emojis:
            if emoji_name == emoji.name.lower():
                return emoji

            

    

def setup(bot):
    bot.add_cog(WebHook(bot))