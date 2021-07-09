import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config 

awards_list=[awards.Rocket_Dislike,awards.Rocket_Like,awards.Wholesome_Award,awards.Silver_Award,awards.Gold_Award,awards.Platinum_Award,awards.Argentinum_Award,awards.Ternion_Award]
colourlist=config.embed_colours


#This cog listens for the addition and removal of reactions
#Reactions that are regestered here: Star, Upvotes and Downvotes, Awards
    
class ReactionCog(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    async def check_if_message_is_poll(self,message,emoji,user,type_of_event):    
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                server_info = await connection.fetchrow("SELECT * FROM server_info WHERE id=$1",message.guild.id)
                ongoing_polls=json.loads(server_info["ongoing_polls"])
                ongoing_polls_list=ongoing_polls["polls"]
                
                if message.id in ongoing_polls_list:#if the message_id is in ongoing_polls
                    UtilityCog = self.bot.get_cog('Utility')
                    await UtilityCog.update_poll(PollMessage=message,emoji=emoji,user=user,type_of_event=type_of_event)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):  
        
        ImportantFunctions = self.bot.get_cog('ImportantFunctions') 
        channel = self.bot.get_channel(payload.channel_id) 
        user = self.bot.get_user(payload.user_id)
        message = await channel.fetch_message(payload.message_id)
        emoji=payload.emoji 
        if channel.guild.id in config.APPROVED_SERVERS:#if that server is approved/that server has the settings
            if user.bot:
                return 
            
            type_of_event="reaction_add"
            await self.check_if_message_is_poll(message=message,emoji=emoji,user=user,type_of_event=type_of_event)


            reaction_count = await ImportantFunctions.get_reaction_count(message=message,emoji=emoji)
            score = await ImportantFunctions.score_calculator(message=message)

            #Upvote add Karma
            if str(emoji) == config.upvote_reaction and message.author != user:
                amt = random.randint(0,2)
                await ImportantFunctions.add_karma(user=message.author,amt=amt)
                await ImportantFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="upvote",num=1)
            #Downvote remove Karma
            
            elif str(emoji) == config.downvote_reaction and message.author != user:
                amt = random.randint(-3,-1)
                await ImportantFunctions.add_karma(user=message.author,amt=amt)
                await ImportantFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="downvote",num=1)

            
            #if any post has 10 or more upvotes, award that posts author 100 credits
            if str(emoji) == config.upvote_reaction and message.channel.id == config.meme_channel_id :  
                score_needed_to_pin = (await ImportantFunctions.get_settings(channel.guild.id))["meme_score_required_to_pin"]
                
                if score >= score_needed_to_pin:
                    await message.pin(reason="Got upvoted.")
                    amt=100
                    await ImportantFunctions.add_credits(user=message.author,amt=amt)
            
            #starboard
            if str(emoji) == "⭐":
                # if message.author == user: #self star
                #     return
                # else:
                # update the reactions sent in database
                await ImportantFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="star",num=1)
                await ImportantFunctions.post_to_starboard(message=message,channel=channel,user=user,emoji=emoji,reaction_name="star")

            
            #awards
            for award in awards_list:
                if str(emoji) == award.reaction_id:
                    async with self.bot.pool.acquire() as connection:
                        async with connection.transaction():
                            await ImportantFunctions.create_account(user)
                            user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                            user_account=dict(user_account)
                            if user_account["credits"] < award.cost:
                                await message.remove_reaction(emoji, user)
                                await message.channel.send(f"{user.mention} You don't have enough credits to buy this {award.name} award. Try earning some credits first.",delete_after=5)
                            
                            else:
                                if user == message.author:
                                    await message.remove_reaction(emoji, user)
                                    await channel.send(f"{user.mention} Awarding yourself? You seriously aren't that desperate, are you?",delete_after=5)
                                    return
                                elif message.author.bot:
                                    await message.remove_reaction(emoji, user)
                                    await channel.send(f"{user.mention} Awarding bots? Sorry no can do.")
                                    return
                                else:

                                    embed = discord.Embed(title=f"{user.name}, Give {award.name} award to {message.author.name}?",description="React with ✅ to give the award and ❌ to ncancel.",color = 0xFFD700)
                                    embed.add_field(name="Note:",value="An award cannot be revoked, once given. The reaction can be removed, but that would not remove the award. \nThis action is irreversible. \nCredits cannot be refunded.")
                                    embed.set_thumbnail(url=str(emoji.url))
                                    embed.set_footer(icon_url= user.avatar_url,text=f"Requested by {user.name} • {self.bot.user.name} ")
                                    check_message=await message.channel.send(embed=embed)
                                    await check_message.add_reaction('✅')
                                    await check_message.add_reaction('❌')
                                    
                                    def check_accept_or_reject(confirm_reaction,confirm_user):
                                        return str(confirm_reaction.emoji) in ['✅', '❌'] and user == confirm_user

                                    try:
                                        confirm_reaction,confirm_user = await self.bot.wait_for('reaction_add',check=check_accept_or_reject, timeout=60)#pylint: disable=unused-argument 
                                        #disables the confirm_user unusesd argument error

                                    except asyncio.TimeoutError:
                                        await check_message.delete()
                                        #await check_message.edit(embed=discord.Embed(title="Timeout!",description=f"{user.mention}, did not react after 60 seconds. Award is cancelled.",color = 0xFFD700))

                                    else:
                                        if str(confirm_reaction.emoji) == '✅':
                                            await check_message.delete()
                                            #await message.channel.send(f"{user.mention} gave {message.author.mention} a {award.name} award.")
                                            embed = discord.Embed(title=f"{message.author.name} received a {award.name} Award!",description=f"{user.mention} liked {message.author.mention}'s [post]({message.jump_url}) so much that they gave it the {award.name} award.",color = 0xFFD700)
                                            embed.set_thumbnail(url=str(emoji.url))
                                            embed.set_footer(icon_url= user.avatar_url,text=f"Given by {user.name} • {self.bot.user.name} ")
                                            await channel.send(embed=embed)
                                            
                                            embed = discord.Embed(title=f"You received an {award.name} Award!",description=f"{user.mention} liked your [post]({message.jump_url}) so much that they gave it the {award.name} award.",color = 0xFFD700)
                                            embed.set_thumbnail(url=str(emoji.url))
                                            embed.set_footer(icon_url= user.avatar_url,text=f"Given by {user.name} • {self.bot.user.name} ")

                                            try: 
                                                await message.author.send(embed=embed)
                                            except:
                                                pass
                                            #post to starboard 
                                            #has a check to see if Award posts to starboard                                  
                                            await ImportantFunctions.post_to_starboard(message=message,channel=channel,user=user,emoji=emoji,reaction_name=award.name)
                                            
                                            await ImportantFunctions.add_karma(user=message.author,amt=award.karma_given_to_receiver)
                                            await ImportantFunctions.add_karma(user=user,amt=award.karma_given_to_giver)
                                            await ImportantFunctions.add_credits(user=user,amt = -award.cost)
                                            await ImportantFunctions.add_credits(user=message.author,amt = award.credits_given_to_receiver)
                                            await ImportantFunctions.add_awards(user_recieving=message.author,user_giving=user,award_name=award.name)
                                        

                                        elif str(confirm_reaction.emoji) == '❌':
                                            await check_message.delete()
                                            await message.remove_reaction(emoji, user)
                                            embed = discord.Embed(title=f"Award was cancelled.",description=f"{award.name} was cancelled.")
                                            await message.channel.send(embed=embed,delete_after=5)
                                        else:
                                            await message.channel.send("Well, you should not be able to see this. Something went wrong")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):  
        ImportantFunctions = self.bot.get_cog('ImportantFunctions') 
        channel=self.bot.get_channel(payload.channel_id) 
        user=self.bot.get_user(payload.user_id)
        message= await channel.fetch_message(payload.message_id)
        emoji=payload.emoji  
        
        if channel.guild.id in config.APPROVED_SERVERS:#if that server is approved/that server has the settings
            if user.bot:
                return
            
            type_of_event="reaction_remove"
            await self.check_if_message_is_poll(message=message,emoji=emoji,user=user,type_of_event=type_of_event)

            reaction_count =await ImportantFunctions.get_reaction_count(message=message,emoji=emoji)
            score = await ImportantFunctions.score_calculator(message=message)

            score_needed_to_pin = (await ImportantFunctions.get_settings(channel.guild.id))["meme_score_required_to_pin"]
            
            #if any post has 10 or more upvotes, award that posts author 100 credits    
            if str(emoji) == config.upvote_reaction and score <= score_needed_to_pin  and message.channel.id == config.meme_channel_id :
                await message.unpin(reason="Upvotes reduced.")
                amt=-100
                await ImportantFunctions.add_credits(user=message.author,amt=amt)
            
            #Removed Upvote remove Karma
            if str(emoji) == config.upvote_reaction and message.author != user:
                amt = random.randint(-3,-1)
                await ImportantFunctions.add_karma(user=message.author,amt=amt)
                await ImportantFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="upvote",num=-1)
            
            #Removed Downvote add Karma
            elif str(emoji) == config.downvote_reaction and message.author != user:
                amt = random.randint(0,2)
                await ImportantFunctions.add_karma(user=message.author,amt=amt)
                await ImportantFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="downvote",num=+1)

            #if the emoji is a star
            if str(emoji) == "⭐":
                #update the reactions sent in database
                await ImportantFunctions.add_reactions(user_recieving=message.author,user_giving=user,reaction_name="star",num=-1)
                async with self.bot.pool.acquire() as connection:
                    async with connection.transaction():
                        starboard_channel=self.bot.get_channel(config.starboard_channel_id) 
                        reacted_message = await connection.fetchrow("SELECT * FROM starboard WHERE root_message_id=$1",message.id)                 
                        #if this message is not in the database/ it has not been starred earlier
                        if reacted_message == None:
                            return
                        else:  
                            stars_required_for_starboard  = (await ImportantFunctions.get_settings(channel.guild.id))["starboard_stars_required"]

                            reacted_message=dict(reacted_message)
                            StarMessage = await starboard_channel.fetch_message(reacted_message["star_message_id"])
                            reactions_of_post = json.loads(reacted_message["reactions"])
                            
                            #if no reactions on message, and no awards in database
                            #only for case where no of stars required is set to 1
                            if len(message.reactions) == 0 and len(reactions_of_post) <= 1 :
                                await StarMessage.delete()
                                await connection.execute("DELETE FROM starboard WHERE root_message_id=$1",message.id)
                            
                            #if stars have become lesser than required number, and no awards in database
                            elif reaction_count < stars_required_for_starboard and len(reactions_of_post) <= 1:
                                await StarMessage.delete()
                                await connection.execute("DELETE FROM starboard WHERE root_message_id=$1",message.id)
                            
                            #if stars are enough
                            elif reaction_count >= stars_required_for_starboard:
                                await ImportantFunctions.post_to_starboard(message=message,channel=channel,user=user,emoji=emoji,reaction_name="star")
                        


def setup(bot):
    bot.add_cog(ReactionCog(bot))