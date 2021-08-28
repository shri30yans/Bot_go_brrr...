import discord,json
from discord.ext import commands
import utils.awards as awards
import utils.badges as badges  

class UserDatabaseFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_user_info(self,user):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await self.has_account(user)
                user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                user_account=dict(user_account)
                return user_account

    async def get_user_cooldown(self,user):
         async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await self.has_account(user)
                user_account = await connection.fetchrow("SELECT cooldown FROM info WHERE user_id=$1",user.id)
                user_account=dict(user_account)
                return user_account["cooldown"]
    
    async def get_user_passive_mode(self,user):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await self.has_account(user)
                user_account = await connection.fetchrow("SELECT passive FROM info WHERE user_id=$1",user.id)
                user_account=dict(user_account)
                return user_account["passive"]
    
    async def get_user_credits(self,user):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await self.has_account(user)
                user_account = await connection.fetchrow("SELECT credits FROM info WHERE user_id=$1",user.id)
                user_account=dict(user_account)
                return user_account["credits"]
   
    async def get_user_karma(self,user):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await self.has_account(user)
                user_account = await connection.fetchrow("SELECT karma FROM info WHERE user_id=$1",user.id)
                user_account=dict(user_account)
                return user_account["karma"]
    
    
    async def give(self,user_giving,user_taking,amt,boost_check=True):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await self.has_account(user_giving)
                if user_giving.bot or user_taking.bot:
                    return
                else: 
                    await self.has_account(user_giving)     
                    await self.has_account(user_taking) 
                    if boost_check:   
                        amt = await self.check_for_boosts(user_taking,amt,type="credits")
                    await connection.execute("UPDATE info SET credits = credits - $1 WHERE user_id=$2",amt,user_giving.id)
                    await connection.execute("UPDATE info SET credits = credits + $1 WHERE user_id=$2",amt,user_taking.id)
    
    async def has_account(self,user:discord.Member):
        async def create_account(user:discord.Member):
            empty_json=json.dumps({})   
            reactions=json.dumps({"upvote":0,"downvote":0,"star":0}) 
            badges=json.dumps({"badges":[]})
            await connection.execute('INSERT INTO info (user_id,credits,karma,awards_received,awards_given,reactions_received,reactions_given,badges,cooldown) VALUES ($1,0,0,$2,$3,$4,$5,$6,$7)',user.id,empty_json,empty_json,reactions,reactions,badges,empty_json)
        if user.bot:
            return 
        else:
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    user_account = dict(await connection.fetchrow("SELECT EXISTS(SELECT 1 FROM info WHERE user_id=$1)",user.id))
                    
                    if user_account["exists"] == False:
                        await create_account(user)
                    else:
                        return 
        

    async def add_karma(self,user,amt,boost_check=True):
        if amt == 0:
            return
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                
                if user.bot:
                    return
                else: 
                    await self.has_account(user)
                    if boost_check:
                        amt = await self.check_for_boosts(user,amt,type="karma")
                    await connection.execute("UPDATE info SET karma = karma +$1 WHERE user_id=$2",amt,user.id)
                   

    async def add_credits(self,user,amt,boost_check=True):
        if amt == 0:
            return
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():

                if user.bot:
                    return
                else: 
                    await self.has_account(user)             
                    # boost=0
                    # amt=int(amt+boost/100*amt) 
                    if boost_check:
                        amt = await self.check_for_boosts(user,amt,type="credits")
                    await connection.execute("UPDATE info SET credits = credits + $1 WHERE user_id=$2",amt,user.id)
    
    async def check_for_boosts(self,user,amt,type):
        if amt < 0: #Doesn't give double negative credits
            return amt

        if type == "karma":
            outcome = await self.check_if_has_badge(user,badge_name="Double Karma Badge")

        elif type == "credits":
            outcome= await self.check_if_has_badge(user,badge_name="Double Credits Badge")
        
        if outcome:
            amt=amt*2
            return amt*5
        else:
            return amt*5


    async def add_awards(self,user_recieving,user_giving,award_name:str):
        await self.has_account(user_recieving) 
        await self.has_account(user_giving) 
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
        await self.has_account(user) 
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
        await self.has_account(user) 
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
        await self.has_account(user)
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                user_account = await connection.fetchrow("SELECT badges FROM info WHERE user_id=$1",user.id)
                user_account= dict(user_account)
                badges = json.loads(user_account["badges"])
                badges_list=badges["badges"]
                return badge_name in badges_list
                    

def setup(bot):
    bot.add_cog(UserDatabaseFunctions(bot))