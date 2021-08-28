from core.ImportantFunctions import ImportantFunctions
from core.UserDatabaseFunctions import UserDatabaseFunctions
from utils.ErrorHandler import *
from discord.ext import commands
import config 
import json
from  datetime import datetime

def server_is_approved():
    async def predicate(ctx):
        if ctx.guild.id in config.APPROVED_SERVERS:
            return True
        else:
            raise NotApprovedServer()
    return commands.check(predicate)





def CustomCooldown(key,delay):
    async def get_last_cooldown(ctx):
        UserDatabaseFunctions = ctx.bot.get_cog('UserDatabaseFunctions')
        user=ctx.author
        async def set_cooldown_to_current(user,key):
            async with ctx.bot.pool.acquire() as connection:
                async with connection.transaction():
                    user_account = await connection.fetchrow("SELECT cooldown FROM info WHERE user_id=$1",user.id)
                    cooldown_info = json.loads(user_account["cooldown"])
                    a_datetime = datetime.now()
                    formatted_datetime = a_datetime.isoformat()
                    cooldown_info[key]=formatted_datetime
                    json_datetime = json.dumps(cooldown_info)
                    await connection.execute("UPDATE info SET cooldown = $1 WHERE user_id=$2",json_datetime,user.id)

        cooldown = await UserDatabaseFunctions.get_user_cooldown(user)
        cooldown_info = json.loads(cooldown)
        
        if key in cooldown_info:
            isoformat = cooldown_info[key]            
            elapsed = datetime.now() - datetime.fromisoformat(isoformat)
            seconds_elapsed=int(elapsed.total_seconds())
            retry_after=delay-seconds_elapsed
            
            if retry_after <= 0: #Delay - Time elapsed will give less than 0 if the time elapsed since last command is greater than 0
                await set_cooldown_to_current(user=user,key=key)
                return True
            else:
                raise CustomCommandOnCooldown(ctx=ctx,user=ctx.author,retry_after=retry_after)

        else:
            await set_cooldown_to_current(user=user,key=key)
            return True
    return commands.check(get_last_cooldown)

# def PassiveModeCheck(key,delay):
#     async def get_last_cooldown(ctx):
#         UserDatabaseFunctions = ctx.bot.get_cog('UserDatabaseFunctions')
#         user=ctx.author
#         async def set_cooldown_to_current(user,key):
#             async with ctx.bot.pool.acquire() as connection:
#                 async with connection.transaction():
#                     user_account = await connection.fetchrow("SELECT cooldown FROM info WHERE user_id=$1",user.id)
#                     cooldown_info = json.loads(user_account["cooldown"])
#                     a_datetime = datetime.now()
#                     formatted_datetime = a_datetime.isoformat()
#                     cooldown_info[key]=formatted_datetime
#                     json_datetime = json.dumps(cooldown_info)
#                     await connection.execute("UPDATE info SET cooldown = $1 WHERE user_id=$2",json_datetime,user.id)

#         cooldown = await UserDatabaseFunctions.get_user_passive_mode(user)
        
#         if key in cooldown_info:
#             isoformat = cooldown_info[key]            
#             elapsed = datetime.now() - datetime.fromisoformat(isoformat)
#             seconds_elapsed=int(elapsed.total_seconds())
#             retry_after=delay-seconds_elapsed
            
#             if retry_after <= 0: #Delay - Time elapsed will give less than 0 if the time elapsed since last command is greater than 0
#                 await set_cooldown_to_current(user=user,key=key)
#                 return True
#             else:
#                 raise CustomCommandOnCooldown(ctx=ctx,user=ctx.author,retry_after=retry_after)

#         else:
#             await set_cooldown_to_current(user=user,key=key)
#             return True
#     return commands.check(get_last_cooldown)


async def get_last_robbed_from(ctx,user,delay):
    UserDatabaseFunctions = ctx.bot.get_cog('UserDatabaseFunctions')
    key="last_robbed_from"
    async def set_cooldown_to_current(user,key):
        async with ctx.bot.pool.acquire() as connection:
            async with connection.transaction():
                user_account = await connection.fetchrow("SELECT cooldown FROM info WHERE user_id=$1",user.id)
                cooldown_info = json.loads(user_account["cooldown"])
                a_datetime = datetime.now()
                formatted_datetime = a_datetime.isoformat()
                cooldown_info[key]=formatted_datetime
                json_datetime = json.dumps(cooldown_info)
                await connection.execute("UPDATE info SET cooldown = $1 WHERE user_id=$2",json_datetime,user.id)

    cooldown = await UserDatabaseFunctions.get_user_cooldown(user)
    cooldown_info = json.loads(cooldown)
    
    if key in cooldown_info:
        isoformat = cooldown_info[key]            
        elapsed = datetime.now() - datetime.fromisoformat(isoformat)
        seconds_elapsed=int(elapsed.total_seconds())
        retry_after=delay-seconds_elapsed
        
        if retry_after <= 0: #Delay - Time elapsed will give less than 0 if the time elapsed since last command is greater than 0
            await set_cooldown_to_current(user=user,key=key)
            return True
        else:
            return False

    else:
        await set_cooldown_to_current(user=user,key=key)
        return True

def CheckIfStarboardExists():
    async def starboard_channel_check(ctx):
        guild_id = ctx.guild.id
        StarboardFunctions = ctx.bot.get_cog('StarboardFunctions')
        starboard_info = await StarboardFunctions.get_starboard_info(ctx.guild.id)
        channel_id = starboard_info["starboard_channel_id"]
        starboard_channel = ctx.bot.get_channel(channel_id)
        #print(starboard_channel,channel_id)

        if channel_id is None:
            raise StarboardChannelNotSet()
        
        elif (starboard_channel is None) and (channel_id is not None):
            #if the starboard channel is None, but a channel is stored in the database (Starboard channel is deleted), reset the stored information
            starboard_info["starboard_channel_id"] = None
            starboard_info["starboard_posts"]=[]
            await StarboardFunctions.update_starboard(starboard_info,guild_id)

        else:
            return True

    return commands.check(starboard_channel_check)

def CheckIfSetupNotCommandUsedBefore():
    async def starboard_setup_check(ctx):
        StarboardFunctions = ctx.bot.get_cog('StarboardFunctions')
        starboard_info = await StarboardFunctions.get_starboard_info(ctx.guild.id)
        
        if starboard_info["starboard_channel_id"] is None:
            return True
            
        else:
            raise StarboardSetupCommandAlreadyRun()

    return commands.check(starboard_setup_check)

        

    
    