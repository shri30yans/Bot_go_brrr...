import os, sys, discord, platform, random, aiohttp, json,time,asyncio,requests
from discord.ext import commands,tasks,menus
from utils.lists import roasts_list
from discord.ext.commands import Greedy
from discord.ext.commands.cooldowns import BucketType
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config




colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
            0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]


class Fun(commands.Cog,name="Fun"):
    def __init__(self, bot):
        self.bot = bot
        self.config=config

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Blob", help="Blobs up the previous message by default\n\"Yeet Blob <Message-Id or link>\"")
    async def blob(self,ctx,msg_id:discord.Message=None):
        if msg_id==None:
            message_to_blob_up=await ctx.channel.history(limit=2).flatten()
            message_to_blob_up=message_to_blob_up[1]
        else:
            message_to_blob_up=msg_id

        for emoji in ("<a:blob_chain:774144015012200478>", "<a:blob_crazy:774144015456665620>","<a:blob_dance:774144054485188640>","<a:blob_mad:774144031734890536>","<a:blob_party_mega:774144017427595266>","<a:blob_rainbow:774144018338545684>"):
            await message_to_blob_up.add_reaction(emoji)
    
    '''@commands.cooldown(1, 3, commands.BucketType.user)
    @commands.group(name="React",aliases=['r'],invoke_without_command=True,case_insensitive = True, help='sends a particular reaction \n Yeet react <reaction-name> <msg-id> \n  ')
    async def reaction(self,ctx,*emojis_keyword_tuple):
        async def reaction_send(self,ctx,*emojis_keyword_tuple):
            emojis_keyword_list=list(emojis_keyword_tuple)
            nsfw_keywords_list=["boob","boobs","fuck","nude","tit","pp","sex","cum",]
            if any(ele in emojis_keyword_list for ele in nsfw_keywords_list) and not ctx.channel.is_nsfw():
                embed = discord.Embed(title ="NSFW Emoji",description=f"The requested keywords: {str(emojis_keyword_list)[1:-1]}  may bring up a NSFW emote. Please use this in a NSFW channel.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
                author_avatar=ctx.author.avatar_url
                embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed)
            else:
                #https://www.geeksforgeeks.org/python-test-if-all-elements-are-present-in-list/ 
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
                    message_id = discord.Embed(title ="Message",description=f"Enter the message ID or link to react to.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
                    author_avatar=ctx.author.avatar_url
                    message_id.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                    message_id_msg=await ctx.send(embed=message_id)

                    def check(message: discord.Message): 
                        return message.author == ctx.author 
                    try:
                        message_to_react = await self.bot.wait_for('message', timeout = 30, check = check)

                    except asyncio.TimeoutError: 
                        await message_id_msg.edit(embed=discord.Embed(title ="Message",description=f"Command Timed out. No message was entered. ",color = random.choice(colourlist),timestamp=ctx.message.created_at))            

                    # This will be executed if the author responded properly
                    else: 
                        emoji= random.choice(selected_emojis_list)
                        await message_to_react.add_reaction(emoji)


    
        #await message_to_react.add_reaction(random.choice(selected_emojis_list))'''
    

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="rSend",aliases=['s'], help='sends a particular reaction \n\"Yeet react <reaction-name>\" \n Aliases:s')
    async def reaction_send(self,ctx,*emojis_keyword_tuple):
        emojis_keyword_list=list(emojis_keyword_tuple)
        nsfw_keywords_list=["boob","boobs","fuck","nude","tit","pp","sex","cum","NSFW"]
        if any(ele in emojis_keyword_list for ele in nsfw_keywords_list) and not ctx.channel.is_nsfw():
            embed = discord.Embed(title ="NSFW Emoji",description=f"The requested keywords: {str(emojis_keyword_list)[1:-1]}  may bring up a NSFW emote. Please use this in a NSFW channel.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(embed=embed)
        else:
            #https://www.geeksforgeeks.org/python-test-if-all-elements-are-present-in-list/ 
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
                emoji= random.choice(selected_emojis_list)
                await ctx.send(emoji)

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="rSearch", help="sends a particular reaction \n\"Yeet react reaction-name\"")
    async def reaction_search(self,ctx,*emojis_keyword_tuple):
        emojis_keyword_list=list(emojis_keyword_tuple)
        nsfw_keywords_list=["boob","boobs","fuck","nude","tit","sex","cum","nipple","tease","licking","lick","nsfw","nsfw_sex","_sex","nsfw_"]
        if any(ele in emojis_keyword_list for ele in nsfw_keywords_list) and not ctx.channel.is_nsfw():
            embed = discord.Embed(title ="NSFW Emoji",description=f"The requested keywords: {str(emojis_keyword_list)[1:-1]}  may bring up a NSFW emote. Please use this in a NSFW channel.",color = random.choice(colourlist),timestamp=ctx.message.created_at)
            author_avatar=ctx.author.avatar_url
            embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(embed=embed)
        else:
            #https://www.geeksforgeeks.org/python-test-if-all-elements-are-present-in-list/ 
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
                    if length<1000:
                        emoji_string=emoji_string + str(elem) +"    |    " + str(elem.name) + " \n"
                        
                    else:
                        Emoji_list_seperated.append(emoji_string)
                        emoji_string=str(elem) +"    |    " + str(elem.name) + " \n"
                        length=0
                Emoji_list_seperated.append(emoji_string)
                    
                if len(Emoji_list_seperated)>1:
                    embeds_list = []
                    for embed_string in Emoji_list_seperated:
                        embed_string_index=Emoji_list_seperated.index(embed_string)
                        embeds_list.append(discord.Embed(title =f"{len(selected_emojis_list)} Emoji's found!",description=f"The requested keywords: {str(emojis_keyword_list)[1:-1]}  have the {len(selected_emojis_list)} results:",color = random.choice(colourlist),timestamp=ctx.message.created_at).add_field(name="Search results:",value=f"{embed_string}\n").set_footer(icon_url= ctx.author.avatar_url,text=f" Page: {embed_string_index+1} of {len(Emoji_list_seperated)+1} • Requested by {ctx.message.author} • Yeet Bot "))
                    menu = menus.MenuPages(EmbedPageSource(embeds_list, per_page=1))
                    await menu.start(ctx)
                else:
                    embed = discord.Embed(title =f"{len(selected_emojis_list)} Emoji's found!",description=f"The requested keywords: {str(emojis_keyword_list)[1:-1]}  have the {len(selected_emojis_list)} results:",color = random.choice(colourlist),timestamp=ctx.message.created_at)
                    embed.add_field(name="Search results:",value=f"{Emoji_list_seperated[0]}")
                    author_avatar=ctx.author.avatar_url
                    embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                    await ctx.send(embed=embed)
                    


    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Gamer", help='find out how much of a epic gamer you are. \n\"Yeet gamer\" OR \"Yeet gamer @\"')
    async def gamer_rate(self,ctx,user:discord.Member=None):
        if (user == None):
            user_mention= ctx.author
        else:
            user_mention=user
        embed = discord.Embed(title = "Epic Gamer Rate", color =random.choice(colourlist),timestamp=ctx.message.created_at)
        if user_mention.id== 571957935270395925:#me
            epic_gamer_percent=str(100)
            response= user_mention.mention + " is " + epic_gamer_percent +"%" +" epic gamer! <a:confetti:775389522875121664><:pepe_ez:775303209739616267><a:confetti:775389522875121664>"
        elif user_mention.id== 682899218695847974:#tahir
            epic_gamer_percent=str(0)
            response= user_mention.mention + " is " + epic_gamer_percent +"%" +" epic gamer! <:Reaction_you_noob:775389521700585502> <a:pepe_cry:775303212059590676>"
        else:
            epic_gamer_percent= str(random.randint(1,101))
            response= user_mention.mention + " is " + epic_gamer_percent +"%" +" epic gamer!"
        epic_gamer_percent=int(epic_gamer_percent)
        epic_emoji="<:text_epic:775303209417834506>" * (epic_gamer_percent // 10)
        embed.add_field(name="Epic gamer percent:",value=f"{response} \n {epic_emoji} ")
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        
        await ctx.send(embed=embed)
    
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(name="Insult", help="Insults a particular user \n\"Yeet insult\" OR \"Yeet insult @User\"")
    async def insult(self,ctx,user:discord.Member=None):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://insult.mattbas.org/api/insult') as resp:
                insult_text=str(await resp.text())
                embed = discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
                
                if (user == None):
                    response=insult_text + "."
                    embed.add_field(name="Insult",value=response)
                elif(user.id== 571957935270395925):#Me
                    response= ctx.author.mention + " " + insult_text + "."
                    embed.add_field(name="How dare you insut him!",value=f"Face the wraith of the Gods:\n {response} ")
                else:
                    response= user.mention + " " + insult_text + "."
                    embed.add_field(name="Insult",value=response)
                    
                author_avatar=ctx.author.avatar_url
                embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(name="Roast", help="roasts a particular user \n\"Yeet roast\" OR \"Yeet roast @User\"")
    async def roast(self,ctx,user:discord.Member=None):
        embed = discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
        roast=random.choice(roasts_list)
        
        if (user == None):
            response=roast
            embed.add_field(name="Roast",value=response)
        elif(user.id== 571957935270395925):#Me
            response= ctx.author.mention + " " + roast
            embed.add_field(name="How dare you insult him!",value=f"Face the wraith of the Gods:\n {response} ")
        else:
            response= user.mention + " " +roast
            embed.add_field(name="Roast",value=response)
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Say",aliases=['repeat','speak'], help="Yeet Bot repeats after you \n\"Yeet say \"Yeet\" \" \n Alias: repeat,speak ")
    async def say(self,ctx,*arguments):
        response =  ' '.join(arguments) 
        try:
            await ctx.message.delete()
        except:
            except_embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
            except_embed.add_field(name="No Permissions",value="This command works better if I have the Manage Messages permission.\n Please contact your Administrators.\n To learn more about this command type \"yeet help say\"") 
            author_avatar=ctx.author.avatar_url
            except_embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
            await ctx.send(embed=except_embed,delete_after=10) 

        finally:
            await ctx.send(response)
        
    
    '''@commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Snipe", help='Embeds the last deleted message \n +snipe')  
    async def snipe(self,ctx, *, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        try:
            msg = bot.snipes[channel.id]
        except KeyError:
            return await ctx.send(embed=discord.Embed(description='Nothing to snipe!'))
        # one liner, dont complain
        await ctx.send(embed=discord.Embed(description=msg.content, color=msg.author.color).set_author(name=str(msg.author), icon_url=str(msg.author.avatar_url)))'''

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Dice",aliases=['roll','die'], help="Rolls a dice.(Default: 6 sided die) \n\" Yeet die <Number of sides>\" \n Aliases:die,roll")
    async def dice(self,ctx,number:int=6):
        choice=random.randint(1,number)
        embed = discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
        embed.add_field(name=":game_die: Dice Roll :game_die:",value=f"I rolled a Die with {number} faces and I got {choice}. ")
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)
    
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="Coin",aliases=['toss','flip'], help="Flips a coin. \n\"Yeet coin\" \n Aliases:toss,flip")
    async def coin(self,ctx):
        choice=random.choice(["Heads","Tails"])
        embed = discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
        embed.add_field(name=":coin: Coin Toss :coin:",value=f" I flipped a coin and got {choice}. ")
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)

    @commands.cooldown(1,10,commands.BucketType.user)  
    @commands.command(name="Rhyme", help='Finds rhyming words \n\" Yeet rhyme Yeet\"')
    async def rhyme(self,ctx,word:str):
        MessageToSend=""
        parameter={"rel_rhy":word}
        request = requests.get("https://api.datamuse.com/words",parameter)

        rhyme_json= request.json()
        for i in rhyme_json[0:3]:
            RhymeWordFetcher=(i['word'])
            MessageToSend=MessageToSend+ "  "+RhymeWordFetcher
        embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
        embed.add_field(name="Rhyme :musical_note: ", value=MessageToSend) 
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")   
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))

class EmbedPageSource(menus.ListPageSource):
    async def format_page(self, menu, embed):
        return embed

