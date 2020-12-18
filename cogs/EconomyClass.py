import os, sys, discord, platform, random, aiohttp, json,time,asyncio
from discord.ext import commands,tasks
from discord.ext.commands import Greedy
from discord.ext.commands.cooldowns import BucketType
import asyncpg

colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
            0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Balance",aliases=["bal"], help='Balance of a user')
    async def bal(self,ctx,user:discord.Member=None):
        user=user or ctx.author

    # retrieve an individual connection from our pool, defined later
        async with self.bot.pool.acquire() as connection:
        # create a transaction for that connection
            async with connection.transaction():

            # actually execute the query. Notice the sanitization using $1.
            # Further values would be $2,$3... and be passed in the tuple.
                balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                if balance==None:
                    await connection.execute("INSERT INTO rpgdatabase (user_id,coins,xp) VALUES ($1,0,0)",user.id)
                    balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id) 
                
                balance=dict(balance)
                coins_amt=balance["coins"]
                xp_amt=balance["xp"]
                embed=discord.Embed(Title=f"{ctx.author.name}'s balance")
                embed.add_field(name="Coins:",value=f"{coins_amt} ")
                embed.add_field(name="XP:",value=f"{xp_amt} ")
                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed)


            # also see: conn.cursor, conn.fetch, conn.fetchrow, etc.


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Beg", help='Balance of a user')
    async def beg(self,ctx):
        user=ctx.author
        earnings=random.randint(1,100)
      
        async with self.bot.pool.acquire() as connection:
        # create a transaction for that connection
            async with connection.transaction():
                balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                await connection.execute("UPDATE rpgdatabase SET coins = $1 WHERE user_id=$2",balance["coins"]+earnings,ctx.author.id)
                await ctx.send(f"Someone gave you {earnings} coins")
        
    '''@commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Deposit",aliases=["dep"], help='Deposit all coinss stuff in xp')
    async def deposit(self,ctx,amt:int):
        user=ctx.author
        if amt<=0:
            await ctx.send(f"You can't withdraw zero or negative coins, dum-dum")
        else:        
            async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
                async with connection.transaction():
                    balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                    if amt > balance["coins"]:
                        await ctx.send(f"You can't deposit what you don't have.")
                    else:
                        await connection.execute("UPDATE rpgdatabase SET coins = $1 WHERE user_id=$2",balance["coins"]-amt,str(ctx.author.id))
                        await connection.execute("UPDATE rpgdatabase SET xp = $1 WHERE user_id=$2",balance["xp"]+amt,str(ctx.author.id))
                        await ctx.send(f"You transfered {amt} coins into your xp")
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Withdraw",aliases=["wth"], help='Deposit all coinss stuff in xp')
    async def withdraw(self,ctx,amt:int):
        user=ctx.author
        if amt<=0:
            await ctx.send(f"You can't withdraw zero or negative coins, dum-dum")
        else:
            async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
                async with connection.transaction():
                    balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                    if amt > balance["xp"]:
                        await ctx.send(f"You can't withdraw what you don't have.")
                    else:
                        await connection.execute("UPDATE rpgdatabase SET coins = $1 WHERE user_id=$2",balance["coins"]+amt,str(ctx.author.id))
                        await connection.execute("UPDATE rpgdatabase SET xp = $1 WHERE user_id=$2",balance["xp"]-amt,str(ctx.author.id))
                        await ctx.send(f"You withdrawed {amt} coins into your coins")'''
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Give", help='Deposit all coinss stuff in xp')
    async def give(self,ctx,user_mentioned:discord.Member,amt:int):
        user=ctx.author

        if amt<=0:
            await ctx.send(f"You can't give zero or negative coins, dum-dum")
        else:
            async with self.bot.pool.acquire() as connection:
            # create a transaction for that connection
                async with connection.transaction():
                    user_balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                    user_mentioned_balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user_mentioned.id)
                    if amt > user_balance["coins"]:
                        await ctx.send(f"You can't give what you don't have.")
                    else:
                        await self.create_account(user,user_balance)
                        await self.create_account(user_mentioned,user_mentioned_balance)
                        await connection.execute("UPDATE rpgdatabase SET coins = $1 WHERE user_id=$2",user_balance["coins"]-amt,user.id)
                        await connection.execute("UPDATE rpgdatabase SET coins = $1 WHERE user_id=$2",user_mentioned_balance["coins"]+amt,user_mentioned.id)
                        await ctx.send(f"You gave {user_mentioned.name}, {amt} coins.")
    
    '''@commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="Inventory", help='Inventory of a user')
    async def inventory(self,ctx,user:discord.Member=None):
        user=user or ctx.author
        async with self.bot.pool.acquire() as connection:
        # create a transaction for that connection
            async with connection.transaction():
                balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                #inventory = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id)
                balance,xp
                
                
                balance=dict(balance)
                coins_amt=balance["coins"]
                xp_amt=balance["xp"]
                inventory_items=inventory

                embed=discord.Embed(Title=f"{ctx.author.name}'s balance")
                embed.add_field(name="coins:",value=f"{coins_amt} ")
                embed.add_field(name="xp:",value=f"{xp_amt} ")
                embed.add_field(name="Inventory:",value=f"{inventory_items} ")
                embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed)'''

    async def create_account(self,user,balance,xp=1):
        if balance==None or xp==None :
            async with self.bot.pool.acquire() as connection:
        # create a transaction for that connection
                async with connection.transaction():
                    await connection.execute("INSERT INTO rpgdatabase (user_id,coins,xp) VALUES ($1,0,0)",user.id)
                    await connection.execute("INSERT INTO rpgdatabase (user_id) VALUES ($1)",user.id)
                    balance = await connection.fetchrow("SELECT * FROM rpgdatabase WHERE user_id=$1",user.id) 


    '''user=ctx.author
        user=await self.bot.pg_con.fetch("SELECT * FROM rpgdatabase WHERE user_id==$1",user.id)
        if not user:#equivalent to if user==[] empty list
            await self.bot.pg_con.execute("INSERT INTO rpgdatabase (user_id,coins,xp,inventory) VALUES (ctx.author.id,0,0,[])",user.id)
            user=await self.bot.pg_con.fetchrow("SELECT * FROM rpgdatabase WHERE user_id==$1",ctx.author.id)'''

            
    '''await self.new_account(ctx,user)
        users=await self.get_xp_data()
        coins_amt=users[user.id]["coins"]
        xp_amt=users[user.id]["xp"]
        embed=discord.Embed(Title=f"{ctx.author.name}'s balance")
        embed.add_field(name="coins:",value=f"{coins_amt} ")
        embed.add_field(name="xp:",value=f"{xp_amt} ")
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)'''
    
    
    


    '''async def new_account(self,ctx,user):
        #user=ctx.author
        with open("rpgdatabase.json","r") as f:
            users=json.load(f)

        if user.id in users:
            return False
        else:
            users[user.id]= {}
            users[user.id]["coins"]=0
            users[user.id]["xp"]=0
            users[user.id]["inventory"]=[]
        with open("rpgdatabase.json","w") as f:
            json.dump(users,f)
        return True
    
    async def get_xp_data(self):
        with open("rpgdatabase.json","r") as f:
            users=json.load(f)
        return(users)'''
    
    

    

def setup(bot):
    bot.add_cog(Economy(bot))