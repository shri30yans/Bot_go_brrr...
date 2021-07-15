import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config   

awards_list=[awards.Rocket_Dislike,awards.Rocket_Like,awards.Wholesome_Award,awards.Silver_Award,awards.Gold_Award,awards.Platinum_Award,awards.Argentinum_Award,awards.Ternion_Award]

class ImportantFunctions(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        # run this function when this cog is loaded (which program is started)
        self.bot.loop.create_task(self.startup())

    async def startup(self):
        await self.bot.wait_until_ready()
        self.bot.loop.create_task(self.fetch_server_info())

    async def create_account(self,user:discord.Member):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                if user_account == None:
                    if user.bot:pass
                        #await ctx.send(f"{user.name} is a bot. Bots don't need accounts.")
                    else: 
                        # create an account   
                        empty_json=json.dumps({})   
                        reactions=json.dumps({"upvote":0,"downvote":0,"star":0}) 
                        await connection.execute('INSERT INTO info (user_id,credits,karma,awards_received,awards_given,reactions_received,reactions_given) VALUES ($1,0,0,$2,$3,$4,$5)',user.id,empty_json,empty_json,reactions,reactions)
                else:
                    return

    async def add_karma(self,user,amt):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                
                if user.bot:
                    return
                else: 
                    await self.create_account(user)
                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                    amt = await self.check_for_boosts(user,amt)
                    await connection.execute("UPDATE info SET karma = $1 WHERE user_id=$2",user_account["karma"]+amt,user.id)

    async def add_credits(self,user,amt):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():

                if user.bot:
                    return
                else: 
                    await self.create_account(user)             
                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                    # boost=0
                    # amt=int(amt+boost/100*amt) 
                    amt = await self.check_for_boosts(user,amt)
                    await connection.execute("UPDATE info SET credits = $1 WHERE user_id=$2",user_account["credits"]+amt,user.id)
    
    async def check_for_boosts(self,user,amt):
        if amt < 0: #if negative
            return amt
        if any([role.id in [config.wheel_karma_boost_role_id,config.wheel_credit_boost_role_id] for role in user.roles]):
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
                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user_recieving.id)
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
                    starboard=json.loads(server_info["starboard"]) #load the json content of the starboard column
                    starboard_post_list=starboard["starboard_posts"] #fetch all the posts in the starboard
                    post=None
                    for x in starboard_post_list:
                        if x["root_message_id"] == message.id:
                            post=x
                    
                    if post is None: #if message is not previously in starboard/ message is not in database ie new message
                        stars_required_for_starboard  = server_info["starboard_stars_required"]
                        
                        all_award_ids=[]
                        for award in awards_list:
                            all_award_ids.append(award.reaction_id)

                        if str(emoji) == "⭐" and reaction_count < stars_required_for_starboard:#if reaction is star but reaction count is less than the set limit
                            return
                            
                        elif str(emoji) in all_award_ids: #if reaction is an award
                            award = await self.fetch_award(award_name_or_id=str(emoji))
                            if award.starboard_post != True: #checking if the award posts to the starboard
                               return
                        
                        else:
                            pass
                        reactions_of_post={}    
                        
                        for r in message.reactions:          
                            reactions_of_post[reaction_name.lower()] = r.count
                    
                        #Embed
                        reaction_id_string = await self.format_awards_in_order(reactions_of_post=reactions_of_post)
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
                        StarMessage= await starboard_channel.fetch_message(post["star_message_id"])
                        reactions_of_post=json.loads(post["reactions"])
                        
                        if reaction_name.lower() in reactions_of_post:#if a similiar award or a star has already been given, add one more
                            reactions_of_post[reaction_name.lower()] = reactions_of_post[reaction_name.lower()] + 1
                        else:
                            #need to create a new key-value pair
                            reactions_of_post.update({reaction_name.lower():1})
                        
                        #Embed
                        reaction_id_string = await self.format_awards_in_order(reactions_of_post=reactions_of_post)
                        reaction_id_string = reaction_id_string + channel.mention
                        await StarMessage.edit(content=f"{reaction_id_string}")
                        
                        #Database Actions
                        post["reactions"]=reactions_of_post
                        starboard_json=json.dumps(starboard)
                        await connection.execute("UPDATE server_info SET starboard = $1 WHERE id=$2",starboard_json,channel.guild.id)
                
    
    async def format_awards_in_order(self,reactions_of_post):
        #used to arrange the award and stars in order so that the order in starboard is [ternion,argentinum,platinum,gold....star]
        ordered_reactions_of_post={}
        for x in awards_list[::-1]:
            try:
                ordered_reactions_of_post[x.name.lower()]=reactions_of_post[x.name.lower()]
            except:
                pass
        try:
            #if post has stars
            ordered_reactions_of_post["star"]=reactions_of_post["star"]
        except:
            pass
        reactions_of_post = ordered_reactions_of_post
        

        all_award_names=[]
        for award in awards_list:
            all_award_names.append(award.name.lower())
        reaction_id_string=""
        for r in reactions_of_post:
            if r == "star":
                reaction_id = "⭐"
            elif r in all_award_names:
                award = await self.fetch_award(award_name_or_id=r)
                if award == None:
                    print("Not found award")
                reaction_id = award.reaction_id
            else:
                print("Not an award or an Star")
            reaction_id_string = reaction_id_string + f"{reactions_of_post[r]} {reaction_id}   "

        return reaction_id_string
    
    
    async def fetch_award(self,award_name_or_id):  
        for award in awards_list: 
            if award_name_or_id.lower() == award.name.lower():#check against names
                return award
        else:
            
            for award in awards_list:
                if award_name_or_id.lower() == award.reaction_id.lower():#check against name of emojis with ids
                    return award
            else:
                for award in awards_list:
                    if award_name_or_id == int(award.reaction_id.split(":")[-1][:-1]):#check against ids/ Numeric Value of the id
                        return award
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