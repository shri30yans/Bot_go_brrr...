import core.checks as checks
import json,asyncio,random,os,discord
import utils.awards as awards
import utils.badges as badges
from discord.ext import commands
import config



colourlist=config.embed_colours

class Economy(commands.Cog,name="Economy",description="Economy functions"): 
    def __init__(self, bot):
        self.bot = bot
        self.messages_count_dict={}
        

    @commands.cooldown(1,10, commands.BucketType.user)
    @commands.command(name="Stats",aliases=["account","bal","acc","balance","karma","credits","profile"], help=f"Shows the Karma, Credits and Awards of a user")
    async def bal(self,ctx,user:discord.Member=None):
        user = user or ctx.author
        sent_msg = await ctx.reply(embed=discord.Embed(title=f"{config.loading_reaction}    {user.name}'s Balance",description=f"Fetching {user.name}'s inventory from the database...",colour = random.choice(colourlist)))
        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        await UserDatabaseFunctions.check_if_badges_need_to_be_given(user)
        
        if user.bot:
            await ctx.reply(f"{user.name} is a bot. Bots don't have accounts.")
        else:
            user_account=await UserDatabaseFunctions.get_user_info(user)
            embed=discord.Embed(title=f"{user.name}'s Balance",colour = random.choice(colourlist))
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
    @commands.command(name="Awards",aliases=["awardlist"], help=f"Shows list of all the awards with their description, cost and other details")
    async def award_list(self,ctx):
        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        user=ctx.author
        credits=await UserDatabaseFunctions.get_user_credits(user)
        embed=discord.Embed(title=f"Awards",description=f"Your balance: **{credits} Credits**")

        for award in list(awards.awards_list.values()):
            embed.add_field(name=f"{award.reaction_id} {award.name} ",value=f"{'{:,}'.format(award.cost)} credits \n {award.description} \n",inline=False)

        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await ctx.reply(embed=embed)

    @commands.cooldown(1,30, commands.BucketType.user)
    @commands.command(name="Badges",aliases=["badge,badgelist"], help=f"Shows list of all the badges with their description, cost and other details.")
    async def badge_list(self,ctx):
        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        user=ctx.author
        credits=await UserDatabaseFunctions.get_user_credits(user)
        embed=discord.Embed(title=f"Badges",description=f"Your balance: **{credits} Credits**")

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

    
    @commands.guild_only()
    @commands.cooldown(1,5, commands.BucketType.user)
    @commands.command(name="Award", help=f'Award a post')
    async def award(self,ctx,message:discord.Message=None):
        user_giving = ctx.author
        try:
            #This will only work if the command has been invoked
            await ctx.message.delete()

            if ctx.message.reference is None and message is None:
                embed = discord.Embed(title="Award",colour = random.choice(colourlist))
                embed.add_field(name="You didn't mention a message.",value="To award a post:\n   - React with `🏆` to a message\n   - Use this command as a reply to the post you would like to award",)
                await ctx.send(content= user_giving.mention,embed = embed,delete_after=5)
                return
            
            elif ctx.message.reference:
                channel = self.bot.get_channel(ctx.message.reference.channel_id)
                message = await channel.fetch_message(ctx.message.reference.message_id)
        
        except:
            pass

        
        user_recieving=message.author

        if user_recieving.bot:
            embed = discord.Embed(title="Award",description=f"{user_giving.mention} you can't award bots.",colour = random.choice(colourlist))
            await ctx.send(content= user_giving.mention,embed = embed,delete_after=5)
            return
        if user_recieving == user_giving:
            embed = discord.Embed(title="Award",description = f"{user_giving.mention} you can't award yourself.",colour = random.choice(colourlist))
            await ctx.send(content= user_giving.mention,embed = embed,delete_after=5)
            return
        
       
        embed = discord.Embed(title=f"Award",colour = random.choice(colourlist))
        embed.add_field(name=f"{user_giving.name} react with the award you would like to give {user_recieving.name}",value=f"An award **cannot** be revoked once given. This action is irreversible.\nChoose a reaction if you would like to award this [post]({message.jump_url}).\n Select `❌` if you would like to cancel the award.")
        award_message = await ctx.channel.send(embed = embed)
        
        award_reaction_ids=[]
        for award in list(awards.awards_list.values()):
            await award_message.add_reaction(award.reaction_id)
            award_reaction_ids.append(award.reaction_id)
        await award_message.add_reaction('❌')
        
        def check_if_award(award_reaction,award_user):
            return (str(award_reaction.emoji) in award_reaction_ids or str(award_reaction.emoji) in ['❌']) and user_giving == award_user

        try:
            award_reaction,award_user = await self.bot.wait_for('reaction_add',check=check_if_award, timeout=60)#pylint: disable=unused-argument 
            #disables the confirm_user unusesd argument error

        except asyncio.TimeoutError:
            await award_message.delete()

        else:
            if str(award_reaction) in ['❌']:
                await award_message.delete()


            else:
                #It is an Award Reaction
                ImportantFunctions = self.bot.get_cog('ImportantFunctions')
                UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')

                award = await ImportantFunctions.fetch_award(str(award_reaction.emoji))
                embed = discord.Embed(title=f"{message.author.name} received a {award.name} Award!",description=f"{user_giving.mention} liked {message.author.mention}'s [post]({message.jump_url}) so much that they gave it the {award.name} award.",color = 0xFFD700)
                embed.set_thumbnail(url=str(award_reaction.emoji.url))
                embed.set_footer(icon_url= user_giving.avatar_url,text=f"Given by {user_giving.name} • {self.bot.user.name} ")
                
                await award_message.clear_reactions()
                await award_message.edit(embed=embed)

                #post to starboard 
                #has a check to see if Award posts to starboard                                  
                #await ImportantFunctions.post_to_starboard(message=message,channel=channel,user=user_giving,emoji=award_reaction.emoji,reaction_name=award.name,reaction_type="add")
                await UserDatabaseFunctions.add_karma(user=user_recieving,amt=award.karma_given_to_receiver)
                await UserDatabaseFunctions.add_karma(user=user_giving,amt=award.karma_given_to_giver)
                
                await UserDatabaseFunctions.add_credits(user=user_giving,amt = -award.cost)
                await UserDatabaseFunctions.add_credits(user=user_recieving,amt = award.credits_given_to_receiver)

                await UserDatabaseFunctions.add_awards(user_recieving=user_recieving,user_giving=user_giving,award_name=award.name)

    
    #@commands.cooldown(1,10, commands.BucketType.user)
    @commands.command(name="Buy", help='Buy a badge')
    async def buy_badge(self,ctx,*,item_name):
        user=ctx.author 
        
        async def check_if_item_exists(item_name):
            for x in list(badges.badges_list.values()):
                if x.name.lower().replace(" ","") == item_name.lower().replace(" ",""):
                    return x
            else:
                return 
        
        item= await check_if_item_exists(item_name)
        
        if item:
            if item.cost is not None:
                UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
                credits = await UserDatabaseFunctions.get_user_credits(user)
                if credits < item.cost:
                    await ctx.reply(f"You don't have enough credits to buy `{item.name}`.")
                else:
                    await UserDatabaseFunctions.add_credits(user,-item.cost)
                    check = await UserDatabaseFunctions.edit_badges(badge_name=item.name,user=user,action="add")
                    if check:    
                        await ctx.reply(content=f"You paid {item.cost} credits and bought `{item.name}`.")    
                    else:
                        await ctx.reply(content=f"You already have the item `{item.name}`.")
            else:
                await ctx.reply(f"The item `{item.name}` cannot be bought.")

        else:
            await ctx.reply(f"The item `{item_name}` does not exist.")


    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(name="Beg", help='Beg for cash')
    async def beg(self,ctx):
        '''Gives the user a little credits'''

        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        user=ctx.author 
        options=["credits","nothing"]
        choice=random.choices(options,weights=(80,20),k=1)[0]
        if choice == "credits":
            amt = random.randint(1,20)
            beg_options=[f"Someone gave you {amt} credits.",f"Awh you begging? Take {amt} credits.",f"You begged and got {amt} credits.",f"Lmao sad guy. Take {amt} credits."]
            await ctx.reply(random.choice(beg_options))
            await UserDatabaseFunctions.add_credits(user=user,amt=amt)
        elif choice == "nothing":
            beg_options=[f"no",f"*\"Sorry no money for you.\"*",f"imagine begging lol","Even your comrades said no","Nah I gave away all my money","credit.exe cannot afford your begging","donate.exe has stopped working","I ain't made of money. go away","You know how people say they got your back? Well I don't. Go away."]
            await ctx.reply(random.choice(beg_options))


    
    @commands.cooldown(1,600, commands.BucketType.user)
    @commands.command(name="Rob",aliases=["steal"], help='Rob other\'s credits')
    async def rob(self,ctx,user_robbed:discord.Member):
        '''Rob another user for upto 18% of their inventory
            If the robbery fails the theif pays money'''

        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        user_robbing=ctx.author
       
        if user_robbed.bot:
            await ctx.reply(f"You can't rob from bots. lol")
            ctx.command.reset_cooldown(ctx)
        
        elif user_robbed.id == user_robbing.id:
            await ctx.reply("Robbing yourself? huh you must be a some different kind of nuts.")
            ctx.command.reset_cooldown(ctx)
        
        else:

            user_robbing_credits = await UserDatabaseFunctions.get_user_credits(user=user_robbing)
            user_robbed_credits = await UserDatabaseFunctions.get_user_credits(user=user_robbed)
            
            user_robbing_credits_required = 500
            user_robbed_credits_required = 750
            
            if user_robbing_credits < user_robbing_credits_required:
                await ctx.reply(f"You need at least {user_robbing_credits_required} credits to rob others.")
                ctx.command.reset_cooldown(ctx)
       
            elif user_robbed_credits < user_robbed_credits_required:
                await ctx.reply(f"Leave the poor folk alone. They have less than {user_robbed_credits_required} credits. sad guy")
                ctx.command.reset_cooldown(ctx)
            else:
                has_not_been_robbed_in_last_10_seconds=await checks.get_last_robbed_from(ctx,user=user_robbed,delay=600)
                if has_not_been_robbed_in_last_10_seconds:
                    options=["fail","caught","nothing","smallloot","loot","bigloot","biggestloot"]
                    choice=random.choices(options,weights=(30,20,30,15,10,5,1),k=1)[0]
                    if choice =="fail":
                        amt = int(random.randint(100,300))
                        await UserDatabaseFunctions.give(user_giving=user_robbing,user_taking=user_robbed,amt=amt)
                        await ctx.reply(f"You failed lmao. You lost {amt} credits to {user_robbed.name}.") 
                    
                    elif choice == "caught":
                        percentage=random.choice(list(range(3,5))+ list([10])) /100
                        amt = int(percentage * user_robbing_credits)
                        await UserDatabaseFunctions.give(user_giving=user_robbing,user_taking=user_robbed,amt=amt)
                        await ctx.reply(f"You got caught lmao. You paid {user_robbed.name} **{amt}** credits. ded xd") 

                    elif choice == "nothing":
                        options = [f"lol you got nothing. ggwp"]
                        await ctx.reply(random.choice(options)) 

                    elif choice == "smallloot":
                        percentage=random.choice(list(range(1,2)))/100
                        amt = int(percentage * user_robbing_credits) 
                        await UserDatabaseFunctions.give(user_giving=user_robbed,user_taking=user_robbing,amt=amt)
                    
                    elif choice == "loot":
                        percentage=random.choice(list(range(2,3)) + list(range(4,5)))/100
                        amt = int(percentage * user_robbing_credits)
                        await UserDatabaseFunctions.give(user_giving=user_robbed,user_taking=user_robbing,amt=amt)
                        await ctx.reply(f"{user_robbing.name} stole **{amt} credits** from {user_robbed.name}. Nice!") 
                    
                    elif choice == "bigloot":
                        percentage=random.choice(list(range(5,8)) + list(range(10,12))) /100
                        amt = int(percentage * user_robbing_credits)
                        await UserDatabaseFunctions.give(user_giving=user_robbed,user_taking=user_robbing,amt=amt)
                        await ctx.reply(f"**BLING BLING!**{user_robbing.name} stole **{amt} credits** from {user_robbed.name}. GG!") 
                    
                    elif choice == "biggestloot":
                        percentage=random.choice(list(range(8,12)) + list(range(15,18))) /100
                        amt = int(percentage * user_robbing_credits)
                        await UserDatabaseFunctions.give(user_giving=user_robbed,user_taking=user_robbing,amt=amt)
                        await ctx.reply(f"**WHOA YOU HIT THE JACKPOT**{user_robbing.name} stole **{amt} credits** from {user_robbed.name}. {int(percentage*100)}% of their whole credits. Just insane.") 

            
                else:
                    await ctx.reply(f"{user_robbed.name} has been robbed in the past 10 minutes. Give it a rest.") 
                    ctx.command.reset_cooldown(ctx)
    
    @commands.cooldown(1,300, commands.BucketType.user)
    @commands.command(name="Spin",aliases=["stw","wheel"], help=f'Spin the wheel of fortune to get free karma or maybe even lose a couple of hundred credits.')
    async def wheel(self,ctx):
        '''Spin the Wheel of Fortume for a chance to get free credits and karma'''
        wheel_outcomes=["Nothing","Free_Credits","Free_Karma","Deduct_Karma","Deduct_Credits","Credits_Boost","Karma_Boost"]
        random_wheel_outcome=random.choices(wheel_outcomes,weights=(20,15,15,15,15,10,10),k=1)[0]

        async def get_image_url(key):
            images_list= config.spin_the_wheel_images[key]
            image_url = random.choice(images_list)
            return image_url
         
        if random_wheel_outcome == "Free_Credits":
            user=ctx.author 
            numbers=list(range(1,200))+list(range(490,500))
            amt=random.choice(numbers)
            
            options=[f"You committed Tax Fraud and got {amt} credits!",f"The mafia decided to give you some dough. You got {amt} credits",f"It's your Birthday! You got {amt} credits.",f"Here is a GET OUT OF JAIL CARD. Collect {amt} as you go."]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune",description=random.choice(options),colour=random.choice(colourlist))
            random_picture= await get_image_url(random_wheel_outcome)
            embed.set_image(url=random_picture)
            await ctx.reply(embed=embed)
           
            UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
            await UserDatabaseFunctions.add_credits(user=user,amt=amt)

        elif random_wheel_outcome == "Free_Karma":
            user=ctx.author 
            numbers=list(range(1,20))
            amt=random.choice(numbers)
            
            options=[f"God messed up the balance sheet and you get {amt} Karma!",f"You got free {amt} karma for breathing. Yay!",f"You got {amt} free Karma.",]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune",description=random.choice(options),colour=random.choice(colourlist))
            
            random_picture= await get_image_url(random_wheel_outcome)
            embed.set_image(url=random_picture)
            await ctx.reply(embed=embed)
            
            UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
            await UserDatabaseFunctions.add_karma(user=user,amt=amt)
        
        elif random_wheel_outcome == "Deduct_Credits":
            user=ctx.author 
            numbers=list(range(1,200))+list(range(490,500))
            amt=random.choice(numbers)
            
            options=[f"The IRS raided your house. You lost {amt} credits.",f"You lost {amt} credits!",f"You got a GO TO JAIL CARD and paid {amt} credits for bail.",]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune",description=random.choice(options),colour=random.choice(colourlist))
            
            random_picture= await get_image_url(random_wheel_outcome)
            embed.set_image(url=random_picture)
            await ctx.reply(embed=embed)
            
            UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
            await UserDatabaseFunctions.add_credits(user=user,amt=-(amt))
        
        elif random_wheel_outcome == "Deduct_Karma":
            user=ctx.author 
            numbers=list(range(1,20))
            amt=random.choice(numbers)
            
            options=[f"You posted a shit meme and lost {amt} Karma.",f"You lost {amt} Karma for fun.",f"Karma? Who needs that? You lost {amt} karma.",]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune",description=random.choice(options),colour=random.choice(colourlist))
            
            random_picture= await get_image_url(random_wheel_outcome)
            embed.set_image(url=random_picture)
            await ctx.reply(embed=embed)
            
            UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
            await UserDatabaseFunctions.add_karma(user=user,amt=-(amt))
       
        elif random_wheel_outcome == "Credits_Boost":
            user=ctx.author 
            options=[f"You get a Credit boost!\nAny Credits you earn in the next 30 minutes are doubled!"]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune!",description=f"{random.choice(options)}",colour=random.choice(colourlist))
            random_picture= await get_image_url(random_wheel_outcome)
            embed.set_image(url=random_picture)
            await ctx.reply(embed=embed)
            
            UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
            await UserDatabaseFunctions.edit_badges(user=user,badge_name="Double Credits Badge",action="add")
            await asyncio.sleep(int(60*30))
            await UserDatabaseFunctions.edit_badges(user=user,badge_name="Double Credits Badge",action="remove")

        elif random_wheel_outcome == "Karma_Boost":
            user=ctx.author 
            options=[f"You get a Karma boost!\nAny Karma you earn in the next 30 minutes are doubled!"]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune!",description=f"{random.choice(options)}",colour=random.choice(colourlist))
            random_picture= await get_image_url(random_wheel_outcome)
            embed.set_image(url=random_picture)
            await ctx.reply(embed=embed)
            
            UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
            await UserDatabaseFunctions.edit_badges(user=user,badge_name="Double Karma Badge",action="add")
            await asyncio.sleep(int(60*30))
            await UserDatabaseFunctions.edit_badges(user=user,badge_name="Double Karma Badge",action="remove")
        
        elif random_wheel_outcome == "Nothing":
            user=ctx.author 
            numbers=list(range(1,200))+list(range(400,500))+list(range(2000,2050))
            amt=random.choice(numbers)
            
            options=[f"You win nothing lol.","You get absolutely nothing. Congrats!","Here you go. Have a nothing !"]
            embed=discord.Embed(title=f"{ctx.author.name} has spinned the Wheel of Fortune",description=random.choice(options),colour=random.choice(colourlist))
            random_picture= await get_image_url(random_wheel_outcome)
            embed.set_image(url=random_picture)
            await ctx.reply(embed=embed)
        

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
    

 
    

    @commands.cooldown(1,30, commands.BucketType.user)
    @commands.command(name="Give",aliases=["pay"], help='Give your credits to others. Boost badges are not applicable for this command')
    async def give(self,ctx,user_mentioned:discord.Member,amt:str):
        '''Allows a user to give their money to another person'''
        user=ctx.author
        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        credits = await UserDatabaseFunctions.get_user_credits(user)

        try:
            amt=int(amt)
        except:
            if amt.lower() == "all":
                amt=credits

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
                raise discord.errors.InvalidArgument()
        
        if amt<=0:
            await ctx.reply(f"You can't give zero or negative credits, dum-dum")
            ctx.command.reset_cooldown(ctx)
        
        elif user == user_mentioned:
            await ctx.reply(f"You can't give yourself the credits dum dum")
            ctx.command.reset_cooldown(ctx)
        
        elif user_mentioned.bot:
            await ctx.reply(f"Bots don't have accounts dum dum.")
            ctx.command.reset_cooldown(ctx)
        
        elif amt > credits:
            await ctx.reply(f"You can't give what you don't have.")
            ctx.command.reset_cooldown(ctx)
        
        
        else:
            await UserDatabaseFunctions.give(user_giving=user,user_taking=user_mentioned,amt=amt,boost_check=False)
            await ctx.reply(f"{user.name} gave {user_mentioned.name}, **{amt} credits**.")     

    @checks.CustomCooldown(key="last_daily_command",delay=24*60*60)
    @commands.command(name="Daily", help='Get some bonus coins everyday.')
    async def daily_credits(self,ctx):
        '''Daily check in reward'''
        user=ctx.author
        amt = 50
        await ctx.reply(f"**{amt} credits** were added to your account.")   
        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        await UserDatabaseFunctions.add_credits(user=user,amt=amt)
    
    @checks.CustomCooldown(key="last_weekly_command",delay=24*60*60*7)
    @commands.command(name="Weekly", help='Get some bonus coins every week.')
    async def weekly_credits(self,ctx):
        '''Weekly check in reward'''
        user=ctx.author
        amt = 500
        await ctx.reply(f"**{amt} credits** were added to your account.")   
        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        await UserDatabaseFunctions.add_credits(user=user,amt=amt)
    
    @checks.CustomCooldown(key="last_monthly_command",delay=24*60*60*30)
    @commands.command(name="Monthly", help='Get some bonus coins every month.')
    async def monthly_credits(self,ctx):
        '''Monthly check in reward'''
        user=ctx.author
        amt = 2000
        await ctx.reply(f"**{amt} credits** were added to your account.")   
        UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
        await UserDatabaseFunctions.add_credits(user=user,amt=amt)
    

    @commands.guild_only()
    @commands.group(name="Leaderboard",aliases=["lb","lboard"],help=f"Shows the server leaderboard",case_insensitive=True,invoke_without_command=True)   
    async def leaderboard(self,ctx,page:int=1):
        await self.karma_leaderboard(ctx,page)
 
    @leaderboard.command(name="Credits",aliases=["credit","creds","cred"],help=f"Shows the server leaderboard according to the credits.")
    async def credits_leaderboard(self,ctx,page:int=1,globallb=False):
        sent_msg = await ctx.reply(embed=discord.Embed(title=f"{config.loading_reaction}   Server Leaderboard",description=f"Fetching the server leaderboard...",colour = random.choice(colourlist)))
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
        
        embed=discord.Embed(title=f"Credits Leaderboard",description=f"{top_string}",colour = random.choice(colourlist))
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await sent_msg.edit(embed=embed)

    @leaderboard.command(name="Karma",help=f"Shows the server leaderboard according to the karma.")
    async def karma_leaderboard(self,ctx,page:int=1):
        sent_msg = await ctx.reply(embed=discord.Embed(title=f"{config.loading_reaction}   Server Leaderboard",description=f"Fetching the server leaderboard...",colour = random.choice(colourlist)))
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
        
        embed=discord.Embed(title=f"Karma Leaderboard",description=f"{top_string}",colour = random.choice(colourlist))
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await sent_msg.edit(embed=embed)

    
    
    @commands.guild_only()
    @commands.group(name="GlobalLeaderboard",aliases=["glb","gleaderboard","glboard"],help=f"Shows the global leaderboard",case_insensitive=True,invoke_without_command=True)   
    async def gloablleaderboard(self,ctx,page:int=1):
        await self.karma_globalleaderboard(ctx,page)

    
    @gloablleaderboard.command(name="Credits",aliases=["credit","creds","cred"],help=f"Shows the global leaderboard according to the credits.")
    async def credits_globalleaderboard(self,ctx,page:int=1):
        sent_msg = await ctx.reply(embed=discord.Embed(title=f"{config.loading_reaction}   Global Leaderboard",description=f"Fetching the server leaderboard...",colour = random.choice(colourlist)))
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
        
        embed=discord.Embed(title=f"Credits Global Leaderboard",description=f"{top_string}",colour=random.choice(colourlist))
        embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
        await sent_msg.edit(embed=embed)

    @gloablleaderboard.command(name="Karma",help=f"Shows the global leaderboard according to the karma.\nFormat: `{config.default_prefixes[0]}GlobalLeaderboard karma`")
    async def karma_globalleaderboard(self,ctx,page:int=1):
        sent_msg = await ctx.reply(embed=discord.Embed(title=f"{config.loading_reaction}   Global Leaderboard",description=f"Fetching the server leaderboard...",colour = random.choice(colourlist)))
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
        
        embed=discord.Embed(title=f"Karma Global Leaderboard",description=f"{top_string}",colour = random.choice(colourlist))
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

  
   


def setup(bot):
    bot.add_cog(Economy(bot))
        