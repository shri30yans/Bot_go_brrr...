import discord,json
from discord.ext import commands
import utils.awards as awards
import utils.badges as badges
import config   
from datetime import datetime


class ImportantFunctions(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        # run this function when this cog is loaded (which program is started)
        self.bot.loop.create_task(self.startup())

    
    async def startup(self):
        await self.bot.wait_until_ready()
        self.bot.loop.create_task(self.fetch_server_info())

    async def get_user_info(self,user):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await self.create_account(user)
                user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                user_account=dict(user_account)
                return user_account
    
    async def create_account(self,user:discord.Member):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                user_account = await connection.fetchrow("SELECT credits FROM info WHERE user_id=$1",user.id)
                if user_account == None:
                    if user.bot:
                        pass
                    else: 
                        # create an account   
                        empty_json=json.dumps({})   
                        reactions=json.dumps({"upvote":0,"downvote":0,"star":0}) 
                        badges=json.dumps({"badges":[]})
                        await connection.execute('INSERT INTO info (user_id,credits,karma,awards_received,awards_given,reactions_received,reactions_given,badges,cooldown) VALUES ($1,0,0,$2,$3,$4,$5,$6,$7)',user.id,empty_json,empty_json,reactions,reactions,badges,empty_json)
                else:
                    return

    async def add_karma(self,user,amt):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                
                if user.bot:
                    return
                else: 
                    await self.create_account(user)
                    user_account = await connection.fetchrow("SELECT karma FROM info WHERE user_id=$1",user.id)
                    amt = await self.check_for_boosts(user,amt,type="karma")
                    await connection.execute("UPDATE info SET karma = $1 WHERE user_id=$2",user_account["karma"]+amt,user.id)
                   

    async def add_credits(self,user,amt):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():

                if user.bot:
                    return
                else: 
                    await self.create_account(user)             
                    user_account = await connection.fetchrow("SELECT credits FROM info WHERE user_id=$1",user.id)
                    # boost=0
                    # amt=int(amt+boost/100*amt) 
                    amt = await self.check_for_boosts(user,amt,type="credits")
                    await connection.execute("UPDATE info SET credits = $1 WHERE user_id=$2",user_account["credits"]+amt,user.id)
    
    async def check_for_boosts(self,user,amt,type):
        if amt < 0: #Doesn't give double negative credits
            return amt

        if type == "karma":
            outcome = await self.check_if_has_badge(user,badge_name="Double Karma Badge")

        elif type == "credits":
            outcome= await self.check_if_has_badge(user,badge_name="Double Credits Badge")
        
        if outcome:
            amt=amt*2
            return amt
        else:
            return amt


    async def add_awards(self,user_recieving,user_giving,award_name:str):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                
                if user_recieving.bot:
                    pass
                else:
                    user_account = await connection.fetchrow("SELECT awards_received FROM info WHERE user_id=$1",user_recieving.id)
                    user_account= dict(user_account)
                    awards_received=json.loads(user_account["awards_received"])
                    
                    if award_name in awards_received:
                        awards_received[award_name]=awards_received[award_name] + 1
                    else:
                        awards_received.update({award_name:1})

                    awards_update=json.dumps(awards_received)
                    await connection.execute("UPDATE info SET awards_received = $1 WHERE user_id=$2",awards_update,user_recieving.id)

                if user_giving.bot:
                    pass
                else:
                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user_giving.id)
                    user_account= dict(user_account)
                    awards_given=json.loads(user_account["awards_given"])
                    if award_name in awards_given:
                        awards_given[award_name]=awards_given[award_name] + 1
                    else:
                        awards_given.update({award_name:1})
                    awards_update=json.dumps(awards_given)
                    await connection.execute("UPDATE info SET awards_given = $1 WHERE user_id=$2",awards_update,user_giving.id)

    async def edit_badges(self,user,badge_name:str,action="add"):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                if user.bot:
                    pass
                else:
                    user_account = await connection.fetchrow("SELECT badges FROM info WHERE user_id=$1",user.id)
                    user_account= dict(user_account)
                    badges=json.loads(user_account["badges"])
                    badges_list=badges["badges"]
                    if action == "add":
                        if badge_name in badges_list:#Already has the badge
                            return False
                        else:
                            badges_list.append(badge_name)
                    elif action == "remove":
                        badges_list.remove(badge_name)
                    
                    badges_update=json.dumps(badges)
                    await connection.execute("UPDATE info SET badges = $1 WHERE user_id = $2",badges_update,user.id)
                    return True

    async def check_if_badges_need_to_be_given(self,user):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                if user.bot:
                    pass
                else:
                    user_account = await connection.fetchrow("SELECT karma FROM info WHERE user_id = $1",user.id)
                    user_account= dict(user_account)
                    #print(user_account["karma"])
                    for badge in list(badges.badges_list.values()):
                        #print(badge.name)
                        if (badge.karma_required is not None) and (badge.karma_required <= user_account["karma"]):
                            await self.edit_badges(user,badge_name=badge.name,action="add")
    
    async def check_if_has_badge(self,user,badge_name):    
        await self.create_account(user)
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                user_account = await connection.fetchrow("SELECT badges FROM info WHERE user_id=$1",user.id)
                user_account= dict(user_account)
                badges = json.loads(user_account["badges"])
                badges_list=badges["badges"]
                return badge_name in badges_list
                    
    #Adds reaction count for each perosn
    async def add_reactions(self,user_recieving,user_giving,reaction_name:str,num):
        await self.create_account(user=user_recieving)
        await self.create_account(user=user_giving)
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                if user_recieving.bot:#if the user recieving the award is a bot pass
                    pass
                else:
                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user_recieving.id)
                    user_account= dict(user_account)
                    reactions_received=json.loads(user_account["reactions_received"])
                    reactions_received[reaction_name]=reactions_received[reaction_name] + num
                    reactions_update=json.dumps(reactions_received)
                    await connection.execute("UPDATE info SET reactions_received = $1 WHERE user_id=$2",reactions_update,user_recieving.id)
                
                if user_giving.bot: #if the user giving the award is a bot pass
                    pass
                else:
                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user_giving.id)
                    user_account= dict(user_account)
                    reactions_given=json.loads(user_account["reactions_given"])
                    reactions_given[reaction_name]=reactions_given[reaction_name] + num
                    reactions_update=json.dumps(reactions_given)
                    await connection.execute("UPDATE info SET reactions_given = $1 WHERE user_id=$2",reactions_update,user_giving.id)
    
    async def post_to_starboard(self,message,channel,user,emoji,reaction_name): 
        starboard_channel=self.bot.get_channel(config.starboard_channel_id)     
        reaction_count = await self.get_reaction_count(message=message,emoji=emoji)
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                    server_info = await connection.fetchrow("SELECT * FROM server_info WHERE id=$1",channel.guild.id)
                    starboard=json.loads(server_info["starboard"])#load the json content of the starboard column
                    starboard_post_list=starboard["starboard_posts"] #fetch all the posts in the starboard
                    
                    post=None
                    for x in starboard_post_list:
                        if x["root_message_id"] == message.id:
                            post=x
                            break
                    
                    
                    if post is None: #if message is not previously in starboard/ message is not in database ie new message 
                        
                        all_award_ids=[]
                        for award in list(awards.awards_list.values())[::-1]:
                            all_award_ids.append(award.reaction_id)

                        if str(emoji) == "⭐" and reaction_count < server_info["starboard_stars_required"]:
                            #if reaction is star but reaction count is less than the set limit it will be returned
                            return
                            
                        elif str(emoji) in all_award_ids: #if reaction is an award
                            award = await self.fetch_award(award_name_or_id=str(emoji))
                            if award.starboard_post != True: #checking if the award posts to the starboard
                               return
                        
                        #This is reached when either the award posts to starboard or the star limit has been reached
                        reactions_of_post={}    
                        for r in message.reactions: 
                            for award in  list(awards.awards_list.values())[::-1]:   
                                if str(r.emoji) in award.reaction_id:
                                    reactions_of_post[award.name] = r.count
                                    break

                            if str(r.emoji) == "⭐":
                                reactions_of_post["star"] = r.count

                    
                        #Embed
                        reaction_id_string = await self.formatted_starboard_awards_string(reactions_of_post=reactions_of_post)
                        reaction_id_string = reaction_id_string + channel.mention

                        embed=discord.Embed(color = channel.guild.me.colour,timestamp=message.created_at,description=message.content)
                        embed.set_author(name=message.author.name, icon_url= f"{message.author.avatar_url}")
                        embed.add_field(name="Source:", value=f"[Jump]({message.jump_url})", inline=False)
                        
                        if len(message.attachments): #basically if len !=0 or if attachments are there
                            embed.set_image(url=message.attachments[0].url)

                        embed.set_footer(text=f"{message.id}")
                       
                        StarMessage = await starboard_channel.send(content=f"{reaction_id_string}",embed=embed)

                        #Database Actions
                        starboard_post_info={"root_message_id":message.id ,"star_message_id":StarMessage.id ,"reactions":reactions_of_post}
                        starboard_post_list.append(starboard_post_info)
                        starboard_json=json.dumps(starboard)
                        await connection.execute("UPDATE server_info SET starboard = $1 WHERE id=$2",starboard_json,channel.guild.id)
                                
                    else: #message exists in starboard/is present in the databse
                        StarMessage = await starboard_channel.fetch_message(post["star_message_id"])
                        reactions_of_post=post["reactions"]
                        
                        if reaction_name.lower() in reactions_of_post:#if a similiar award or a star has already been given, add one more
                            reactions_of_post[reaction_name.lower()] = reactions_of_post[reaction_name.lower()] + 1
                        else:
                            #need to create a new key-value pair
                            reactions_of_post.update({reaction_name.lower():1})
                        
                        #Embed
                        reaction_id_string = await self.formatted_starboard_awards_string(reactions_of_post=reactions_of_post)
                        reaction_id_string = reaction_id_string + channel.mention
                        await StarMessage.edit(content=f"{reaction_id_string}")
                        
                        #Database Actions
                        post["reactions"]=reactions_of_post
                        starboard_json=json.dumps(starboard)
                        await connection.execute("UPDATE server_info SET starboard = $1 WHERE id=$2",starboard_json,channel.guild.id)
                
    async def formatted_starboard_awards_string(self,reactions_of_post):
        #used to arrange the award and stars in order so that the order in starboard is [ternion,argentinum,platinum,gold....star]
        ordered_reactions_of_post={}
        for x in list(awards.awards_list.values())[::-1]:
            try:
                ordered_reactions_of_post[x.name]=reactions_of_post[x.name]
            except:
                pass
        try:
            #if post has stars
            ordered_reactions_of_post["star"]=reactions_of_post["star"]
        except:
            pass        

        reaction_id_string=""
        for r in ordered_reactions_of_post:
            if r == "star":
                reaction_id = "⭐"
            else:
                try:
                    award = await self.fetch_award(award_name_or_id=r)
                    reaction_id = award.reaction_id
                except:
                    print("Not an award or an star.")
            
            reaction_id_string = reaction_id_string + f"{ordered_reactions_of_post[r]} {reaction_id}   "

        return reaction_id_string
    
    async def fetch_award(self,award_name_or_id):  
        for award in list(awards.awards_list.values())[::-1]: 
            if award_name_or_id.lower() == award.name.lower():#check against names
                return award
        else:
            
            for award in list(awards.awards_list.values())[::-1]:
                if award_name_or_id.lower() == award.reaction_id.lower():#check against name of emojis with ids
                    return award
            else:
                for award in list(awards.awards_list.values())[::-1]:
                    if award_name_or_id == int(award.reaction_id.split(":")[-1][:-1]):#check against ids/ Numeric Value of the id
                        return award
                else:
                    return None

    async def fetch_badge(self,badge_name_or_id):  
        for badge in list(badges.badges_list.values())[::-1]: 
            if badge_name_or_id.lower() == badge.name.lower():#check against names
                return badge
        else:
            
            for badge in list(badges.badges_list.values())[::-1]: 
                if badge_name_or_id.lower() == badge.reaction_id.lower():#check against names
                    return badge
            else:
                for badge in list(awards.awards_list.values())[::-1]:
                    if badge_name_or_id == int(badge.reaction_id.split(":")[-1][:-1]):#check against ids/ Numeric Value of the id
                        return badge
                else:
                    return None

    async def get_reaction_count(self,message,emoji):
        if len(message.reactions) == 0:
            reaction_count=0
            return reaction_count
            
        else:
            for x in message.reactions:
                if str(x.emoji) == str(emoji):
                    reaction = x
                    reaction_count=reaction.count
                    return reaction_count
                else: 
                    reaction_count = 0
                    return reaction_count

    async def score_calculator(self,message):
        upvote_count= await self.get_reaction_count(message=message,emoji=config.upvote_reaction)
        downvote_count= await self.get_reaction_count(message=message,emoji=config.downvote_reaction)
        score = upvote_count - downvote_count
        return score
    
    async def fetch_server_info(self):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                self.Info_table = await connection.fetch("SELECT * FROM server_info")
                #print(Info_table)

    async def get_settings(self,server_id):
        for server in self.Info_table:
            if server_id == server["id"]:
                return dict(server)

    

def setup(bot):
    bot.add_cog(ImportantFunctions(bot))