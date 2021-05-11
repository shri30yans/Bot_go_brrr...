import discord,random,aiohttp,json,asyncio
from discord.ext import commands,tasks,menus
import config   
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
colourlist=config.embed_colours
    
class WebHook(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.content.startswith(";") and message.content.endswith(";"):
            emoji=await self.get_emoji(message)
            if emoji != None:
                await message.delete()
                await self.send_message(message,emoji)
            else:
                await message.add_reaction("\U0000274c")

        
    async def send_message(self,message,emoji):
        user=message.author
        url = await self.get_webhook_url(message)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
            await webhook.send(emoji, username=user.display_name,avatar_url=user.avatar_url)

    async def get_webhook_url(self,message):
        channel=message.channel
        webhook_urls= await channel.webhooks()
        for webhook in webhook_urls:
            if webhook.name=="Emoji Webhook":
                return webhook.url
            else:
                webhook_url = await self.create_webhook(channel)
                return webhook_url
        
        if len(webhook_urls) == 0:
            webhook_url = await self.create_webhook(channel)
            return webhook_url


    async def create_webhook(self,channel):
        webhook = await channel.create_webhook(name="Emoji Webhook", avatar= await self.bot.user.avatar_url.read(), reason="Webhook to use animated emojis.")
        return webhook.url
    
    async def get_emoji(self,message):
        emoji_name = message.content.lower()[1:-1]
        for emoji in self.bot.emojis:
            if emoji_name == emoji.name.lower():
                return emoji


    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Emojis", help=f"Shows the available reactions that you can use with `;reaction-name;` \n \"{config.prefix}emojis reaction-name\"")
    async def reaction_search(self,ctx,*emojis_keyword_tuple):
        emojis_keyword_list=list(emojis_keyword_tuple)
        for i in range(len(emojis_keyword_list)):
            emojis_keyword_list[i] = emojis_keyword_list[i].lower() 
            #Iterate through string_list and convert each elem to lowercase                         
        selected_emojis_list=[]
        # Test if all elements are present in list 
        # Using list comprehension + all()      
        for i in self.bot.emojis:
            emoji_name=i.name.lower()
            if all(ele in emoji_name for ele in emojis_keyword_list):
                selected_emojis_list.append(i)
            
        if selected_emojis_list==[]:
                embed = discord.Embed(title ="Emoji not found",description=f"The emoji with the keywords :  {str(emojis_keyword_list)[1:-1]}  is not found. Please try a different keyword.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
                author_avatar=ctx.author.avatar_url
                embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed)
        else:
            length=0
            emoji_string=""
            Emoji_list_seperated=[]
            for elem in selected_emojis_list:
                length=length+len(str(elem))+len(str(elem.name))+15
                if length<850:
                    emoji_string=emoji_string + str(elem) +"    |    `;" + str(elem.name) + ";` \n"
                    
                else:
                    Emoji_list_seperated.append(emoji_string)
                    emoji_string=str(elem) +"    |     ` ;" + str(elem.name) + "; ` \n"
                    length=0
            Emoji_list_seperated.append(emoji_string)
                
            if len(Emoji_list_seperated)>1:
                embeds_list = []
                for embed_string in Emoji_list_seperated:
                    embed_string_index=Emoji_list_seperated.index(embed_string)
                    embeds_list.append(discord.Embed(title =f"{len(selected_emojis_list)} Emoji's found!",description=f"The requested keywords: {str(emojis_keyword_list)[1:-1]}  have the {len(selected_emojis_list)} results: \n Paste the name of anyone of the emojis in chat.",color = random.choice(colourlist),timestamp=ctx.message.created_at).add_field(name="Search results:",value=f"{embed_string}\n").set_footer(icon_url= ctx.author.avatar_url,text=f" Page: {embed_string_index+1} of {len(Emoji_list_seperated)+1} • Requested by {ctx.message.author} • Yeet Bot "))
                menu = menus.MenuPages(EmbedPageSource(embeds_list, per_page=1))
                await menu.start(ctx)
            else:
                embed = discord.Embed(title =f"{len(selected_emojis_list)} Emoji's found!",description=f"The requested keywords: {str(emojis_keyword_list)[1:-1]}  have the {len(selected_emojis_list)} results:",color = random.choice(colourlist),timestamp=ctx.message.created_at)
                embed.add_field(name="Search results:",value=f"{Emoji_list_seperated[0]}")
                author_avatar=ctx.author.avatar_url
                embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed)

            

    

def setup(bot):
    bot.add_cog(WebHook(bot))

class EmbedPageSource(menus.ListPageSource):
    async def format_page(self, menu, embed):
        return embed