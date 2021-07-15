import os,sys,discord,platform,random,aiohttp,json,time,asyncio,textwrap
from discord.ext import commands,tasks
import utils.awards as awards
import config   
images_dir = "Images/Wheel_of_Fortune"
colour_upvote=0xFF8b60
colour_downvote=0x9494FF
colour_dark_blue=0x021998
colour_green=0x2CFB21
colour_red=0xFF2300
colour_serverperms=0x00FDFF 
colour_yellow=0xFDED00 



    
class Wheel(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1,300, commands.BucketType.user)
    #@commands.is_owner()
    @commands.command(name="Spin",aliases=["stw","wheel"], help=f'Spin the wheel of fortune to get exciting prizes or perhaps a mute or two.\nFormat: `{config.prefix}spin`\nAliases: `stw`,`wheel')
    async def wheel(self,ctx):
        wheel_outcomes=["Nothing","Free_Credits","Free_Karma","Deduct_Karma","Deduct_Credits","Muted","Credits_Boost","Karma_Boost","Server_Perms","Add_Emoji","Mute_Others",]#"Celebrity"
        #random_wheel_outcome=random.choice(wheel_outcomes)
        random_wheel_outcome=random.choices(wheel_outcomes,weights=(15,15,10,10,15,10,10,10,5,5,5,),k=1)[0]
         
        if random_wheel_outcome == "Free_Credits":
            user=ctx.author 
            numbers=list(range(1,200))+list(range(490,500))
            amt=random.choice(numbers)
            
            options=[f"You committed Tax Fraud and got {amt} credits!",f"The mafia decided to give you some dough. You got {amt} credits",f"It's your Birthday! You got {amt} credits.",f"Here is a GET OUT OF JAIL CARD. Collect {amt} as you go."]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune",description=random.choice(options),colour=colour_dark_blue)
            random_picture=random.choice(os.listdir(f"{images_dir}/Free_Credits/")) 
            path=f"{images_dir}/Free_Credits/{random_picture}"
            image = discord.File(path, filename=random_picture)
            embed.set_image(url=f"attachment://{random_picture}")
            await ctx.send(embed=embed,file=image)
           
            ImportantFunctions = self.bot.get_cog('ImportantFunctions')
            await ImportantFunctions.create_account(user)
            await ImportantFunctions.add_credits(user=user,amt=amt)

        elif random_wheel_outcome == "Free_Karma":
            user=ctx.author 
            numbers=list(range(1,20))
            amt=random.choice(numbers)
            
            options=[f"God messed up the balance sheet and you get {amt} Karma!",f"You got free {amt} karma for breathing. Yay!",f"You got {amt} free Karma.",]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune",description=random.choice(options),colour=colour_upvote)
            
            random_picture=random.choice(os.listdir(f"{images_dir}/Free_Karma/")) 
            path=f"{images_dir}/{random_wheel_outcome}/{random_picture}"
            image = discord.File(path, filename=random_picture)
            embed.set_image(url=f"attachment://{random_picture}")
            await ctx.send(embed=embed,file=image)
            
            ImportantFunctions = self.bot.get_cog('ImportantFunctions')
            await ImportantFunctions.create_account(user)
            await ImportantFunctions.add_karma(user=user,amt=amt)
        
        elif random_wheel_outcome == "Deduct_Credits":
            user=ctx.author 
            numbers=list(range(1,200))+list(range(490,500))
            amt=random.choice(numbers)
            
            options=[f"The IRS raided your house. You lost {amt} credits.",f"You lost {amt} credits!",f"You got a GO TO JAIL CARD and paid {amt} credits for bail.",]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune",description=random.choice(options),colour=colour_red)
            random_picture=random.choice(os.listdir(f"{images_dir}/Deduct_Credits/")) 
            path=f"{images_dir}/{random_wheel_outcome}/{random_picture}"
            image = discord.File(path, filename=random_picture)
            embed.set_image(url=f"attachment://{random_picture}")
            await ctx.send(embed=embed,file=image)
            
            ImportantFunctions = self.bot.get_cog('ImportantFunctions')
            await ImportantFunctions.create_account(user)
            await ImportantFunctions.add_credits(user=user,amt=-(amt))
        
        elif random_wheel_outcome == "Deduct_Karma":
            user=ctx.author 
            numbers=list(range(1,20))
            amt=random.choice(numbers)
            
            options=[f"You posted a shit meme and lost {amt} Karma.",f"You lost {amt} Karma for fun.",f"Karma? Who needs that? You lost {amt} karma.",]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune",description=random.choice(options),colour=colour_downvote)
            
            random_picture=random.choice(os.listdir(f"{images_dir}/Deduct_Karma/")) 
            path=f"{images_dir}/{random_wheel_outcome}/{random_picture}"
            image = discord.File(path, filename=random_picture)
            embed.set_image(url=f"attachment://{random_picture}")
            await ctx.send(embed=embed,file=image)
            
            ImportantFunctions = self.bot.get_cog('ImportantFunctions')
            await ImportantFunctions.create_account(user)
            await ImportantFunctions.add_karma(user=user,amt=-(amt))

        elif random_wheel_outcome == "Muted":
            user=ctx.author 
            minutes_to_be_muted=random.choice([1,5,10])
            options=[f"Muted for {minutes_to_be_muted} minutes!"]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune!",description=f"{random.choice(options)}",colour=colour_red)
            
            random_picture=random.choice(os.listdir(f"{images_dir}/Muted/")) 
            path=f"{images_dir}/{random_wheel_outcome}/{random_picture}"
            image = discord.File(path, filename=random_picture)
            embed.set_image(url=f"attachment://{random_picture}")
            await ctx.send(embed=embed,file=image)

            await self.role_management(ctx,user=ctx.author,type="add",role_id=config.wheel_muted_role_id,role_name="Muted (Spin the Wheel)",description="Muted (Spin the Wheel)")
            await asyncio.sleep(int(minutes_to_be_muted*60))
            await self.role_management(ctx,user=ctx.author,type="remove",role_id=config.wheel_muted_role_id,role_name="Muted (Spin the Wheel)",description="Muted (Spin the Wheel)")

        elif random_wheel_outcome == "Server_Perms":
            user=ctx.author 
            options=[f"You get the Manage Server Perms for 10 seconds!\nChange the name, the server icon or even add a bot."]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune!",description=f"{random.choice(options)}",colour=colour_serverperms)
            random_picture=random.choice(os.listdir(f"{images_dir}/Server_Perms/")) 
            path=f"{images_dir}/{random_wheel_outcome}/{random_picture}"
            image = discord.File(path, filename=random_picture)
            embed.set_image(url=f"attachment://{random_picture}")
            await ctx.send(embed=embed,file=image)
            
            await self.role_management(ctx,user=ctx.author,type="add",role_id=config.wheel_server_perms_role_id,role_name="Server Perms Role (Spin the Wheel)",description="Server Perms")
            await asyncio.sleep(int(10))
            await self.role_management(ctx,user=ctx.author,type="remove",role_id=config.wheel_server_perms_role_id,role_name="Server Perms Role (Spin the Wheel)",description="Server Perms")
    
        elif random_wheel_outcome == "Add_Emoji":
            user=ctx.author 
            options=[f"You get to add any one Emoji you want!"]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune",description=random.choice(options),colour=colour_yellow)
            random_picture=random.choice(os.listdir(f"{images_dir}/Add_Emoji/")) 
            path=f"{images_dir}/{random_wheel_outcome}/{random_picture}"
            image = discord.File(path, filename=random_picture)
            embed.set_image(url=f"attachment://{random_picture}")
            role=await self.get_role(ctx,role_id=config.wheel_mod_role_id,role_name="Wheel of Fortune Mod")
            await ctx.send(embed=embed,file=image,content=role.mention)

        elif random_wheel_outcome == "Celebrity":
            user=ctx.author 
            options=[f"Smile you are a celebrity!\nStay high in the Member list for 24 hours!"]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune!",description=f"{random.choice(options)}",colour=colour_serverperms)
            random_picture=random.choice(os.listdir(f"{images_dir}/Celebrity/")) 
            path=f"{images_dir}/{random_wheel_outcome}/{random_picture}"
            image = discord.File(path, filename=random_picture)
            embed.set_image(url=f"attachment://{random_picture}")
            await ctx.send(embed=embed,file=image)
            
            await self.role_management(ctx,user=ctx.author,type="add",role_id=config.wheel_celebrity_role_id,role_name="Celebrity (Spin the Wheel)",description="Celebrity")
            await asyncio.sleep(int(24*60*60))
            await self.role_management(ctx,user=ctx.author,type="remove",role_id=config.wheel_celebrity_role_id,role_name="Celebrity (Spin the Wheel)",description="Celebrity")
       
        elif random_wheel_outcome == "Credits_Boost":
            user=ctx.author 
            options=[f"You get a Credit boost!\nAny Credits you earn or lose in the next one hour are doubled!"]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune!",description=f"{random.choice(options)}",colour=colour_yellow)
            random_picture=random.choice(os.listdir(f"{images_dir}/Credits_Boost/")) 
            path=f"{images_dir}/{random_wheel_outcome}/{random_picture}"
            image = discord.File(path, filename=random_picture)
            embed.set_image(url=f"attachment://{random_picture}")
            await ctx.send(embed=embed,file=image)
            
            await self.role_management(ctx,user=ctx.author,type="add",role_id=config.wheel_credit_boost_role_id,role_name="2x Credits Boost (Spin the Wheel)",description="Credits Boost")
            await asyncio.sleep(int(60*60))
            await self.role_management(ctx,user=ctx.author,type="remove",role_id=config.wheel_credit_boost_role_id,role_name="2x Credits Boost (Spin the Wheel)",description="Credits Boost")

        elif random_wheel_outcome == "Karma_Boost":
            user=ctx.author 
            options=[f"You get a Karma boost!\nAny Karma you earn or lose in the next one hour are doubled!"]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune!",description=f"{random.choice(options)}",colour=colour_red)
            random_picture=random.choice(os.listdir(f"{images_dir}/Karma_Boost/")) 
            path=f"{images_dir}/{random_wheel_outcome}/{random_picture}"
            image = discord.File(path, filename=random_picture)
            embed.set_image(url=f"attachment://{random_picture}")
            await ctx.send(embed=embed,file=image)
            
            await self.role_management(ctx,user=ctx.author,type="add",role_id=config.wheel_karma_boost_role_id,role_name="2x Karma Boost (Spin the Wheel)",description="Karma Boost")
            await asyncio.sleep(int(60*60))
            await self.role_management(ctx,user=ctx.author,type="remove",role_id=config.wheel_karma_boost_role_id,role_name="2x Karma Boost (Spin the Wheel)",description="Karma Boost")
        
        
        elif random_wheel_outcome == "Mute_Others":
            user=ctx.author 
            options=[f"You can mute anyone you want for 30 mins!\nExpect a DM from me or in case you don't allow DM's, too bad."]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune!",description=f"{random.choice(options)}",colour=0xC651FF )
            random_picture=random.choice(os.listdir(f"{images_dir}/Mute_Others/")) 
            path=f"{images_dir}/{random_wheel_outcome}/{random_picture}"
            image = discord.File(path, filename=random_picture)
            embed.set_image(url=f"attachment://{random_picture}")
            await ctx.send(embed=embed,file=image)
            
            embed=discord.Embed(title=f"You get to mute anyone for 5 minutes!",description=f"Reply to this message with the User ID of the person you would like to mute\nIf you are not sure about how to get the User ID:\n```1) Navigate to User Settings\n2) Choose the Advanced Setting\n3) Enable Developer Mode\n4)Right-Click on a user and select Copy ID```\nBe quick about it. This offer expires in 5 minutes.\nYou can't mute Moderators.",colour=colour_serverperms)
            try:
                message = await user.send(embed=embed)
            except:
                return
            async def wait_for_message():
                try:
                    message = await self.bot.wait_for('message', timeout =300,check=lambda m:(ctx.author == m.author and ctx.channel == m.channel) )
                except asyncio.TimeoutError: 
                    embed=discord.Embed(title=f"Oops!",description=f"You took too long and lost this chance. Better luck next time")
                    await ctx.send(embed=embed)            
                else: 
                    try:#This was added so that this doesnt break in case the message doesn't have any text in it.
                        if message.content.lower() in ["quit","exit"]:
                            return
                    except:
                        pass

                    try:
                        user_to_mute=self.bot.get_user(message.content)
                        for role in user_to_mute.roles:
                            if role.id in [config.moderator_role_id,config.admin_role_id]:
                                embed=discord.Embed(title="⚠️ | Can't mute",description="The User ID you entered was of a moderator.\nEnter another User ID or type `quit` to exit.", color =colour_serverperms)
                                await ctx.send(embed=embed)
                                user_to_mute=await wait_for_message()
                                return user_to_mute
                        return user_to_mute
           
                    except:
                        embed=discord.Embed(title="⚠️ | Invalid User",description="The User ID you entered was invalid.\nEnter another User ID or type `quit` to exit.", color =colour_serverperms)
                        await ctx.send(embed=embed)
                        user_to_mute=await wait_for_message()
                        return user_to_mute
                
                user_to_mute=await wait_for_message()
                embed=discord.Embed(title=f"Done!",description=f"{user_to_mute.name} was muted.")
                try:
                    message = await user.send(embed=embed)
                except:
                    pass
                await self.role_management(ctx,user=user_to_mute,type="add",role_id=config.wheel_muted_role_id,role_name="Muted (Spin the Wheel)",description="Muted (Spin the Wheel)")
                await asyncio.sleep(5*60)
                await self.role_management(ctx,user=user_to_mute,type="remove",role_id=config.wheel_muted_role_id,role_name="Muted (Spin the Wheel)",description="Muted (Spin the Wheel)")

        elif random_wheel_outcome == "Nothing":
            user=ctx.author 
            numbers=list(range(1,200))+list(range(400,500))+list(range(2000,2050))
            amt=random.choice(numbers)
            
            options=[f"You win nothing lol.","You get absolutely nothing. Congrats!","Here you go. Have a nothing !"]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune",description=random.choice(options),colour=colour_dark_blue)
            random_picture=random.choice(os.listdir(f"{images_dir}/Nothing/")) 
            path=f"{images_dir}/{random_wheel_outcome}/{random_picture}"
            image = discord.File(path, filename=random_picture)
            embed.set_image(url=f"attachment://{random_picture}")
            await ctx.send(embed=embed,file=image)
        


                
            
           
          


            
            
        
        # elif random_wheel_outcome == "Jail":
        #     user=ctx.author 
        #     options=[f"You go to jail for evading taxes.\n"]
        #     embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune!",description=f"{random.choice(options)}",colour=random.choice(config.embed_colours))
        #     await ctx.send(embed=embed)
        #     role = discord.utils.get(ctx.guild.roles, id=config.wheel_server_perms_role_id)
        #     if role == None:
        #         role = discord.utils.get(ctx.guild.roles, name="Server Perms Role (Spin the Wheel)")
        #         if role == None:
        #             await ctx.send("The Server Perms role was not found.")
        #             return
        #     try: 
        #         await ctx.author.add_roles(role)
        #     except: 
        #         await ctx.send(f"Failed to give manage server perms to {ctx.author.mention}!")

        #     await asyncio.sleep(int(10))
        #     try: 
        #         await ctx.author.remove_roles(role)
        #     except : 
        #         await ctx.send(f"Failed to remove manage server perms for {ctx.author.mention}!")
        else:
            await ctx.send("Invalid choice")
    
    async def get_role(self,ctx,role_id,role_name):
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        if role == None:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role == None:
                await ctx.send(f"The {role_name} role was not found.")
        return role


    async def role_management(self,ctx,user,type,role_id,role_name,description):
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        if role == None:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role == None:
                await ctx.send(f"The {description} role was not found.")
                return
        
        if type =="add":
            try: 
                await user.add_roles(role)
            except: 
                await ctx.send(f"Failed to give the {description} role to {ctx.author.mention}!")

        elif type =="remove":
            try: 
                await user.remove_roles(role)
            except : 
                await ctx.send(f"Failed to remove the {description} role for {ctx.author.mention}!")
        else:
            await ctx.send("Invalid role management type.")
        





    

def setup(bot):
    bot.add_cog(Wheel(bot))