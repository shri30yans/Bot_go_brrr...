from discord.errors import InvalidArgument
import utils.checks as checks
import json
import random
import config
import discord
import utils.awards as awards
import utils.badges as badges
from discord.ext import commands

colourlist=config.embed_colours

class Economy(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        self.messages_count_dict={}
        

    @commands.cooldown(1,20, commands.BucketType.user)
    @commands.command(name="Stats",aliases=["account","bal","acc","balance","karma","credits","profile"], help=f"Shows the Karma, Credits and Awards of a user\nFormat: `{config.prefix}stats'\nAliases: `Account`, `Bal`, `Acc`, `Balance`, `Karma`, `Credits`, `Stats`, `Profile`")
    async def bal(self,ctx,user:discord.Member=None):
        user = user or ctx.author
        sent_msg = await ctx.reply(embed=discord.Embed(title=f"{config.loading_reaction}    {user.name}'s Balance",description=f"Fetching {user.name}'s inventory from the database..."))
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        await ImportantFunctions.check_if_badges_need_to_be_given(user)
        if user.bot:
            await ctx.reply(f"{user.name} is a bot. Bots don't have accounts.")
        else:
            user_account=await ImportantFunctions.get_user_info(user)
            embed=discord.Embed(title=f"{user.name}'s Balance")
            badges = await self.format_in_order(to_format=json.loads(user_account["badges"])["badges"],type="badge")
            embed.add_field(name="Badges:",value=f"{badges}",inline=False)
            embed.add_field(name="Balance:",value=f"{'{:,}'.format(user_account['credits'])} Credits",inline=True)
            embed.add_field(name="Karma:",value=f"{'{:,}'.format(user_account['karma'])} Karma",inline=True)

            awards_given,total_awards_given = await self.format_in_order(to_format=json.loads(user_account["awards_given"]),type="award")
            awards_received,total_awards_received = await self.format_in_order(to_format=json.loads(user_account["awards_received"]),type="award")

            awards_given = awards_given or "None"
            awards_received = awards_received or "None"

            embed.add_field(name="Awards given:",value=f"{awards_given}\nTotal awards given: {total_awards_given}",inline=False)
            embed.add_field(name="Awards received:",value=f"{awards_received}\nTotal awards received: {total_awards_received}",inline=False)
            # embed.add_field(name="Upvotes given:",value=f"{user_account['karma']} Karma")
            # embed.add_field(name="Upvotes received:",value=f"{user_account['karma']} Karma")                                             
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
            await sent_msg.edit(embed=embed)

    async def format_in_order(self,to_format,type:str):
        async def format_awards_in_order(self,awards_dict):
            #formats the awards in order of cost
            ImportantFunctions = self.bot.get_cog('ImportantFunctions')
            ordered_reactions_of_post={}
            for x in list(awards.awards_list.values())[::-1]:
                try:
                    ordered_reactions_of_post[x.name.lower()] = awards_dict[x.name]
                except:
                    pass                
                
            total_awards=0        
            reaction_id_string=""
            for r in ordered_reactions_of_post:
                award = await ImportantFunctions.fetch_award(award_name_or_id=r)
                count=ordered_reactions_of_post[r]
                total_awards+=count
                if award.animated_reaction_id:
                    reaction_id = award.animated_reaction_id
                else:
                    reaction_id = award.reaction_id
                reaction_id_string = reaction_id_string + f"{count} {reaction_id} ,   "
            return reaction_id_string,total_awards

        async def format_badges_in_order(self,badges_list):
            #formats the awards in order of cost
            #ImportantFunctions = self.bot.get_cog('ImportantFunctions')
            if len(badges_list) > 0:
                all_badges = list(badges.badges_list.values())[::-1]
                ordered_reactions_of_post = list(badges.badges_list.values())[::-1]  
                for x in all_badges:
                    if x.name not in badges_list :
                        ordered_reactions_of_post.remove(x)             
                        
                reaction_id_string=""
                for b in ordered_reactions_of_post:
                    reaction_id_string = reaction_id_string + f"{b.reaction_id}   "

                return reaction_id_string
            else:
                return "None"
        
        if type == "award":
            return (await format_awards_in_order(self,awards_dict=to_format))
        
        elif type == "badge":
            return(await format_badges_in_order(self,badges_list=to_format))
            
        
    @commands.cooldown(1,30, commands.BucketType.user)
    @commands.command(name="Awards",aliases=["award,awardlist"], help=f"Shows list of all the awards with their description, cost and other details\nFormat: `?awards'\nAliases: `awardlist`, `award`")
    async def award_list(self,ctx):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        user=ctx.author
        user_account=await ImportantFunctions.get_user_info(user)
        embed=discord.Embed(title=f"Awards",description=f"Your balance: **{user_account['credits']} Credits**")

        for award in list(awards.awards_list.values()):
            embed.add_field(name=f"{award.reaction_id} {award.name} ",value=f"{'{:,}'.format(award.cost)} credits \n {award.description} \n",inline=False)

        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await ctx.reply(embed=embed)

    @commands.cooldown(1,30, commands.BucketType.user)
    @commands.command(name="Badges",aliases=["badge,badgelist"], help=f"Shows list of all the badges with their description, cost and other details\nFormat: `?badges'\nAliases: `badges`, `badgelist`")
    async def badge_list(self,ctx):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        user=ctx.author
        user_account=await ImportantFunctions.get_user_info(user)
        embed=discord.Embed(title=f"Badges",description=f"Your balance: **{user_account['credits']} Credits**")

        embed.add_field(name="**Credits based**",value="**These badges can be bought in exchange of credits.**")
        for badge in list(badges.badges_list.values()):
            if badge.cost is not None:
                embed.add_field(name=f"{badge.reaction_id} {badge.name} ",value=f"{'{:,}'.format(badge.cost)} credits \n {badge.description} \n",inline=False)
        
        embed.add_field(name="**Karma based**",value="**These badges are earned when you reach a certain karma.**")
        for badge in list(badges.badges_list.values()):
            if badge.karma_required is not None:
                embed.add_field(name=f"{badge.reaction_id} {badge.name} ",value=f"{badge.karma_required} karma \n {badge.description} \n",inline=False)
        
        embed.add_field(name="**Special**",value="**These badges can only be earned through special methods.**")
        for badge in list(badges.badges_list.values()):
            if badge.karma_required is None and badge.cost is None:
                embed.add_field(name=f"{badge.reaction_id} {badge.name} ",value=f"{badge.description} \n",inline=False)

        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await ctx.reply(embed=embed)

    
    
    #@commands.cooldown(1,10, commands.BucketType.user)
    @commands.command(name="Buy", help='Buy a badge\nFormat: `?buy item_name`')
    async def buy_badge(self,ctx,*,item_name):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        user=ctx.author 
        await ImportantFunctions.create_account(user)
        
        async def check_if_item_exists(item_name):
            for x in list(badges.badges_list.values()):
                if x.name.lower().replace(" ","") == item_name.lower().replace(" ",""):
                    return x
            else:
                return 
        
        item= await check_if_item_exists(item_name)
        
        if item:
            if item.cost is not None:
                user_account=await ImportantFunctions.get_user_info(user)
                if user_account["credits"] < item.cost:
                    await ctx.reply(f"You don't have enough credits to buy `{item.name}`.")
                else:
                    await ImportantFunctions.add_credits(user,-item.cost)
                    check = await ImportantFunctions.edit_badges(badge_name=item.name,user=user,action="add")
                    if check:    
                        await ctx.reply(content=f"You paid {item.cost} credits and bought `{item.name}`.")    
                    else:
                        await ctx.reply(content=f"You already have the item `{item.name}`.")
            else:
                await ctx.reply(f"The item `{item.name}` cannot be bought.")

        else:
            await ctx.reply(f"The item `{item_name}` does not exist.")


    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(name="Beg", help='Beg for cash\nFormat: `?beg`')
    async def beg(self,ctx):
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        user=ctx.author 
        options=["credits","nothing"]
        choice=random.choices(options,weights=(80,20),k=1)[0]
        if choice == "credits":
            amt = random.randint(1,20)
            beg_options=[f"Someone gave you {amt} credits.",f"Awh you begging? Take {amt} credits.",f"You begged and got {amt} credits.",f"Lmao sad guy. Take {amt} credits."]
            await ctx.reply(random.choice(beg_options))
            await ImportantFunctions.add_credits(user=ctx.message.author,amt=amt)
        elif choice == "nothing":
            beg_options=[f"no",f"*\"Sorry no money for you.\"*",f"imagine begging lol","Even your comrades said no","Nah I gave away all my money","credit.exe cannot afford your begging","donate.exe has stopped working","I ain't made of money. go away","You know how people say they got your back? Well I don't. Go away."]
            await ctx.reply(random.choice(beg_options))


    
    @commands.cooldown(1,600, commands.BucketType.user)
    @commands.command(name="Rob",aliases=["steal"], help='Rob other\'s credits\nFormat: `?rob @User`\nAlias: `steal`"')
    async def rob(self,ctx,user_robbed:discord.Member):

        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        user_robbing=ctx.author
        try:# this only fails if any of the users is a bot
            user_robbing_info= await ImportantFunctions.get_user_info(user=user_robbing)
            user_robbed_info= await ImportantFunctions.get_user_info(user=user_robbed)
        except:
            pass

        user_robbing_credits_required = 500
        user_robbed_credits_required = 750
        
        if user_robbed.bot:
            await ctx.reply(f"You can't rob from bots. lol")
            ctx.command.reset_cooldown(ctx)
        
        elif user_robbed.id == user_robbing.id:
            await ctx.reply("Robbing yourself? huh you must be a some different kind of nuts.")
            ctx.command.reset_cooldown(ctx)
        
        elif user_robbing_info["credits"] < user_robbing_credits_required:
            await ctx.reply(f"You need at least {user_robbing_credits_required} credits to rob others.")
            ctx.command.reset_cooldown(ctx)
       
        elif user_robbed_info["credits"] < user_robbed_credits_required:
            await ctx.reply(f"leave the poor folk alone. They have less than {user_robbed_credits_required} credits. sad guy")
            ctx.command.reset_cooldown(ctx)
        else:
            has_not_been_robbed_in_last_10_seconds=await checks.get_last_robbed_from(ctx,user=user_robbed,delay=600)
            if has_not_been_robbed_in_last_10_seconds:
                options=["fail","caught","success","nothing"]
                choice=random.choices(options,weights=(30,20,35,20),k=1)[0]
                if choice =="fail":
                    amt = int(random.randint(100,300))
                    await ImportantFunctions.add_credits(user=user_robbing,amt=-amt)    
                    await ctx.reply(f"You failed lmao. You lost {amt} credits.") 
                
                elif choice == "caught":
                    percentage=random.choice(list(range(1,5))+ list(10)) /100
                    amt = percentage * user_robbing_info["credits"]
                    await ImportantFunctions.add_credits(user=user_robbing,amt=-amt)    
                    await ctx.reply(f"You got caught lmao. You paid {user_robbed.display_name} **{amt}** credits. ded xd") 


                elif choice == "success":
                    percentage=random.choice(list(range(2,8)) + list(range(10,12))) /100
                    amt = int(percentage * user_robbing_info["credits"])
                    await ImportantFunctions.add_credits(user=user_robbed,amt=-amt)   
                    await ImportantFunctions.add_credits(user=user_robbing,amt=amt)  
                    await ctx.reply(f"{user_robbing.display_name} stole **{amt} credits** from {user_robbed.display_name}. {int(percentage*100)}% of their credits. Just insane.") 

                elif choice == "nothing":
                    options = [f"lol you got nothing. ggwp"]
                    await ctx.reply(random.choice(options)) 
            
            else:
                await ctx.reply(f"{user_robbed.display_name} has been robbed in the past 10 minutes. Give it a rest.") 
                ctx.command.reset_cooldown(ctx)


        


            

    # @commands.cooldown(1,20, commands.BucketType.user)
    # @commands.command(name="Gamble", help='Gamble away your money')
    # async def gamble(self,ctx,amt:str):
    #     ImportantFunctions = self.bot.get_cog('ImportantFunctions')
    #     user=ctx.author
    #     async with self.bot.pool.acquire() as connection:
    #         async with connection.transaction():
    #             await ImportantFunctions.create_account(user)
    #             user_account = await connection.fetchrow("SELECT * FROM info WHERE user_id=$1",user.id)
    #             if amt.lower() == "all":
    #                 amt = user_account["credits"]
    #             try:
    #                 amt=int(amt)
    #             except:
    #                 await ctx.send(f"{amt} is not a valid number. Please use \"all\" or a valid number.")
    #                 return
    #             if amt <= 0:
    #                 await ctx.send(f"You can't gamble away zero or negative credits, dum-dum")
    #             elif amt < 50:
    #                 await ctx.send(f"Minimum Stakes is 50 credits.")
    #             else:
    #                 if amt > user_account["credits"]:
    #                     await ctx.send("You can't gamble away what you don't have.")
    #                     return
    #                 else:
    #                     choice=random.choice(["lose","win"])
    #                     earnings=random.randint(0,20)
    #                     if choice=="lose":
    #                         total_earned=-(round(amt*(earnings/100)))
    #                         bal=user_account["credits"]+total_earned
    #                         await ctx.send(f"You gambled away {amt} and got {total_earned} credits with an {earnings}% decrease. New balance is {bal} credits ")
    #                     elif choice=="win":
    #                         total_earned=round(amt*(earnings/100))
    #                         bal=user_account["credits"]+total_earned
    #                         await ctx.send(f"You gambled away {amt} and earned {total_earned} credits with an {earnings}% increase. New balance is {bal} credits ")
    #                     else:
    #                         await ctx.send("error")
                        
    #                     await ImportantFunctions.add_credits(user=user,amt=total_earned)
    

    @checks.CustomCooldown(key="last_daily_command",delay=24*60*60)
    @commands.command(name="Daily", help='Get some bonus coins everyday.\nFormat: `?Daily`')
    async def daily_credits(self,ctx):
        user=ctx.author
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        amt = 50
        await ctx.reply(f"**{amt} credits** were added to your account.")   
        await ImportantFunctions.add_credits(user=user,amt=amt) 
    
    @checks.CustomCooldown(key="last_weekly_command",delay=24*60*60*7)
    @commands.command(name="Weekly", help='Get some bonus coins every week.\nFormat: `?Weekly`')
    async def weekly_credits(self,ctx):
        user=ctx.author
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        amt = 500
        await ctx.reply(f"**{amt} credits** were added to your account.")   
        await ImportantFunctions.add_credits(user=user,amt=amt)
    
    @checks.CustomCooldown(key="last_monthly_command",delay=24*60*60*30)
    @commands.command(name="Monthly", help='Get some bonus coins every month.\nFormat: `?Monthly`')
    async def monthly_credits(self,ctx):
        user=ctx.author
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        amt = 2000
        await ctx.reply(f"**{amt} credits** were added to your account.")   
        await ImportantFunctions.add_credits(user=user,amt=amt)
    
    

    @commands.cooldown(1,30, commands.BucketType.user)
    @commands.command(name="Give",aliases=["pay"], help='Give your credits to others\nFormat: `?Give @user amount_to_give`\nAlias: `pay`')
    async def give(self,ctx,user_mentioned:discord.Member,amt:str):
        user=ctx.author
        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
        user_account = await ImportantFunctions.get_user_info(user)
        await ImportantFunctions.create_account(user_mentioned)

        try:
            amt=int(amt)
        except:
            if amt.lower() == "all":
                amt=user_account["credits"]

            elif any(letter in amt.lower() for letter in ["k","m","b"]):
                def convert_str_to_number(x):
                    x = x.replace(',','')
                    num = 0
                    num_map = {'K':1000, 'M':1000000, 'B':1000000000}
                    if x.isdigit():
                        num = int(x)
                    else:
                        if len(x) > 1:
                            num = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
                    return int(num)
                amt=convert_str_to_number(amt)
            
            else:
                raise InvalidArgument()

        #badge = await ImportantFunctions.check_if_has_badge(user=user_mentioned,badge_name="Double Credits Badge")
        
        if amt<=0:
            await ctx.reply(f"You can't give zero or negative credits, dum-dum")
            ctx.command.reset_cooldown(ctx)
        
        elif user == user_mentioned:
            await ctx.reply(f"You can't give yourself the credits dum dum")
            ctx.command.reset_cooldown(ctx)
        
        elif user_mentioned.bot:
            await ctx.reply(f"Bots don't have accounts dum dum.")
            ctx.command.reset_cooldown(ctx)
        
        elif amt > user_account["credits"]:
            await ctx.reply(f"You can't give what you don't have.")
            ctx.command.reset_cooldown(ctx)
        
        #checks if the person you are giving it to has a boost role.
        elif await ImportantFunctions.check_if_has_badge(user=user_mentioned,badge_name="Double Credits Badge"):
            await ctx.reply(f"The person you are giving the credits to has a Boosted badge. Try again later.")
            ctx.command.reset_cooldown(ctx)
        
        else:
            await ImportantFunctions.add_credits(user=user,amt=-amt)   
            await ImportantFunctions.add_credits(user=user_mentioned,amt=amt)  
            await ctx.reply(f"{user.mention} gave {user_mentioned.mention}, **{amt} credits**.")     

    @commands.guild_only()
    @commands.group(name="Leaderboard",aliases=["lb","lboard"],help=f"Shows the server leaderboard\nFormat: `{config.prefix}Leaderboard subcommand`\nSubcommands: `Karma`, `Credits`\nAliases: `lb`, `lboard`",case_insensitive=True,invoke_without_command=True)   
    async def leaderboard(self,ctx,page:int=1):
        await self.karma_leaderboard(ctx,page)
 
    @leaderboard.command(name="Credits",aliases=["credit","creds","cred"],help=f"Shows the server leaderboard according to the credits.\nFormat: `{config.prefix}Leaderboard credits`\nAliases: `credit`, `creds`, `cred`")
    async def credits_leaderboard(self,ctx,page:int=1,globallb=False):
        sent_msg = await ctx.reply(embed=discord.Embed(title=f"{config.loading_reaction}   Server Leaderboard",description=f"Fetching the server leaderboard..."))
        formated_list = await self.get_leaderboard("credits")
        top=formated_list[page*10-10:page*10]
        top_string=""
        for entry in top:
            num = formated_list.index(entry)+1
            user = ctx.guild.get_member(entry["user_id"])
            if user or globallb:
                top_string = top_string + f"`{num}.` " + f" {user.mention} • `{entry['credits']} Credits `" + "\n"

        
        if len(top_string) == 0:#is space/blank/None
            top_string = "There are no entries in your leaderboard."
        
        embed=discord.Embed(title=f"Credits Leaderboard",colour=random.choice(colourlist),description=f"{top_string}")
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await sent_msg.edit(embed=embed)

    @leaderboard.command(name="Karma",help=f"Shows the server leaderboard according to the karma.\nFormat: `{config.prefix}Leaderboard karma`")
    async def karma_leaderboard(self,ctx,page:int=1):
        sent_msg = await ctx.reply(embed=discord.Embed(title=f"{config.loading_reaction}   Server Leaderboard",description=f"Fetching the server leaderboard..."))
        formated_list = await self.get_leaderboard("karma")
        top=formated_list[page*10-10:page*10]
        top_string=""
        for entry in top:
            num = formated_list.index(entry)+1
            user = ctx.guild.get_member(entry["user_id"])
            if user:
                top_string = top_string + f"`{num}.` " + f" {user.mention} • `{entry['karma']} Karma `" + "\n"
        
        if len(top_string) == 0 :
            top_string = "There are no entries in your leaderboard"
        
        embed=discord.Embed(title=f"Karma Leaderboard",colour=random.choice(colourlist),description=f"{top_string}")
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await sent_msg.edit(embed=embed)

    
    
    @commands.guild_only()
    @commands.group(name="GlobalLeaderboard",aliases=["glb","gleaderboard","glboard"],help=f"Shows the global leaderboard\nFormat: `{config.prefix}Leaderboard subcommand`\nSubcommands: `Karma`, `Credits`\nAliases: `glb`, `glboard`, `gleaderboard`",case_insensitive=True,invoke_without_command=True)   
    async def gloablleaderboard(self,ctx,page:int=1):
        await self.karma_globalleaderboard(ctx,page)

    
    @gloablleaderboard.command(name="Credits",aliases=["credit","creds","cred"],help=f"Shows the global leaderboard according to the credits.\nFormat: `{config.prefix}GlobalLeaderboard credits`\nAliases: `credit`, `creds`, `cred`")
    async def credits_globalleaderboard(self,ctx,page:int=1):
        sent_msg = await ctx.reply(embed=discord.Embed(title=f"{config.loading_reaction}   Server Leaderboard",description=f"Fetching the server leaderboard..."))
        top = await self.get_leaderboard("credits",offset=page*10-10)
        top_string=""
        for entry in top:
            num=top.index(entry)+1
            try:
                user = await self.bot.get_user(entry["user_id"])
                top_string = top_string + f"`{num}.` " + f" {user.mention} • `{entry['credits']} Credits `" + "\n"
            except:
                user = await self.bot.fetch_user(entry["user_id"])
                top_string = top_string + f"`{num}.` " + f" {user.mention} • `{entry['credits']} Credits `" + "\n"
        
        if len(top_string) == 0:#is space/blank/None
            top_string = "There are no entries in your leaderboard."
        
        embed=discord.Embed(title=f"Credits Global Leaderboard",colour=random.choice(colourlist),description=f"{top_string}")
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await sent_msg.edit(embed=embed)

    @gloablleaderboard.command(name="Karma",help=f"Shows the global leaderboard according to the karma.\nFormat: `{config.prefix}GlobalLeaderboard karma`")
    async def karma_globalleaderboard(self,ctx,page:int=1):
        sent_msg = await ctx.reply(embed=discord.Embed(title=f"{config.loading_reaction}   Server Leaderboard",description=f"Fetching the server leaderboard..."))
        top = await self.get_leaderboard("karma",offset=page*10-10)
        top_string=""
        for entry in top:
            try:
                num=top.index(entry)+1
                user = await self.bot.bot_user(entry["user_id"])
                top_string = top_string + f"`{num}.` " + f" {user.mention} • `{entry['karma']} Karma `" + "\n"
            except:
                user = await self.bot.fetch_user(entry["user_id"])
                top_string = top_string + f"`{num}.` " + f" {user.mention} • `{entry['karma']} Karma `" + "\n"
        
        if len(top_string) == 0 :
            top_string = "There are no entries in your leaderboard"
        
        embed=discord.Embed(title=f"Karma Global Leaderboard",colour=random.choice(colourlist),description=f"{top_string}")
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await sent_msg.edit(embed=embed)


    async def get_leaderboard(self,column,offset=None):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                if offset is not None: #if we know how many entries we want
                    if column == "credits":
                        all_rows = await connection.fetch("SELECT user_id, credits FROM info ORDER BY credits DESC LIMIT 10 OFFSET $1",offset)
                    elif column== "karma":
                        all_rows = await connection.fetch("SELECT user_id, karma FROM info ORDER BY karma DESC LIMIT 10 OFFSET $1",offset)
                    return all_rows
                else:
                    if column == "credits":
                        all_rows = await connection.fetch("SELECT user_id, credits FROM info ORDER BY credits DESC")
                    elif column== "karma":
                        all_rows = await connection.fetch("SELECT user_id, karma FROM info ORDER BY karma DESC")
                    return all_rows

   #For adding credits for chatting in #main_chat
    @commands.Cog.listener(name="on_message")
    async def add_credits_for_sending_messages(self,message):
        if message.guild.id in config.APPROVED_SERVERS:#if that server is approved/that server has the settings
            user=message.author
            if user.bot:
                return
            if message.channel.id != config.main_chat_id:
                return
            messages = await message.channel.history(limit=5).flatten() 
            #if previous message is also written by same person
            count=0
            for msg in messages:
                if msg.author == message.author:
                    count += 1
            if count >= 3:
                return

            else:    
                if str(user.id) in self.messages_count_dict:
                    if self.messages_count_dict[str(user.id)] >= 5:
                        self.messages_count_dict[str(user.id)] = 0 #reset messages
                        #Add credits
                        ImportantFunctions = self.bot.get_cog('ImportantFunctions')
                        amt=5
                        await ImportantFunctions.create_account(user)
                        await ImportantFunctions.add_credits(user=user,amt=amt)
                    
                    else:
                        self.messages_count_dict[str(user.id)] += 1
                    
                else:
                    self.messages_count_dict[str(user.id)] = 1
            
   


def setup(bot):
    bot.add_cog(Economy(bot))
        