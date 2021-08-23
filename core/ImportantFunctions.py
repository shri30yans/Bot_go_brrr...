import discord,json,random
from discord.ext import commands
import utils.awards as awards
import utils.badges as badges
import config   
from datetime import datetime
import asyncio

colourlist=config.embed_colours

class ImportantFunctions(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    
    async def fetch_award(self,award_name_or_id):  
        for award in list(awards.awards_list.values())[::-1]:
            try: 
                if award_name_or_id.lower() == award.name.lower():#check against names
                    return award
            except: 
                pass
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
            try:
                if badge_name_or_id.lower() == badge.name.lower():#check against names
                    return badge
            except:
                pass
        else:
            
            for badge in list(badges.badges_list.values())[::-1]: 
                if badge_name_or_id == badge.reaction_id:#check against names
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
        score = (upvote_count - downvote_count) - 1 #-1 To ignore bot reactions
        return score


    async def create_tables(self):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute('''CREATE TABLE IF NOT EXISTS info (
                                        "user_id" int   PRIMARY KEY,
                                        "credits" bigint,
                                        "karma" bigint,
                                        "badges" json,
                                        "awards_recieved" json,
                                        "awards_given" json,
                                        "cooldown" json,
                                        "settings" json
                                        );

                                        CREATE TABLE IF NOT EXISTS server_info(
                                            "id"  int   PRIMARY KEY,
                                            "starboard" json,
                                            "ongoing_polls" json,
                                            "prefixes" json
                                        ); ''')

    
    @commands.Cog.listener(name="on_guild_join")
    async def on_guild_join(self,guild):  
        await self.has_server_entry(guild=guild,action='add')
        embed=discord.Embed(color = random.choice(colourlist))
        embed.add_field(name=f"Just joined {guild.name}",value=f"Members:{len(guild.members)} \nID: {guild.id} \n I am now in {str(len(self.bot.guilds))} servers. )") 
        embed.set_thumbnail(url=str(guild.icon_url))
        embed.set_image(url=config.help_animation_link)
        guild_join_update_channel=self.bot.get_channel(config.guild_join_update_channel_id)
        await guild_join_update_channel.send(embed=embed)

    @commands.Cog.listener(name="on_guild_remove")
    async def on_guild_remove(self,guild):  
        await self.has_server_entry(guild=guild,action="remove")
        embed=discord.Embed(color = random.choice(colourlist))
        embed.add_field(name=f"Just left {guild.name}",value=f"Members:{len(guild.members)} \nID: {guild.id} \n I am now in {str(len(self.bot.guilds))} servers. )") 
        embed.set_thumbnail(url=str(guild.icon_url))
        embed.set_image(url=config.help_animation_link)
        guild_leave_update_channel=self.bot.get_channel(config.guild_leave_update_channel_id)
        await guild_leave_update_channel.send(embed=embed)
    
    
    async def has_server_entry(self,guild,action):
        
        async def create_new_server_entry(guild):
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    prefixes = json.dumps({"prefixes": ["uwu"]})
                    polls=json.dumps({"polls":[]})
                    starboard=json.dumps({"starboard_posts": [], "stars_required": 6, "starboard_channel_id": None , "self_star": True,"nsfw":False,"private_channel":False,"lock": False, "emoji": ["\u2b50"]})
                    await connection.execute('INSERT INTO server_info (id,ongoing_polls,starboard,prefixes) VALUES ($1,$2,$3,$4)',guild.id,polls,starboard,prefixes)
            
        
        async def remove_server_entry(guild):
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute('DELETE FROM server_info WHERE id = $1',guild.id)
        
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                server_record = dict(await connection.fetchrow("SELECT EXISTS(SELECT 1 FROM server_info WHERE id=$1)",guild.id))
                if action == "add":
                    if server_record["exists"] == False:
                        await create_new_server_entry(guild)
                    else:
                        return 
                elif action == "remove":
                    if server_record["exists"] == False:
                        return
                    else:
                        await remove_server_entry(guild)

               


    async def get_server_settings(self,guild_id):
        try:
            return self.bot.Info_Table[guild_id]
        except:
            await self.update_server_settings_cache(guild_id)
            return self.bot.Info_Table[guild_id]

    
    async def update_server_settings_cache(self,guild_id):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                row = await connection.fetchrow("SELECT * FROM server_info WHERE id = $1",guild_id)
                self.bot.Info_Table[dict(row)["id"]] = dict(row)
                #print(self.bot.Info_Table)
    
    
    async def update_server_settings_key_cache(self,guild_id,key,value):
        await self.get_server_settings(guild_id)
        self.bot.Info_Table[guild_id][key] = value

    
    async def get_server_prefixes_string(self,guild_id):
        async def get_server_prefixes_list(guild_id):
            try:
                #Try statement since searching may sometimes result in a key error
                server_settings=await self.get_server_settings(guild_id)
                prefix_json=json.loads(server_settings["prefixes"])
                return prefix_json["prefixes"]
            except:
                return
        try:
            #Try statement since searching may sometimes result in a key error
            prefix_list = (await get_server_prefixes_list(guild_id=guild_id))
            prefix=', '.join(prefix_list)
            return prefix
        except:
            return


    async def update_server_prefix(self,new_prefix,guild_id):
        new_prefix_list=[]
        new_prefix_list.append(new_prefix)  
        new_prefix_json = json.dumps({"prefixes":new_prefix_list})      
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("UPDATE server_info SET prefixes = $1 WHERE id = $2",new_prefix_json,guild_id)
                await self.update_server_settings_key_cache(guild_id=guild_id,key="prefixes",value=new_prefix_json)


   
                
     
    
        




    

def setup(bot):
    bot.add_cog(ImportantFunctions(bot))