import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config   

awards_list=[awards.Rocket_Dislike,awards.Rocket_Like,awards.Wholesome_Award,awards.Silver_Award,awards.Gold_Award,awards.Platinum_Award,awards.Argentinum_Award,awards.Ternion_Award]

class ImportantFunctions(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

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
        #user=ctx.author
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():

                if user.bot:
                    return
                else: 
                    await self.create_account(user)

                user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                await connection.execute("UPDATE info SET karma = $1 WHERE user_id=$2",user_account["karma"]+amt,user.id)

    async def add_credits(self,user,amt):
        #user=ctx.author
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():

                if user.bot:
                    return
                else: 
                    await self.create_account(user)

                user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                await connection.execute("UPDATE info SET credits = $1 WHERE user_id=$2",user_account["credits"]+amt,user.id)
                #await ctx.send(f"Someone gave you {earnings} credits")

    async def add_awards(self,user_recieving,user_giving,award_name:str):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                if user_recieving.bot:pass
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

                if user_giving.bot:pass
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

    async def add_reactions(self,user_recieving,user_giving,reaction_name:str,num):
        await self.create_account(user=user_recieving)
        await self.create_account(user=user_giving)
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                if user_recieving.bot:pass
                else:

                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user_recieving.id)
                    user_account= dict(user_account)
                    reactions_received=json.loads(user_account["reactions_received"])
                    reactions_received[reaction_name]=reactions_received[reaction_name] + num
                    reactions_update=json.dumps(reactions_received)
                    await connection.execute("UPDATE info SET reactions_received = $1 WHERE user_id=$2",reactions_update,user_recieving.id)
                    #print("Recieving",user_recieving.name,reactions_update)
                
                if user_giving.bot:pass
                else:
                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user_giving.id)
                    user_account= dict(user_account)
                    reactions_given=json.loads(user_account["reactions_given"])
                    reactions_given[reaction_name]=reactions_given[reaction_name] + num
                    reactions_update=json.dumps(reactions_given)
                    await connection.execute("UPDATE info SET reactions_given = $1 WHERE user_id=$2",reactions_update,user_giving.id)
                    #print("Giving",user_giving.name,reactions_update)


    async def post_to_starboard(self,message,channel,user,reaction,type_of_reaction,reaction_name):  
        starboard_channel=self.bot.get_channel(config.starboard_channel_id)
        # for x in message.reactions:
        #     if x.emoji == emoji:
        #         reaction = x

        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                reacted_message = await connection.fetchrow("SELECT * FROM starboard WHERE root_message_id=$1",message.id)
                if reacted_message == None:#if message is not previously in starboard/ message is not in database
                    all_award_ids=[]
                    for award in awards_list:
                        all_award_ids.append(award.reaction_id)
                    
                    for r in message.reactions:
                        if str(r.emoji) in all_award_ids or str(r.emoji) == "⭐":
                            embed=discord.Embed(color = channel.guild.me.colour,timestamp=message.created_at,description=message.content)
                            embed.set_author(name=message.author.name, icon_url= f"{message.author.avatar_url}")
                            embed.add_field(name="Source:", value=f"[Jump]({message.jump_url})", inline=False)
                            if len(message.attachments): #basically if len !=0
                                embed.set_image(url=message.attachments[0].url)
                            embed.set_footer(text=f"{message.id} ")

                            if type_of_reaction == "Star" and reaction.count >= config.stars_required_for_starboard:
                                reaction_id = "⭐" 
                            elif type_of_reaction == "Award":
                                award = await self.fetch_award(award_name=reaction_name)
                                #print(award.name)
                                reaction_id = award.reaction_id
                            else:
                                #means stars are less that the required number 
                                return

                            StarMessage = await starboard_channel.send(f"{reaction.count} {reaction_id} {channel.mention}",embed=embed)

                            reaction_json=json.dumps({reaction_name.lower():reaction.count})                            
                            await connection.execute('INSERT INTO starboard (root_message_id,star_message_id,reactions) VALUES ($1,$2,$3)',message.id,StarMessage.id,reaction_json)
                            
                elif reacted_message != None:#message exists in starboard/is present in the databse
                    reacted_message=dict(reacted_message)
                    StarMessage= await starboard_channel.fetch_message(reacted_message["star_message_id"])
                    reactions_of_post=json.loads(reacted_message["reactions"])
                    if reaction_name.lower() in reactions_of_post:
                        #reactions_of_post[reaction_name.lower()] = reactions_of_post[reaction_name.lower()] + 1
                        reactions_of_post[reaction_name.lower()] = reaction.count
                    else:
                        reactions_of_post.update({reaction_name.lower():1})
                    
                    reaction_id_string= await self.format_awards_in_order(message=message,channel=channel,user=user,reactions_of_post=reactions_of_post)
                    
                    await StarMessage.edit(content=f"{reaction_id_string}")

                    reactions_of_post_j=json.dumps(reactions_of_post)
                    await connection.execute("UPDATE starboard SET reactions = $1 WHERE root_message_id=$2",reactions_of_post_j,message.id)
                
                else:
                    print("How is did we get here? This is not possible")
    
    async def format_awards_in_order(self,message,channel,user,reactions_of_post):
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
                award = await self.fetch_award(award_name=r)
                if award == "Not Found":
                    print("Not found award")
                    #return
                reaction_id = award.reaction_id
            else:
                print("Not an award or an Star")
            reaction_id_string = reaction_id_string + f"{reactions_of_post[r]} {reaction_id}   "
        reaction_id_string = reaction_id_string + channel.mention
        return reaction_id_string
    
    
    async def fetch_award(self,award_name):
        for award in awards_list:
            if award_name.lower() == award.name.lower():
                #print(award.name)
                return award
        else:
            return "Not found"
    

def setup(bot):
    bot.add_cog(ImportantFunctions(bot))