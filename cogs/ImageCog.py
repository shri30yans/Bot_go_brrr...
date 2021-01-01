import os, sys, discord, platform, random, aiohttp, json,time,asyncio,textwrap,pathlib,colour
from discord.ext import commands,tasks
from PIL import Image,ImageOps
import utils.addtext
from io import BytesIO
from typing import Union
#MemeDir = "utils/Images/Meme Templates/"
colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
            0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]
class ImageEditor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.cooldown(1, 12, commands.BucketType.user)
    @commands.group(name="text",aliases=['swtext'],invoke_without_command=True, help=f'Create memes with inbuilt templates or create a custom meme \n\" Yeet memecreate <templatename> \" or \"Yeet memecreate custom <attachment> \" \n Alias: creatememe')
    async def SW_font_convert(self,ctx):
        #image = utils.addtext.star_wars_font(text="Star Wars")
        image = utils.addtext.star_wars_font(text="Star Wars")
        output_buffer = BytesIO()
        image.save(output_buffer, "png")  # or whatever format
        output_buffer.seek(0)
        await ctx.send(file=discord.File(fp=output_buffer, filename="Star Wars Font"))
        #image.show()

    @commands.cooldown(1, 12, commands.BucketType.user)
    @commands.group(name="MemeList",aliases=['listmeme'],invoke_without_command=True, help=f'Create memes with inbuilt templates or create a custom meme \n\" Yeet memecreate <templatename> \" or \"Yeet memecreate custom <attachment> \" \n Alias: creatememe')
    async def memelist(self,ctx):
        embed=discord.Embed(title="Meme Templates",color = random.choice(colourlist),timestamp=ctx.message.created_at)
        embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        embed.add_field(name="List of Meme Templates:",value='''• abilitytospeak \n • anakinliar/ liar \n• archives/ archivesincomplete \n• everywordwrong/ everywordwrong \n• ikwhattodo/ strengthtodoit \n• democracy/ ilovedemocracy \n• no \n• unexpected \n• sworetodestroy \n• underestimate \n• confusion \n• destroyyou \nUse \" r memecreate template-name\" to create a meme\n To create a custom meme use \"r memecreate custom\"''')
        await ctx.send(embed=embed)
    
    #exception discord.ext.commands.MaxConcurrencyReached(number, per)
    #Maximum ongoing is 1 per user
    #@commands.max_concurrency(1)
    @commands.cooldown(1, 12, commands.BucketType.user)
    @commands.max_concurrency(1, commands.BucketType.user, wait=False)
    @commands.group(name="MemeCreate",aliases=['creatememe'],invoke_without_command=True, help=f'Create memes with inbuilt templates or create a custom meme \n\" Yeet memecreate <templatename> \" or \"Yeet memecreate custom <attachment> \" \n Alias: creatememe')
    async def memecreate(self,ctx,*template_name):
        template_name = ''.join(template_name)
        template_name=template_name.lower()

        
        async def questions():
            top_text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the top text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
            bottom_text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the bottom text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
            if top_text_strings.lower()=="blank":
                top_text_strings=""
            if bottom_text_strings.lower()=="blank":
                bottom_text_strings=""
            return top_text_strings,bottom_text_strings

        if template_name in ["abilitytospeak"]:
            text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the top text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
            if text_strings.lower()=="blank":
                text_strings=""
            img = Image.open("utils/Images/Meme Templates/ability_to_speak.jpg")
            image=utils.addtext.generate_meme(img,top_text=text_strings,bottom_text="")
        
        elif template_name in ["liar","anakinliar"]:
            text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the top text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
            if text_strings.lower()=="blank":
                text_strings=""
            img = Image.open("utils/Images/Meme Templates/anakin_liar.jpg")
            image=utils.addtext.generate_meme(img,top_text=text_strings,bottom_text="")
        
        elif template_name in ["archives","archivesincomplete"]:
            text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the top text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
            if text_strings.lower()=="blank":
                text_strings=""
            img = Image.open("utils/Images/Meme Templates/archives_incomplete.jpg")
            image=utils.addtext.generate_meme(img,top_text=text_strings,bottom_text="")
        
        elif template_name in ["everywordwrong","everyword"]:
            text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the top text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
            if text_strings.lower()=="blank":
                text_strings=""
            img = Image.open("utils/Images/Meme Templates/every_word_wrong.jpg")
            image=utils.addtext.generate_meme(img,top_text=text_strings,bottom_text="")
        
        elif template_name in ["ikwhattodo","strengthtodoit"]:
            text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the top text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
            if text_strings.lower()=="blank":
                text_strings=""
            img = Image.open("utils/Images/Meme Templates/ik_what_to_do.jpg")
            image=utils.addtext.generate_meme(img,top_text=text_strings,bottom_text="")
        
        elif template_name in ["no"]:
            top_text_strings,bottom_text_strings=await questions()
            img = Image.open("utils/Images/Meme Templates/luke_no.jpg")
            #image=utils.addtext.generate_meme(img,top_text=top_text_strings,bottom_text=bottom_text_strings)
            image=utils.addtext.add_text_height(img,top_text=top_text_strings,bottom_text=bottom_text_strings,y1=100,y2=223)
        
        elif template_name in ["democracy","ilovedemocracy"]:
            text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the top text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
            if text_strings.lower()=="blank":
                text_strings=""
            img = Image.open("utils/Images/Meme Templates/palaptine_democracy.jpg")
            image=utils.addtext.generate_meme(img,top_text=text_strings,bottom_text="")
        
        elif template_name in ["unexpected"]:
            text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the top text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
            if text_strings.lower()=="blank":
                text_strings=""
            img = Image.open("utils/Images/Meme Templates/unexpected_this_is.jpg")
            image=utils.addtext.generate_meme(img,top_text=text_strings,bottom_text="")
        
        elif template_name in ["confusion"]:
            text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the top text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
            if text_strings.lower()=="blank":
                text_strings=""
            img = Image.open("utils/Images/Meme Templates/visible_confusion.jpg")
            image=utils.addtext.generate_meme(img,top_text=text_strings,bottom_text="")
        
        elif template_name in ["sworetodestroy"]:
            text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the top text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
            if text_strings.lower()=="blank":
                text_strings=""
            img = Image.open("utils/Images/Meme Templates/you_have_become_the_very_thing_swore_to_destroy.jpg")
            image=utils.addtext.generate_meme(img,top_text=text_strings,bottom_text="")
        
        elif template_name in ["underestimate"]:
            text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the top text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
            if text_strings.lower()=="blank":
                text_strings=""
            img = Image.open("utils/Images/Meme Templates/you_underestimate_my_power.jpg")
            image=utils.addtext.generate_meme(img,top_text=text_strings,bottom_text="")
        
        elif template_name in ["destroy","destroyyou"]:
            text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the top text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
            if text_strings.lower()=="blank":
                text_strings=""
            img = Image.open("utils/Images/Meme Templates/dont_make_me_destroy.png")
            image=utils.addtext.generate_meme(img,top_text=text_strings,bottom_text="")



            
        else:
            embed=discord.Embed(title="No Meme Template Found",description=f'The requested Meme Template was not found. Try \"MemeList\" to get a list of a the templates.',color = random.choice(colourlist),timestamp=ctx.message.created_at)
            embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(embed=embed)
            return
        
        output_buffer = BytesIO()
        image.save(output_buffer, "png")  # or whatever format
        output_buffer.seek(0)
        await ctx.send(file=discord.File(fp=output_buffer, filename="StarWarsMeme.png"))       
        
        
        # async def template_finding_function(ctx):
        #     question_embed=await ctx.send(embed=discord.Embed(title ="Meme Generator",description="Enter the meme templates name:\n**Meme Templates:**\n • meandtheboys \n • mikeawkward \n • alonespongebob \n • cursedsongebob\n • stonks \n • suprisedpikachu\n To create a custom meme use \"Yeet memecreate custom\"\nEnter the name of the template below:",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        #     try:
        #         template_to_do= await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel and m.content.lower() in choices))
        #     except asyncio.TimeoutError:
        #         await question_embed.edit(embed=discord.Embed(title ="Timeout Error",description="You took too much time, ya retarded monkey",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        #     else: 
        #         return template_to_do.content
        
        # if template_name==None:
        #     template_name=await template_finding_function(ctx)
        #     template_name=template_name.lower()    
        # else:
            
    @memecreate.command(name="custom",aliases=['creatememe'], help=f'Create memes with a custom template \n\" Yeet memecreate custom \"  \n Alias: creatememe')
    async def custom(self,ctx):    
        
        top_text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the top text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
        bottom_text_strings=await self.text_input_function(ctx,"Meme Creator","Enter the bottom text: (50 Characters Max)\n Type \"Blank\" to keep it blank.")
        if top_text_strings.lower()=="blank":
            top_text_strings=""
        if bottom_text_strings.lower()=="blank":
            bottom_text_strings=""

        if len(ctx.message.attachments) == 0:
            img=await self.upload_function(ctx,"Meme Generator")
            img=img[0]
            #gets discord.Asset
        else:
            img=ctx.message.attachments[0]
        asset = img
        #asset = asset_attachment
        #Converts it into bytes
        bytes = await asset.read()
        #converts it into a PIL Image object
        with Image.open(BytesIO(bytes)) as attachment:
            image=utils.addtext.generate_meme(attachment,top_text=top_text_strings,bottom_text=bottom_text_strings)
            output_buffer = BytesIO()
            image.save(output_buffer, "png")  # or whatever format
            output_buffer.seek(0)
            await ctx.send(file=discord.File(fp=output_buffer, filename="Created-Meme-Yeet_Bot.png"))
    
    async def text_input_function(self,ctx,title:str,text:str):
        question_embed=await ctx.send(embed=discord.Embed(title =title,description=text,color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        try:
            text= await self.bot.wait_for('message', timeout=30.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            await question_embed.edit(embed=discord.Embed(title ="Timeout Error",description="You took too much time, ya retarded monkey",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        else: 
            if len(text.content)> 50:
                embed=discord.Embed(title="<:warn:789487083802460200> | Too many Characters ",description="How many letters will you type, you retard?",color = random.choice(colourlist))
                embed.add_field(name="Type only 50 characters in your sentence.",value=f"You typed {len(text.content)} letters, dumbshit! Type the top text again.", inline=False)
                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed)
                return await self.text_input_function(ctx,title,text)
            else:
                return str(text.content)

    async def upload_function(self,ctx,name):
        question_embed=await ctx.send(embed=discord.Embed(title =f"{name}",description="**Upload the image:**\nPlease upload a static image in png/jpg for best results.",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        try:
            image_message= await self.bot.wait_for('message', timeout=30.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            await question_embed.edit(embed=discord.Embed(title ="Timeout Error",description="You took too much time, ya retarded monkey",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        else:
            if len(image_message.attachments) > 1:
                embed=discord.Embed(title="<:warn:789487083802460200> | Multiple Attachments ",description="Attach one attachment, ya braindead zombie! ",color = random.choice(colourlist))
                embed.add_field(name="Something went wrong. Try again later",value=f"You attached {len(ctx.message.attachments)} attachments. Only attach one ", inline=False)
                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed)

            elif len(image_message.attachments) == 1:
                return image_message.attachments
                
            else:
                embed=discord.Embed(title="<:warn:789487083802460200> | No Attachments ",description="Boi, you don't have any attachment. ",color = random.choice(colourlist))
                embed.add_field(name="lol u dumb",value="Where required attachment ya retard? Try Again and attach a image this time, genius", inline=False)
                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed) 
                return await self.upload_function(ctx,name)

def setup(bot):
    bot.add_cog(ImageEditor(bot))