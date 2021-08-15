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
            raise NotApprovedServer(user=ctx.author)
    return commands.check(predicate)


def CustomCooldown(key,delay):
    async def get_last_cooldown(ctx):
        ImportantFunctions = ctx.bot.get_cog('ImportantFunctions')
        user=ctx.author
        async def set_cooldown_to_current(user,key):
            async with ctx.bot.pool.acquire() as connection:
                async with connection.transaction():
                    user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                    cooldown_info = json.loads(user_account["cooldown"])
                    a_datetime = datetime.now()
                    formatted_datetime = a_datetime.isoformat()
                    cooldown_info[key]=formatted_datetime
                    json_datetime = json.dumps(cooldown_info)
                    await connection.execute("UPDATE info SET cooldown = $1 WHERE user_id=$2",json_datetime,user.id)

        user_account = await ImportantFunctions.get_user_info(user)
        cooldown_info = json.loads(user_account["cooldown"])
        
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

async def get_last_robbed_from(ctx,user,delay):
    ImportantFunctions = ctx.bot.get_cog('ImportantFunctions')
    key="last_robbed_from"
    async def set_cooldown_to_current(user,key):
        async with ctx.bot.pool.acquire() as connection:
            async with connection.transaction():
                user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
                cooldown_info = json.loads(user_account["cooldown"])
                a_datetime = datetime.now()
                formatted_datetime = a_datetime.isoformat()
                cooldown_info[key]=formatted_datetime
                json_datetime = json.dumps(cooldown_info)
                await connection.execute("UPDATE info SET cooldown = $1 WHERE user_id=$2",json_datetime,user.id)

    user_account = await ImportantFunctions.get_user_info(user)
    cooldown_info = json.loads(user_account["cooldown"])
    
    if key in cooldown_info:
        isoformat = cooldown_info[key]            
        elapsed = datetime.now() - datetime.fromisoformat(isoformat)
        seconds_elapsed=int(elapsed.total_seconds())
        retry_after=delay-seconds_elapsed
        
        if retry_after <= 0: #Delay - Time elapsed will give less than 0 if the time elapsed since last command is greater than 0
            print("<0")
            await set_cooldown_to_current(user=user,key=key)
            return True
        else:
            print("false")
            return False

    else:
        print("else")
        await set_cooldown_to_current(user=user,key=key)
        return True

        

    
    