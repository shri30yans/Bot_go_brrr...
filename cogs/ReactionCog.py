import discord,random,json,asyncio
from discord.abc import User
from discord.ext import commands,tasks
import utils.awards as awards
import config 

colourlist=config.embed_colours


#This cog listens for the addition and removal of reactions
#Reactions that are regestered here: Star, Upvotes and Downvotes, Awards
    
class ReactionCog(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        self.messages_count_dict={}

    

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def upvote_downvote_reaction_add(self,payload):  
        await self.bot.wait_until_ready() 
        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        ImportantFunctions = self.bot.get_cog('ImportantFunctions') 
        channel = self.bot.get_channel(payload.channel_id) 
        user = self.bot.get_user(payload.user_id)
        message = await channel.fetch_message(payload.message_id)
        emoji=payload.emoji 

        if str(emoji) in config.award_reaction_menu_emoji:
            #await message.remove_reaction(emoji,user)
            
            class CustomContext:
                def __init__(self,channel,author):
                    self.channel = channel
                    self.author = author

            cmd = self.bot.get_command("Award")
            await cmd(ctx = CustomContext(channel = channel,author = user),message=message)
            return
        
        
        if channel.guild.id in config.APPROVED_SERVERS:#if that server is approved/that server has the settings
            if user.bot:
                return 
            
            await self.check_if_message_is_poll(message=message,emoji=emoji,user=user,type_of_event="reaction_add")


            score = await ImportantFunctions.score_calculator(message=message)

            
            #=============================================
            #Upvote/Downvote
            #=============================================
            
            #Upvote add Karma
            if str(emoji) == config.upvote_reaction and message.author != user:
                amt = random.randint(0,2)
                await UserDatabaseFunctions.add_karma(user=message.author,amt=amt)
            
            #Downvote remove Karma
            elif str(emoji) == config.downvote_reaction and message.author != user:
                amt = random.randint(-3,-1)
                await UserDatabaseFunctions.add_karma(user=message.author,amt=amt)

            
            #if any post crosses a certain limit of upvotes, award that posts author 100 credits
            if str(emoji) == config.upvote_reaction and message.channel.id == config.meme_channel_id :  
                #score_needed_to_pin = (await ImportantFunctions.get_server_settings(channel.guild.id))["meme_score_required_to_pin"]
                score_needed_to_pin =config.meme_score_needed_to_pin

                if score >= score_needed_to_pin:
                    await self.send_to_dank_memes_channel(message)
                    amt=100
                    await UserDatabaseFunctions.add_credits(user=message.author,amt=amt)
    

    @commands.Cog.listener(name="on_raw_reaction_remove")
    async def upvote_downvote_reaction_remove(self,payload):  
        await self.bot.wait_until_ready() 
        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        ImportantFunctions = self.bot.get_cog('ImportantFunctions') 
        channel=self.bot.get_channel(payload.channel_id) 
        user=self.bot.get_user(payload.user_id)
        message= await channel.fetch_message(payload.message_id)
        emoji=payload.emoji  
        
        if channel.guild.id in config.APPROVED_SERVERS:#if that server is approved/that server has the settings
            if user.bot:
                return
            
            await self.check_if_message_is_poll(message=message,emoji=emoji,user=user,type_of_event="reaction_remove")

            score = await ImportantFunctions.score_calculator(message=message)

            #score_needed_to_pin = (await ImportantFunctions.get_server_settings(channel.guild.id))["meme_score_required_to_pin"]
            score_needed_to_pin = config.meme_score_needed_to_pin

            
            #if any post has 10 or more upvotes, award that posts author 100 credits    
            if str(emoji) == config.upvote_reaction and score <= score_needed_to_pin  and message.channel.id == config.meme_channel_id :
                amt=-100
                await UserDatabaseFunctions.add_credits(user=message.author,amt=amt)
            
            #Removed Upvote remove Karma
            elif str(emoji) == config.upvote_reaction and message.author != user:
                amt = random.randint(-3,-1)
                await UserDatabaseFunctions.add_karma(user=message.author,amt=amt)
            
            #Removed Downvote add Karma
            if str(emoji) == config.downvote_reaction and message.author != user:
                amt = random.randint(0,2)
                await UserDatabaseFunctions.add_karma(user=message.author,amt=amt)


    async def send_to_dank_memes_channel(self,message):
        async def send_message():
            embed=discord.Embed(color = meme_channel.guild.me.colour,timestamp=message.created_at,description=message.content)
            embed.set_author(name=message.author.name, icon_url= f"{message.author.avatar_url}")
            embed.add_field(name="Source:", value=f"[Jump]({message.jump_url})", inline=False)
            if len(message.attachments): #basically if len !=0 or if attachments are there
                embed.set_image(url=message.attachments[0].url)
            embed.set_footer(text=f"{message.id}")
            await dank_memes_channel.send(embed=embed)
        
        meme_channel=self.bot.get_channel(config.meme_channel_id)
        dank_memes_channel=self.bot.get_channel(config.dank_meme_channel_id)
        messages = await dank_memes_channel.history(limit=20).flatten() 

        for x in messages:
            try:
                footer=x.embeds[0].footer
                if str(message.id) in str(footer):
                    return
            except:
                pass
        else:
            await send_message()
        
        #Listeners
   
    
    @commands.Cog.listener(name="on_message")
    async def automatic_reactions(self,message):
        await self.bot.wait_until_ready() 
        if message.author == self.bot.user:
            return

        elif message.channel.id==config.suggestions_channel_id:
            if message.content.startswith("//"):
                return
            else:
                await message.add_reaction(config.upvote_reaction)
                await message.add_reaction(config.downvote_reaction)

        elif message.channel.id==config.meme_channel_id and len(message.attachments) !=0:
            await message.add_reaction(config.upvote_reaction)
            await message.add_reaction(config.downvote_reaction)

    #For adding credits for chatting in #main_chat
    @commands.Cog.listener(name="on_message")
    async def add_credits_for_sending_messages(self,message):
        await self.bot.wait_until_ready() 
        if message.guild is not None:
                #if it is a guild
            if message.guild.id in config.APPROVED_SERVERS:
                        #if that server is approved/that server has the settings
                user=message.author
                if user.bot:
                    return
                if message.channel.id != config.main_chat_id:
                    return
                messages = await message.channel.history(limit=5).flatten() 
                #if previous message is also written by same person
                count=0
                for msg in messages:
                    if msg.author == message.author:
                        count += 1
                if count >= 3:
                    return

                else:    
                    if str(user.id) in self.messages_count_dict:
                        if self.messages_count_dict[str(user.id)] >= 5:
                            self.messages_count_dict[str(user.id)] = 0 #reset messages
                            #Add credits
                            UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
                            amt=5
                            await UserDatabaseFunctions.add_credits(user=user,amt=amt)
                        
                        else:
                            self.messages_count_dict[str(user.id)] += 1
                        
                    else:
                        self.messages_count_dict[str(user.id)] = 1
                
    
    async def check_if_message_is_poll(self,message,emoji,user,type_of_event):    
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                server_info = await connection.fetchrow("SELECT * FROM server_info WHERE id=$1",message.guild.id)
                ongoing_polls=json.loads(server_info["ongoing_polls"])
                ongoing_polls_list=ongoing_polls["polls"]
                
                if message.id in ongoing_polls_list:#if the message_id is in ongoing_polls
                    UtilityCog = self.bot.get_cog('Utility')
                    await UtilityCog.update_poll(PollMessage=message,emoji=emoji,user=user,type_of_event=type_of_event)

    
    
            


def setup(bot):
    bot.add_cog(ReactionCog(bot))