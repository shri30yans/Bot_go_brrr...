import os, sys, discord, platform, random, aiohttp, json,time,asyncio,textwrap,pathlib,colour
from discord.ext import commands,tasks
from PIL import Image, ImageDraw, ImageFont,ImageFilter,ImageOps
import utils.addtext,utils.image_effects
from io import BytesIO
from typing import Union
MediaDir = pathlib.Path(__file__).parent / "Media"
MemeDir = pathlib.Path(__file__).parent / "Media"/ "Meme Templates"


colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
            0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]

class Image_Functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.cooldown(1, 12, commands.BucketType.user)
    @commands.group(name="memecreate",aliases=['creatememe'],invoke_without_command=True, help=f'Create memes with inbuilt templates or create a custom meme \n\" Yeet memecreate <templatename> \" or \"Yeet memecreate custom <attachment> \" \n Alias: creatememe')
    #async def memecreate(self,ctx,colour:discord.Colour="blue",*,text):
    async def memecreate(self,ctx,template_name:str=None):
        choices=["meandtheboys","mike","mikeawkward","alonespongebob","sadspongebobalone","cursedspongebob","spongebobcursed","stonks","suprisedpikachu"]
                
        async def template_finding_function(ctx):
            question_embed=await ctx.send(embed=discord.Embed(title ="Meme Generator",description="Enter the meme templates name:\n**Meme Templates:**\n • meandtheboys \n • mikeawkward \n • alonespongebob \n • cursedsongebob\n • stonks \n • suprisedpikachu\n To create a custom meme use \"Yeet memecreate custom\"\nEnter the name of the template below:",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
            try:
                template_to_do= await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel and m.content.lower() in choices))
            except asyncio.TimeoutError:
                await question_embed.edit(embed=discord.Embed(title ="Timeout Error",description="You took too much time, ya retarded monkey",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
            else: 
                return template_to_do.content
        
        if template_name==None:
            template_name=await template_finding_function(ctx)
            template_name=template_name.lower()    
        else:
            template_name=template_name.lower()
            top_text_strings=await self.top_text_function(ctx)
            bottom_text_strings=await self.bottom_text_function(ctx)
            if top_text_strings=="None":
                top_text_strings=""
            if bottom_text_strings=="None":
                bottom_text_strings=""

            async with ctx.typing():

                if template_name in ["meandtheboys"]:
                    img = Image.open(MemeDir/"meandtheboys.png")
                    image=utils.addtext.generate_meme(img,top_text=top_text_strings,bottom_text=bottom_text_strings)
                elif template_name in ["mike","mikeawkward"]:
                    img = Image.open(MemeDir/"mikeawkward.png")
                    image=utils.addtext.generate_meme(img,top_text=top_text_strings,bottom_text=bottom_text_strings)
                elif template_name in ["alonespongebob","sadspongebobalone"]:
                    img = Image.open(MemeDir/"sadspongebobalone.jpg")
                    image=utils.addtext.generate_meme(img,top_text=top_text_strings,bottom_text=bottom_text_strings)
                elif template_name in ["cursedspongebob","spongebobcursed"]:
                    img = Image.open(MemeDir/"spongebobcursed.jpg")
                    image=utils.addtext.generate_meme(img,top_text=top_text_strings,bottom_text=bottom_text_strings)
                elif template_name in ["stonks"]:
                    img = Image.open(MemeDir/"stonks.png")
                    image=utils.addtext.generate_meme(img,top_text=top_text_strings,bottom_text=bottom_text_strings)
                elif template_name in ["suprisedpikachu"]:
                    img = Image.open(MemeDir/"suprisedpikachu.jpg")
                    image=utils.addtext.generate_meme(img,top_text=top_text_strings,bottom_text=bottom_text_strings)
                    
                else:
                    await ctx.send("error")
                output_buffer = BytesIO()
                image.save(output_buffer, "png")  # or whatever format
                output_buffer.seek(0)
                await ctx.send(file=discord.File(fp=output_buffer, filename="Created-Meme-Yeet_Bot.png"))
    
    @memecreate.command(name="custom",aliases=['creatememe'], help=f'Create memes with a custom template \n\" Yeet memecreate custom \"  \n Alias: creatememe')
    async def custom(self,ctx):    
        
        top_text_strings=await self.top_text_function(ctx)
        bottom_text_strings=await self.bottom_text_function(ctx)
        if top_text_strings=="None":
            top_text_strings=""
        if bottom_text_strings=="None":
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
                
    @commands.cooldown(1, 12, commands.BucketType.user)
    @commands.command(name="MinecraftArt",aliases=['pixelate','mcart',"minecraftimage","mcimage"], help=f'Create Minecraft Art by attaching an image \n\" Yeet minecraftart <pixels on each side> <attachment> \" \n Alias: Pixelate, MCart, MinecraftImage, MCImage')
    async def mcimage(self,ctx,size:int=36):
        if len(ctx.message.attachments) == 0:
            img= await self.upload_function(ctx,"Minecraft Art Generator <a:YB_minecraft_mc_block:781419743110234132>")
            img=img[0]
            #gets discord.Asset
        else:
            img=ctx.message.attachments[0]
        asset = img
        bytes = await asset.read()
        async with ctx.typing():
            with Image.open(BytesIO(bytes)) as attachment:
                # Resize smoothly down to size x size pixels
                Final_Image = attachment.resize((size,size),resample=Image.BILINEAR)
                # Scale back up using NEAREST to original size
                Final_Image = Final_Image.resize(attachment.size,Image.NEAREST)
                output_buffer = BytesIO()
                Final_Image.save(output_buffer, "png")  # or whatever format
                output_buffer.seek(0)
            await ctx.send(file=discord.File(fp=output_buffer, filename="my_file.png"))
            
    @commands.cooldown(1, 12, commands.BucketType.user)
    @commands.command(name="Effect", help=f'Add filters to an image by attaching an image \n\" Yeet effect <effect name> <attachment> \" \n**Effects:**\n• Metal (Metallify an Image) \n• BlackAndWhite (Change an Image to Black and White) \n • Edges (Removes everything except edges)\n • Inverse (Changes all colours to their opposite ones)')
    async def effect(self,ctx,effect:str=None):
        choices = ["BLACKANDWHITE","B&W","METAL","EMBOSS","EDGES","EDGE","CONTOUR","INVERT","INVERSE"]
        
        async def effect_finding_function(ctx):
            question_embed=await ctx.send(embed=discord.Embed(title ="Effect Generator",description="Enter the effect name:\n**Effects:**\n• Metal (Metallify an Image) \n• BlackAndWhite (Change an Image to Black and White) \n • Edges (Removes everything except edges)\n • Inverse (Changes all colours to their opposite ones) ",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
            try:
                effect_to_do= await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel and m.content.upper() in choices))
            except asyncio.TimeoutError:
                await question_embed.edit(embed=discord.Embed(title ="Timeout Error",description="You took too much time, ya retarded monkey",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
            else: 
                return effect_to_do.content
        
        if effect==None:
            effect=await effect_finding_function(ctx)    
        
        if len(ctx.message.attachments) == 0:
            img=await self.upload_function(ctx,"Effect Editor")
            img=img[0]
            #gets discord.Asset
        else:
            img=ctx.message.attachments[0]
        asset = img
            #contour=Black and white
            #embos=Metallic
        effect=effect.upper()
        bytes = await asset.read()
        async with ctx.typing():
            with Image.open(BytesIO(bytes)) as attachment:
                if  effect in ["BLACKANDWHITE","B&W"]:
                    Final_Image = attachment.convert('1')
                    output_buffer = BytesIO()
                    Final_Image.save(output_buffer, "png")  # or whatever format
                    output_buffer.seek(0)
                    await ctx.send(file=discord.File(fp=output_buffer, filename="my_file.png"))
                elif  effect in ["METAL","EMBOSS"]:
                    Final_Image = attachment.filter(ImageFilter.EMBOSS)
                    output_buffer = BytesIO()
                    Final_Image.save(output_buffer, "png")  # or whatever format
                    output_buffer.seek(0)
                    await ctx.send(file=discord.File(fp=output_buffer, filename="my_file.png"))
                elif  effect in ["EDGES","EDGE","CONTOUR"]:
                    Final_Image = attachment.filter(ImageFilter.CONTOUR)
                    output_buffer = BytesIO()
                    Final_Image.save(output_buffer, "png")  # or whatever format
                    output_buffer.seek(0)
                    await ctx.send(file=discord.File(fp=output_buffer, filename="my_file.png"))
                elif  effect in ["INVERT","INVERSE"]:
                    Final_Image = attachment.convert('RGB')
                    Final_Image = ImageOps.invert(Final_Image)
                    output_buffer = BytesIO()
                    Final_Image.save(output_buffer, "png")  # or whatever format
                    output_buffer.seek(0)
                    await ctx.send(file=discord.File(fp=output_buffer, filename="my_file.png"))

                else:
                    embed=discord.Embed(title="<:warn:779698024212463637> | Error ",description="That's not even a effect, ya thicc headed giraffe.",color = random.choice(colourlist))
                    #embed.add_field(name="Effects",value="Error", inline=False)
                    embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                    await ctx.send(embed=embed)
    
    @commands.cooldown(1, 12, commands.BucketType.user)
    @commands.group(name="asciiart",aliases=['digital','ascii'],invoke_without_command=True, help=f'Create ASCII art with your avatar or upload an image and convert it into ASCII Art \n\" Yeet asciiart  \" or \"Yeet asciiart custom \" for converting uploaded images \n Alias: Digital,Ascii')
    async def ascii(self,ctx,member:discord.Member=None):
        member = member or ctx.author 
        asset = member.avatar_url_as(static_format="png")
        colours_list=await self.ascii_colour_finding_function(ctx)
        bytes = await asset.read()
        async with ctx.typing():
            with Image.open(BytesIO(bytes)) as my_image:   
                Final_Image=utils.image_effects.asciiart(my_image,SC = 0.40,GCF= 1.5, color1=colours_list[0], color2=colours_list[1], bgcolor=colours_list[2])
            output_buffer = BytesIO()
            Final_Image.save(output_buffer, "png")  # or whatever format
            output_buffer.seek(0)
        await ctx.send(file=discord.File(fp=output_buffer, filename="ascii_art.png"))       
    
    @ascii.command(name="image",aliases=['upload','custom'])
    async def ascii_upload(self,ctx):
        
        if len(ctx.message.attachments) == 0:
            img=await self.upload_function(ctx,"ASCII Art Generator")
            img=img[0]
            #gets discord.Asset
        else:
            img=ctx.message.attachments[0]
        asset = img
        bytes = await asset.read()
        colours_list=await self.ascii_colour_finding_function(ctx)
        async with ctx.typing():
            with Image.open(BytesIO(bytes)) as my_image:   
                Final_Image=utils.image_effects.asciiart(my_image,SC = 0.40,GCF= 1.5, color1=colours_list[0], color2=colours_list[1], bgcolor=colours_list[2])
            output_buffer = BytesIO()
            Final_Image.save(output_buffer, "png")  # or whatever format
            output_buffer.seek(0)
        await ctx.send(file=discord.File(fp=output_buffer, filename="ascii_art.png")) 
            
    async def ascii_colour_finding_function(self,ctx):
        question_embed=await ctx.send(embed=discord.Embed(title ="ASCII Art Generator",description="**Enter the colour's names:**\n**Format:**\n<top-text-colour> / <bottom-text-colour> / <background-colour>\n**Examples:**\n • DarkTurquoise/ LawnGreen/ White\n • #00CED1/ #7CFC00/ #FFFFFF\nYou can type any random text if you want the text to generate in it's default colours.\nEntering any incorrect colour names would generate the art in the default colours *(Green, Green, Black)*. \n[Click Me for Colour Codes](https://htmlcolorcodes.com/)",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        try:
            colours= await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            await question_embed.edit(embed=discord.Embed(title ="Timeout Error",description="You took too much time, ya retarded monkey",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        else: 
            colours_list=colours.content.replace(" ", "")
            colours_list=colours_list.split("/")
            if len(colours_list)>3:
                #print("too many arguments")
                colours_list=["green","green","black"]
            elif len(colours_list)<3:
                #print("too less arguments")
                colours_list=["green","green","black"]
            else:    
                for clr in colours_list:
                    if clr=="":
                        if colours_list.index(clr) == 2:
                            colours_list[colours_list.index(clr)]="black"
                        elif colours_list.index(clr) == 1 or colours_list.index(clr) == 0:
                            colours_list[colours_list.index(clr)]="green"
                    else:
                        try:
                            colour.Color(str(clr))
                        except:
                            if colours_list.index(clr) == 2:
                                colours_list[colours_list.index(clr)]="black"
                            elif colours_list.index(clr) == 1 or colours_list.index(clr) == 0:
                                colours_list[colours_list.index(clr)]="green"

        return colours_list

    
    @commands.cooldown(1, 12, commands.BucketType.user)
    @commands.command(name="Hacker",aliases=['hackerman'], help=f'sends the Hackerman meme with your avatar. \n\"Yeet hacker @Yeet Bot \" \n Alias: Hackerman')
    async def hackerman(self,ctx,member:discord.Member=None):
        member = member or ctx.author
        async with ctx.typing():
            #gets discord.Asset
            Hacker_template = Image.open(MediaDir / "hackerman.png")
            asset = member.avatar_url_as(static_format="png")
            #Converts it into bytes
            bytes = await asset.read()
            #converts it into a PIL Image object
            with Image.open(BytesIO(bytes)) as my_image:
                # open the pic and give it an alpha channel so it's transparent
                my_image= my_image.resize((220, 220)).convert('RGBA')
                my_image= my_image.rotate(352,Image.NEAREST, expand = 1, fillcolor=None)
                Final_Image = Hacker_template.copy()
                # note the second appearance of my_image, that's necessary to paste without a bg
                Final_Image.paste(my_image,(250, 20),my_image)

            #Final_Image.show()
            Final_Image.save('Final_Image_Hackerman.png')
            embed = embed=discord.Embed(title = f"Hackerman!", color =0x660099, timestamp=ctx.message.created_at)
            embed.set_image(url="attachment://Final_Image_Hackerman.png")
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(file=discord.File('Final_Image_Hackerman.png'),embed=embed)
            os.remove("Final_Image_Hackerman.png")

    @commands.cooldown(1, 12, commands.BucketType.user)
    @commands.command(name="Shit", help=f'Creates a Shit Meme with your avatar. \n\"Yeet Shit @Yeet Bot \"')
    async def stepped_on_shit(self,ctx,member:discord.User=None):
        owner=await self.bot.fetch_user(571957935270395925)
        if (member == owner or member == self.bot.user):
            embed = embed=discord.Embed(title = f"lol as if he is Shit :poop: .",description=" You are the only one who is shit here.", color =0x660099)
        else:
            embed = embed=discord.Embed(title = f"Ew! What's this Shit! :poop: ", color =0x660099)
            member = member or ctx.author
        async with ctx.typing():
            Shit_template = Image.open(MediaDir / "steppedinshit.jpg")
           #gets discord.Asset
            asset = member.avatar_url_as(static_format="png")
            #Converts it into bytes
            bytes = await asset.read()
            #converts it into a PIL Image object
            with Image.open(BytesIO(bytes)) as my_image:
                # open the pic and give it an alpha channel so it's transparent
                my_image= my_image.resize((180,180)).convert("RGBA")
                Final_Image = Shit_template.copy()
                # note the second appearance of my_image, that's necessary to paste without a bg
                Final_Image.paste(my_image,(200,590))

            #Final_Image.show()
            Final_Image.save('Final_Image_Shit.png')
            
            embed.set_image(url="attachment://Final_Image_Shit.png")
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(file=discord.File('Final_Image_Shit.png'),embed=embed)
            os.remove("Final_Image_Shit.png")

    @commands.cooldown(1, 12, commands.BucketType.user)
    @commands.command(name="Wanted", help=f'Creates a Wanted Poster with your avatar. \n\"Yeet Wanted @Yeet Bot \"')
    async def wanted(self,ctx,member:discord.User=None):
        member = member or ctx.author
        async with ctx.typing():
            #gets discord.Asset
            Wanted_template = Image.open(MediaDir / "wanted.png")
            asset = member.avatar_url_as(static_format="png")
            #Converts it into bytes
            bytes = await asset.read()
            #converts it into a PIL Image object
            with Image.open(BytesIO(bytes)) as my_image:
                # open the pic and give it an alpha channel so it's transparent
                my_image= my_image.resize((255, 255)).convert("RGBA")
                Final_Image = Wanted_template.copy()
                # note the second appearance of my_image, that's necessary to paste without a bg
                Final_Image.paste(my_image,(98,165))

            #Final_Image.show()
            Final_Image.save('Final_Image_Wanted.png')
            embed = embed=discord.Embed(title = f"{member.name} Wanted", color =0x660099)
            embed.set_image(url="attachment://Final_Image_Wanted.png")
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(file=discord.File('Final_Image_Wanted.png'),embed=embed)
            os.remove("Final_Image_Wanted.png")
    
    '''@commands.cooldown(1, 12, commands.BucketType.user)
    @commands.command(name="Gay",aliases=['gei'], help=f'Creates the \" Why are you gay? \" meme with your avatar. \n\"Yeet Shit @Yeet Bot \"')
    async def why_are_you_gei(self,ctx,member:discord.User=None):
        owner=await self.bot.fetch_user(571957935270395925)
        if member == None:
            embed = embed=discord.Embed(title = f"Asking yourself?", color =0x660099,url="https://youtu.be/bk_O3m_Agjg")
            member = ctx.author

        elif (member == owner  or member==self.bot.user):
            embed = embed=discord.Embed(title = f"Sorry, I can't lie..", color =0x660099,url="https://youtu.be/bk_O3m_Agjg")
            member=ctx.author

        else:
            embed = embed=discord.Embed(title = f"Why are you gay?", color =0x660099,url="https://youtu.be/bk_O3m_Agjg")
            member = member 

        async with ctx.typing():
            Gei_template = Image.open(MediaDir / "whyareyougay.jpg")
            #gets discord.Asset
            asset_1 = ctx.author.avatar_url
            asset_2 = member.avatar_url
            

            #Converts it into bytes
            bytes1 = await asset_1.read()
            #converts it into a PIL Image object
            with Image.open(BytesIO(bytes1)) as user_avatar_image:
                user_avatar_image= user_avatar_image.resize((220,220)).convert("RGBA")
                Final_Image = Gei_template.copy()
                Final_Image.paste(user_avatar_image,(710,50))
            
            
            bytes2 = await asset_2.read()
            with Image.open(BytesIO(bytes2)) as user_mentioned_avatar_image:
                user_mentioned_avatar_image= user_mentioned_avatar_image.resize((220,220)).convert("RGBA")
                Final_Image.paste(user_mentioned_avatar_image,(35,70))

            #Final_Image.show()
            Final_Image.save('Final_Image_Gei.jpg')
            embed.set_image(url="attachment://Final_Image_Gei.jpg")
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(file=discord.File('Final_Image_Gei.jpg'),embed=embed)
            os.remove("Final_Image_Gei.jpg")'''


    async def upload_function(self,ctx,name):
        question_embed=await ctx.send(embed=discord.Embed(title =f"{name}",description="**Upload the image:**\nPlease upload a static image in png/jpg for best results.",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        try:
            image_message= await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            await question_embed.edit(embed=discord.Embed(title ="Timeout Error",description="You took too much time, ya retarded monkey",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        else:
            if len(image_message.attachments) > 1:
                embed=discord.Embed(title="<:warn:779698024212463637> | Multiple Attachments ",description="Attach one attachment, ya braindead zombie! ",color = random.choice(colourlist))
                embed.add_field(name="Something went wrong. Try again later",value=f"You attached {len(ctx.message.attachments)} attachments. Only attach one ", inline=False)
                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed)

            elif len(image_message.attachments) == 1:
                return image_message.attachments
                
            else:
                embed=discord.Embed(title="<:warn:779698024212463637> | No Attachments ",description="Boi, you don't have any attachment. ",color = random.choice(colourlist))
                embed.add_field(name="lol u dumb",value="Where required attachment ya retard? Try Again and attach a image this time, genius", inline=False)
                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed) 
                return await self.upload_function(ctx,name)

    async def top_text_function(self,ctx):
        question_embed=await ctx.send(embed=discord.Embed(title ="Meme Creator",description="Enter the top text: (50 Characters Max)\n Type \"None\" to keep it blank.",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        try:
            top_text= await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            await question_embed.edit(embed=discord.Embed(title ="Timeout Error",description="You took too much time, ya retarded monkey",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        else: 
            if len(top_text.content)> 50:
                embed=discord.Embed(title="<:warn:779698024212463637> | Too many Characters ",description="How many letters will you type, you retard?",color = random.choice(colourlist))
                embed.add_field(name="Type only 50 characters in your sentence.",value=f"You typed {len(top_text.content)} letters, dumbshit! Type the top text again.", inline=False)
                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed)
                return await self.top_text_function(ctx)
            else:
                return top_text.content

    async def bottom_text_function(self,ctx):
        question_embed=await ctx.send(embed=discord.Embed(title ="Meme Creator",description="Enter the bottom text: (50 Characters Max)\n Type \"None\" to keep it blank.",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        try:
            bottom_text= await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
        except asyncio.TimeoutError:
            await question_embed.edit(embed=discord.Embed(title ="Timeout Error",description="You took too much time, ya retarded monkey",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
        else: 
            if len(bottom_text.content)> 50:
                embed=discord.Embed(title="<:warn:779698024212463637> | Too many Characters ",description="How many letters will you type, you retard?",color = random.choice(colourlist))
                embed.add_field(name="Type only 50 characters in your sentence.",value=f"You typed {len(bottom_text.content)} letters, dumbshit! Type the bottom text again.", inline=False)
                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ") 
                await ctx.send(embed=embed)
                return await self.bottom_text_function(ctx)
            else:
                return bottom_text.content
   

def setup(bot):
    bot.add_cog(Image_Functions(bot))