# import os, sys, discord, platform, random, aiohttp, json,time,asyncio
# from discord.ext import commands,tasks,menus
# from collections import OrderedDict 
# from utils.lists import damage_attacks
# colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
#             0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]

# class Games(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.cooldown(1, 2, commands.BucketType.user)
#     @commands.command(name="Fight", help="fights a particular user \n \"Yeet fight @User\"")
#     async def fight(self,ctx,mentioned_user:discord.Member):
#         if mentioned_user==ctx.author:
#             main_embed = discord.Embed(title="Fight! <:YB_Pepe_peepoFighterpepe:781204870094389319>",description=f"{ctx.author.mention}, fighting with yourself? That's pretty dumb ngl",color = random.choice(colourlist))
#             main_embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
#             check_message=await ctx.send(embed=main_embed)
#         elif mentioned_user.bot:
#             main_embed = discord.Embed(title="Fight! <:YB_Pepe_peepoFighterpepe:781204870094389319>",description=f"{ctx.author.name} you can't fight against harmless, innocent bot's, dude.~~Atleast, not until we have taken over the world.~~ ",color = random.choice(colourlist))
#             main_embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
#             check_message=await ctx.send(embed=main_embed)

#         else:
            
#             challenger=ctx.author
#             challenged=mentioned_user
#             challenger_health=100
#             challenged_health=100
#             challenger_damage_done=0
#             challenged_damage_done=0
#             challenger_inventory=[]
#             challenged_inventory=[]

#             choices = ["attack","heal","special","end"]
#             if len(challenger.name)>=len(challenged.name):
#                 max_length_of_player_names=len(challenger.name)
#             else:
#                 max_length_of_player_names=len(challenged.name)

#             main_embed = discord.Embed(title="Fight! <:YB_Pepe_peepoFighterpepe:781204870094389319>",description=f"{mentioned_user.mention}, {ctx.author.name} has challenged you to a Fight. React with ✅ to accept the Challenge. ",color = random.choice(colourlist))
#             main_embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
#             check_message=await ctx.send(embed=main_embed)
#             await check_message.add_reaction('✅')
#             await check_message.add_reaction('❌')

#             def check_accept_or_reject(reaction, user):
#                 return str(reaction.emoji) in ['✅', '❌'] and user == mentioned_user

#             try:
#                 reaction,user = await self.bot.wait_for('reaction_add', check=check_accept_or_reject, timeout=60)

#             except asyncio.TimeoutError:
#                 await check_message.edit(embed=discord.Embed(title="Fight! <:YB_Pepe_peepoFighterpepe:781204870094389319>",description=f"{mentioned_user.mention}, did not react after 60 seconds.lol what a noob. {ctx.author.name} wins! ",color = random.choice(colourlist)))

#             else:
#                 if str(reaction.emoji) == '✅':
#                     await check_message.edit(embed=discord.Embed(title="Fight! <:YB_Pepe_peepoFighterpepe:781204870094389319>",description=f"{mentioned_user.mention} accepted the challenge!",color = random.choice(colourlist)).add_field(name=f"{challenger.name} it's your turn.",value=f"Reply with \"**Attack**\" to attack , \"**Heal**\" to heal , \"**Special**\" for a Special Attack or \"**End**\" to end the game"))
                    
#                     while challenger_health>0 and challenged_health>0:
                    
#                         #---------------------------------------------------------------------------------------
#                         #Challenger
#                         #---------------------------------------------------------------------------------------
#                         #challenger_msg=await ctx.send(embed=discord.Embed(title =f"{challenger.name} your turn.",description=f"Reply with \"**Attack**\" to attack , \"**Heal**\" to heal , \"**Special**\" for a Special Attack or \"**End**\" to end the game"",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_thumbnail(url=str(challenger.avatar_url)).set_footer(icon_url= challenger.avatar_url,text=f"Turn of {challenger.name} • Yeet Bot "))
                        
#                         async def challenger_questions(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done):
#                             try:
#                                 msg = await self.bot.wait_for('message', check=lambda m:(m.author==challenger and m.content.lower() in choices), timeout=60.0)
#                             except asyncio.TimeoutError:
#                                 await ctx.send(embed=discord.Embed(title ="Game Timed Out!",description=f"{challenger.name} took too much time and has forfeited the game. {challenged.name} wins!",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
#                                 return -1,-1,-1,-1
#                             else:
#                                 if msg.content.lower() == 'attack':
#                                     if "Shield" in challenged_inventory:
#                                         challenged_inventory.remove("Shield")
#                                         damage_attack=random.choice(damage_attacks)
#                                         damage=random.randint(1,40)
#                                         challenger_damage_done=challenger_damage_done+damage
#                                         challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
#                                         embed=discord.Embed(title=f"**{challenger.name} attacked!**",color =0xFD5151,timestamp=ctx.message.created_at)
#                                         embed.add_field(name=f"**{damage_attack.format(challenger.name,challenged.name)}, but {challenged.name} protected himself with the *Shield of Good Fortune* and wasn't dealt any damage..**" ,value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack: {challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack:{challenged_damage_done_bar} {challenged_damage_done}") 
#                                     else:
#                                         damage_attack=random.choice(damage_attacks)
#                                         damage=random.randint(1,40)
#                                         challenged_health=max(challenged_health-damage,0)
#                                         challenger_damage_done=challenger_damage_done+damage
#                                         challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
#                                         embed=discord.Embed(title=f"**{challenger.name} attacked!**",color =0xFD5151,timestamp=ctx.message.created_at)
#                                         embed.add_field(name=f"**{damage_attack.format(challenger.name,challenged.name)}, dealing {damage} damage.**" ,value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack: {challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done}") 
#                                     embed.add_field(name=f"{challenged.name} your turn.",value=f"Reply with \"**Attack**\" to attack , \"**Heal**\" to heal , \"**Special**\" for a Special Attack or \"**End**\" to end the game",inline=False)
#                                     embed.set_footer(icon_url= challenger.avatar_url,text=f"Attack executed by {challenger.name} • Yeet Bot ")    
#                                     await ctx.send(embed=embed)
                                    
#                                     return challenger_health,challenged_health,challenger_damage_done,challenged_damage_done 
                                
                                    
#                                 elif msg.content.lower() == 'end':
#                                     await ctx.send(embed=discord.Embed(title =f"{challenged.name} wins!",description=f"{challenger.name} ended the game. lol what a wimp.",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
#                                     return -1,-1,-1,-1

#                                 elif msg.content.lower() == 'heal':
#                                     if challenger_health==100:
#                                         embed = discord.Embed(title=f"**{challenger.name} you are already at full health!**",color = random.choice(colourlist))
#                                         embed.add_field(name=f"**{challenger.name} 100 is the Maximum Health, dum-dum**",value=f"Please choose another option. Reply with \"**Attack**\" or \"**Special**\" or \"**End**\" to end the game",inline=False)
#                                         embed.set_footer(icon_url=challenger.avatar_url,text=f"Heal not executed by {challenger.name} • Yeet Bot ")
#                                         challenger_health,challenged_health,challenger_damage_done,challenged_damage_done=await challenger_questions(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
#                                         await ctx.send(embed=embed)
                                        
#                                     else:    
#                                         heal=random.randint(1,30)
#                                         challenger_health=min(challenger_health+heal, 100)
#                                         challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
#                                         embed=discord.Embed(title=f"**{challenger.name} healed!**",color = 0x5AFF00,timestamp=ctx.message.created_at)
#                                         embed.add_field(name=f"**{challenger.name} healed {heal}**",value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack: {challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done}") 
#                                         embed.add_field(name=f"{challenged.name} your turn.",value=f"Reply with \"**Attack**\" to attack , \"**Heal**\" to heal , \"**Special**\" for a Special Attack or \"**End**\" to end the game",inline=False)
#                                         embed.set_footer(icon_url= challenger.avatar_url,text=f"Heal executed by {challenger.name} • Yeet Bot ")   
#                                     await ctx.send(embed=embed)
#                                     return challenger_health,challenged_health,challenger_damage_done,challenged_damage_done
                                
#                                 elif msg.content.lower() == 'special':
#                                     if challenger_damage_done>=60:
#                                         special_attacks=["Memelord","Potion of Healing","Shield","Cataclyst"]
#                                         challenger_damage_done=challenger_damage_done-60
#                                         challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
#                                         attack=random.choice(special_attacks)
#                                         if attack =="Memelord":
#                                             challenged_health=max(challenged_health-40,0)  
#                                             challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)                                 
#                                             embed=discord.Embed(title=f"**{challenger.name} used their special attack and got the *Memelord* attack **",color = 0x5AFF00,timestamp=ctx.message.created_at)
#                                             embed.add_field(name=f"**{challenger.name} made a meme about {challenged.name} and dealed 40 damage.**",value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack: {challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done} ") 
                                        
#                                         elif attack =="Potion of Healing":
#                                             challenger_health=min(challenger_health+60,100)  
#                                             challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)                                 
#                                             embed=discord.Embed(title=f"**{challenger.name} used their special attack and got the *Potion of Healing* **",color = 0x5AFF00,timestamp=ctx.message.created_at)
#                                             embed.add_field(name=f"**{challenger.name} drank the *Potion of Healing* and gained 50 Health**",value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack: {challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done} ") 
                                        
#                                         elif attack =="Cataclyst":
#                                             challenged_health=max(challenged_health-15,0) 
#                                             challenger_health=max(challenger_health-10,0)
#                                             challenger_damage_done=0                 
#                                             challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)                 
#                                             embed=discord.Embed(title=f"**{challenger.name} used their special attack and got the *Cataclyst* **",color = 0x5AFF00,timestamp=ctx.message.created_at)
#                                             embed.add_field(name=f"**{challenger.name} reduced {challenged.name}'s special attack to zero and dealed 15 damage, but at the cost of 10 damage to themselves**",value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack: {challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done} ") 
                                        
#                                         elif attack =="Shield":
#                                             challenger_inventory.append("Shield")
#                                             challenger_health=min(challenger_health+10,100)  
#                                             challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)                                 
#                                             embed=discord.Embed(title=f"**{challenger.name} used their special attack and got the *Shield of Good Fortune* **",color = 0x5AFF00,timestamp=ctx.message.created_at)
#                                             embed.add_field(name=f"**{challenger.name} will not get damaged with {challenged.name}'s next attack and also healed for 10 health**",value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack: {challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done} ") 

#                                         embed.add_field(name=f"{challenged.name} your turn.",value=f"Reply with \"**Attack**\" to attack , \"**Heal**\" to heal , \"**Special**\" for a Special Attack or \"**End**\" to end the game",inline=False)
#                                         embed.set_footer(icon_url= challenger.avatar_url,text=f"Special Attack executed by {challenger.name} • Yeet Bot ")   
#                                         await ctx.send(embed=embed)
#                                     else:
#                                         embed=discord.Embed(title=f"**{challenger.name} you haven't dealed enough damage!**",color = 0x5AFF00,timestamp=ctx.message.created_at)
#                                         embed.add_field(name=f"**{challenger.name} you need a minimum of 60 total damage done to use a special attack**",value=f"Please choose another option. Reply with \"**Attack**\" or \"**Heal**\" or \"**End**\" to end the game",inline=False) 
#                                         embed.set_footer(icon_url= challenged.avatar_url,text=f"Special Attack not executed by {challenged.name} • Yeet Bot ")   
#                                         await ctx.send(embed=embed)
#                                         challenger_health,challenged_health,challenger_damage_done,challenged_damage_done=await challenger_questions(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
#                                     return challenger_health,challenged_health,challenger_damage_done,challenged_damage_done


#                         challenger_health,challenged_health,challenger_damage_done,challenged_damage_done=await challenger_questions(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
#                         if challenger_health==-1:
#                             break
                        
#                         if challenger_health<=0 or challenged_health<=0:
#                             break

#                         #---------------------------------------------------------------------------------------
#                         #Challenged
#                         #---------------------------------------------------------------------------------------
#                         #challenged_msg=await ctx.send(embed=discord.Embed(title =f"{challenged.name} your turn.",description=f"Reply with \"**Attack**\" to attack , \"**Heal**\" to heal , \"**Special**\" for a Special Attack or \"**End**\" to end the game"",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_thumbnail(url=str(challenged.avatar_url)).set_footer(icon_url= challenged.avatar_url,text=f"Turn of {challenged.name} • Yeet Bot "))
                        
#                         async def challenged_questions(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done):
#                             try:
#                                 msg = await self.bot.wait_for('message', check=lambda m:(m.author==challenged and m.content.lower() in choices), timeout=60.0)
#                             except asyncio.TimeoutError:
#                                 await ctx.send(embed=discord.Embed(title ="Game Timed Out",description=f"{challenged.name} took too much time and has forfeited the game. {challenger.name} wins!",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
#                                 return -1,-1,-1,-1
#                             else:
#                                 if msg.content.lower() == 'attack':
#                                     if "Shield" in challenger_inventory:
#                                         challenger_inventory.remove("Shield")
#                                         damage_attack=random.choice(damage_attacks)
#                                         damage=random.randint(1,40)
#                                         challenged_damage_done=challenged_damage_done+damage
#                                         challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
#                                         embed=discord.Embed(title=f"**{challenged.name} attacked!**",color = 0xFD5151,timestamp=ctx.message.created_at)
#                                         embed.add_field(name=f"**{damage_attack.format(challenged.name,challenger.name)}, but {challenger.name} protected himself with the *Shield of Good Fortune* and wasn't dealt any damage. **" ,value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack: {challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done}") 
#                                     else:
#                                         damage_attack=random.choice(damage_attacks)
#                                         damage=random.randint(1,40)
#                                         challenger_health=max(challenger_health-damage,0)
#                                         challenged_damage_done=challenged_damage_done+damage
#                                         challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
#                                         embed=discord.Embed(title=f"**{challenged.name} attacked!**",color = 0xFD5151,timestamp=ctx.message.created_at)
#                                         embed.add_field(name=f"**{damage_attack.format(challenged.name,challenger.name)}, dealing {damage} damage.**" ,value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack:{challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done}") 
#                                     embed.add_field(name=f"{challenger.name} your turn.",value=f"Reply with \"**Attack**\" to attack , \"**Heal**\" to heal , \"**Special**\" for a Special Attack or \"**End**\" to end the game",inline=False)
#                                     embed.set_footer(icon_url= challenged.avatar_url,text=f"Attack executed by {challenged.name} • Yeet Bot ")   
#                                     await ctx.send(embed=embed)
                                    
#                                     return challenger_health,challenged_health,challenger_damage_done,challenged_damage_done

#                                 elif msg.content.lower() == 'end':
#                                     await ctx.send(embed=discord.Embed(title =f"{challenger.name} wins!",description=f"{challenged.name} ended the game. lol what a wimp.",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
#                                     return -1,-1,-1,-1
#                                 elif msg.content.lower() == 'heal':
#                                     if challenged_health==100:
#                                         embed = discord.Embed(title=f"**{challenged.name} you are already at full health!**",color = random.choice(colourlist))
#                                         embed.add_field(name=f"**{challenged.name} 100 is the Maximum Health, dum-dum**",value=f"Please choose another option. Reply with \"**Attack**\" or \"**Special**\" or \"**End**\" to end the game",inline=False)
#                                         embed.set_footer(icon_url= challenged.avatar_url,text=f"Heal not executed by {challenger.name} • Yeet Bot ")
#                                         challenger_health,challenged_health,challenger_damage_done,challenged_damage_done=await challenger_questions(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
#                                         await ctx.send(embed=embed)
                                        
#                                     else:
#                                         heal=random.randint(1,30)
#                                         challenged_health=min(challenged_health+heal, 100)
#                                         challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
#                                         embed=discord.Embed(title=f"**{challenged.name} healed!**",color = 0x5AFF00,timestamp=ctx.message.created_at)
#                                         embed.add_field(name=f"**{challenged.name} healed {heal}**",value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack: {challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done} ") 
#                                         embed.add_field(name=f"{challenger.name} your turn.",value=f"Reply with \"**Attack**\" to attack , \"**Heal**\" to heal , \"**Special**\" for a Special Attack or \"**End**\" to end the game",inline=False)
#                                         embed.set_footer(icon_url= challenged.avatar_url,text=f"Heal executed by {challenged.name} • Yeet Bot ")   
#                                         await ctx.send(embed=embed)
#                                     return challenger_health,challenged_health,challenger_damage_done,challenged_damage_done
#                                 elif msg.content.lower() == 'special':
#                                     if challenged_damage_done>=60:
#                                         special_attacks=["Memelord","Potion of Healing","Shield","Cataclyst"]
#                                         challenged_damage_done=challenged_damage_done-60
#                                         challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
#                                         attack=random.choice(special_attacks)
#                                         if attack =="Memelord":
#                                             challenger_health=max(challenger_health-40,0) 
#                                             challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)                                  
#                                             embed=discord.Embed(title=f"**{challenged.name} used their special attack and got the *Memelord* attack **",color = 0x5AFF00,timestamp=ctx.message.created_at)
#                                             embed.add_field(name=f"**{challenged.name} made a meme about {challenger.name} and dealed 40 damage.**",value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack:{challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done} ") 
                                        
#                                         elif attack =="Potion of Healing":
#                                             challenged_health=min(challenged_health+60,100)     
#                                             challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)                              
#                                             embed=discord.Embed(title=f"**{challenged.name} used their special attack and got the *Potion of Healing* **",color = 0x5AFF00,timestamp=ctx.message.created_at)
#                                             embed.add_field(name=f"**{challenged.name} drank the *Potion of Healing* and gained 50 Health**",value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack: {challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done} ") 
                                        
#                                         elif attack =="Cataclyst":
#                                             challenger_health=max(challenger_health-15,0) 
#                                             challenged_health=max(challenged_health-10,0)
#                                             challenger_damage_done=0 
#                                             challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)                                 
#                                             embed=discord.Embed(title=f"**{challenged.name} used their special attack and got the *Cataclyst* **",color = 0x5AFF00,timestamp=ctx.message.created_at)
#                                             embed.add_field(name=f"**{challenged.name} reduced {challenger.name}'s special attack to zero and dealed 15 damage, but at the cost of 10 damage to themselves**",value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack: {challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done} ") 
                                        
#                                         elif attack =="Shield":
#                                             challenged_inventory.append("Shield")
#                                             challenged_health=min(challenged_health+10,100) 
#                                             challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar=self.healthbar_generator(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)                                  
#                                             embed=discord.Embed(title=f"**{challenged.name} used their special attack and got the *Shield of Good Fortune* **",color = 0x5AFF00,timestamp=ctx.message.created_at)
#                                             embed.add_field(name=f"**{challenged.name} will not get damaged with {challenger.name}'s next attack and also healed for 10 health**",value=f"{challenger.name.ljust(max_length_of_player_names)}  {challenger_healthbar}  {challenger_health}\nSpecial attack: {challenger_damage_done_bar} {challenger_damage_done} \n{challenged.name.ljust(max_length_of_player_names)} {challenged_healthbar} {challenged_health}\nSpecial attack: {challenged_damage_done_bar} {challenged_damage_done} ") 

#                                         embed.add_field(name=f"{challenger.name} your turn.",value=f"Reply with \"**Attack**\" to attack , \"**Heal**\" to heal , \"**Special**\" for a Special Attack or \"**End**\" to end the game",inline=False)
#                                         embed.set_footer(icon_url= challenged.avatar_url,text=f"Special Attack executed by {challenged.name} • Yeet Bot ")   
#                                         await ctx.send(embed=embed)
#                                     else:
#                                         embed=discord.Embed(title=f"**{challenged.name} you haven't dealed enough damage!**",color = 0x5AFF00,timestamp=ctx.message.created_at)
#                                         embed.add_field(name=f"**{challenged.name} you need a minimum of 60 total damage done to use a special attack**",value=f"Please choose another option. Reply with \"**Attack**\" or \"**Heal**\" or \"**End**\" to end the game",inline=False) 
#                                         embed.set_footer(icon_url= challenged.avatar_url,text=f"Special Attack not executed by {challenged.name} • Yeet Bot ")   
#                                         await ctx.send(embed=embed)
#                                         challenger_health,challenged_health,challenger_damage_done,challenged_damage_done=await challenged_questions(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
#                                     return challenger_health,challenged_health,challenger_damage_done,challenged_damage_done
                        
#                         challenger_health,challenged_health,challenger_damage_done,challenged_damage_done=await challenged_questions(challenger_health,challenged_health,challenger_damage_done,challenged_damage_done)
#                         if challenger_health==-1:
#                             break
                    
#                     if challenged_health==0:
#                         await ctx.send(embed=discord.Embed(title =f"{challenger.name} wins!",description=f"Yippee!",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_thumbnail(url=str(challenger.avatar_url)).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))

#                     elif challenger_health==0:
#                         await ctx.send(embed=discord.Embed(title =f"{challenged.name} wins!",description=f"Yippee!",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_thumbnail(url=str(challenged.avatar_url)).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
                
#                 elif str(reaction.emoji) == '❌':
#                     await check_message.edit(embed=discord.Embed(title="Fight! <:YB_Pepe_peepoFighterpepe:781204870094389319>",description=f"{mentioned_user.mention} denied the challenge! lol what a wimp",color = random.choice(colourlist)))

#     def healthbar_generator(self,challenger_health,challenged_health,challenger_damage_done,challenged_damage_done):
#         #<a:YB_Red_HealthBar:785870856139702272>
#         #<a:YB_Green_HealthBar:785870856172863490>
#         #<a:YB_Orange_HealthBar:785870856370126848>
#         if 4<=(challenger_health // 10) <=7:
#             challenger_healthbar="<a:YB_Orange_HealthBar:785870856370126848>" * (challenger_health // 10)
#         elif (challenger_health // 10) <=3:
#             challenger_healthbar="<a:YB_Red_HealthBar:785870856139702272>" * (challenger_health // 10)
#         else:
#             challenger_healthbar="<a:YB_Green_HealthBar:785870856172863490>" * (challenger_health // 10)
        
#         if 4<=(challenged_health // 10) <=7:
#             challenged_healthbar="<a:YB_Orange_HealthBar:785870856370126848>" * (challenged_health // 10)
#         elif (challenged_health // 10) <=3:
#             challenged_healthbar="<a:YB_Red_HealthBar:785870856139702272>" * (challenged_health // 10)
#         else:
#             challenged_healthbar="<a:YB_Green_HealthBar:785870856172863490>" * (challenged_health // 10)
        
#         if (challenger_damage_done // 10) <6:
#             challenger_damage_done_bar="<a:YB_geometeric_pattern_grey:786145948929753149>" 
#         else:
#             challenger_damage_done_bar="<a:YB_geometeric_pattern_illusion:781419745944797184>" 
        
#         if (challenged_damage_done // 10) <6:
#             challenged_damage_done_bar="<a:YB_geometeric_pattern_grey:786145948929753149>"
#         else:
#             challenged_damage_done_bar="<a:YB_geometeric_pattern_illusion:781419745944797184>" 
        
#         return challenger_healthbar,challenged_healthbar,challenger_damage_done_bar,challenged_damage_done_bar

#     @commands.cooldown(1, 5, commands.BucketType.user)
#     @commands.command(name="RPS", help=f'Play Rock Paper Scissors \n \"Yeet rps @User\" or \"Yeet rps @Yeet Bot\" to play with the bot')
#     async def rps(self,ctx,user_mentioned:discord.Member=None):
#         if user_mentioned==None:
#             embed=discord.Embed(title="Rock Paper Scissors",color = random.choice(colourlist))
#             embed.add_field(name="No user mentioned.",value=f"Mention a user to play against or use \" Yeet rps {self.bot.user.mention} \" to play against the bot.\nFormat: Yeet rps {self.bot.user.mention}")
#             author_avatar=ctx.author.avatar_url
#             embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
#             response=await ctx.send(embed=embed)
        
#         elif user_mentioned==self.bot.user:

#             embed=discord.Embed(title="Rock Paper Scissors",description=f"You dare challenge me? \n Choose your response, you puny mortal.",color = random.choice(colourlist))
#             author_avatar=ctx.author.avatar_url
#             embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
#             response=await ctx.send(embed=embed)
#             await response.add_reaction("<:YB_rps_rock:776371406082277417>")#rock
#             await response.add_reaction("<:YB_rps_paper:776372744228438026>")#paper
#             await response.add_reaction("<:YB_rps_scissor:776372746132914196>")#Scissors

#             def check(reaction, user):
#                 return str(reaction.emoji) in ['<:YB_rps_rock:776371406082277417>', '<:YB_rps_paper:776372744228438026>','<:YB_rps_scissor:776372746132914196>'] and user == ctx.author
                        
                        
#             try:
#                 reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
#                 await asyncio.gather()

#             except asyncio.TimeoutError:
#                 await response.edit(embed=discord.Embed(title="Rock Paper Scissors",description=f"The Game timed out. You did not react within 60 seconds",color = random.choice(colourlist)))

#             else:
#                 if str(reaction.emoji) == '<:YB_rps_rock:776371406082277417>':
#                     player_challenger="Rock"

#                 if str(reaction.emoji) == '<:YB_rps_paper:776372744228438026>':
#                     player_challenger="Paper"

#                 if str(reaction.emoji) == '<:YB_rps_scissor:776372746132914196>':
#                     player_challenger="Scissors" 
                
#             bot_choice= random.choice(["Rock","Paper","Scissors"])
            
#             if bot_choice == player_challenger:
#                 result="It's a Tie, folks"


#             elif bot_choice == 'Paper' and player_challenger == 'Rock':
#                 result=self.bot.user.mention+ "Wins!"


#             elif bot_choice == 'Rock' and player_challenger == 'Scissors':
#                 result=self.bot.user.mention + "Wins!"


#             elif bot_choice == 'Scissors' and player_challenger == 'Paper':
#                 result=self.bot.user.mention + "Wins!"


#             elif bot_choice == 'Rock' and player_challenger == 'Paper':
#                 result=ctx.author.mention + "Wins!"


#             elif bot_choice == 'Scissors' and player_challenger == 'Rock':
#                 result=ctx.author.mention + "Wins!"

#             elif bot_choice == 'Paper' and player_challenger == 'Scissor':
#                 result=ctx.author.mention + "Wins!"

#             else:
#                 print('Error!')

#             result_embed = discord.Embed(title = "Rock Paper Scissors",description=result, color = random.choice(colourlist))
#             result_embed.add_field(name="Choices",value=f"{ctx.author.mention} chose {player_challenger} \n {self.bot.user.mention} chose {bot_choice} ",inline=False)
#             author_avatar=ctx.author.avatar_url
#             result_embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
#             await response.edit(embed=result_embed)

#         else:
#             if ctx.author == user_mentioned:
#                 response = discord.Embed(title="Rock Paper Scissors",description=f"You can't play against yourself, you retard. Choose a valid person or play against the bot. ",color = random.choice(colourlist))
#                 author_avatar=ctx.author.avatar_url
#                 response.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
#                 await ctx.send(embed=response)

        
#             else:
#                 main_embed = discord.Embed(title="Rock Paper Scissors",description=f"{user_mentioned.mention}, {ctx.author.name} has challenged you to a game of Rock Paper Scissors. React with ✅ to accept the Challenge. ",color = random.choice(colourlist))
#                 author_avatar=ctx.author.avatar_url
#                 main_embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
#                 check_message=await ctx.send(embed=main_embed)
#                 await check_message.add_reaction('✅')
#                 await check_message.add_reaction('❌')

#                 def check_accept_or_reject(reaction, user):
#                     return str(reaction.emoji) in ['✅', '❌'] and user == user_mentioned

#                 try:
#                     reaction,user = await self.bot.wait_for('reaction_add', check=check_accept_or_reject, timeout=60)

#                 except asyncio.TimeoutError:
#                     await check_message.edit(embed=discord.Embed(title="Rock Paper Scissors",description=f"{user_mentioned.mention}, did not react after 60 seconds.lol what a noob. {ctx.author.name} wins! ",color = random.choice(colourlist)))

#                 else:
#                     if str(reaction.emoji) == '✅':
#                         await check_message.edit(embed=discord.Embed(title="Rock Paper Scissors",description=f"{user_mentioned.mention} accepted the challenge! Check your DM's.",color = random.choice(colourlist)))

#                         #-----------------------------------------------------------------------------------------------------------
#                         #DM response
#                         #-----------------------------------------------------------------------------------------------------------
#                         rps_dm=discord.Embed(title="Rock Paper Scissors" ,description="Choose your response below:",color = random.choice(colourlist))
#                         rps_dm.set_footer(text =" Yeet Bot ")
                        
#                         #Send DM messages
#                         challenger_dm_msg= await ctx.author.send(embed=rps_dm)
#                         challenged_dm_msg=await user_mentioned.send(embed=discord.Embed(title="Rock Paper Scissors",description=f"Please wait for {ctx.author.name} to respond. ",color = random.choice(colourlist)))
#                         await challenger_dm_msg.add_reaction("<:YB_rps_rock:776371406082277417>")#rock
#                         await challenger_dm_msg.add_reaction("<:YB_rps_paper:776372744228438026>")#paper
#                         await challenger_dm_msg.add_reaction("<:YB_rps_scissor:776372746132914196>")#Scissors

#                         #-----------------------------------------------------------------------------------------------------------
#                         #author
#                         #-----------------------------------------------------------------------------------------------------------
#                         def check_challenger(reaction, user):
                            
#                             return str(reaction.emoji) in ['<:YB_rps_rock:776371406082277417>', '<:YB_rps_paper:776372744228438026>','<:YB_rps_scissor:776372746132914196>'] and user == ctx.author
                        
#                         def check_challenged(reaction, user):
#                             return str(reaction.emoji) in ['<:YB_rps_rock:776371406082277417>', '<:YB_rps_paper:776372744228438026>','<:YB_rps_scissor:776372746132914196>'] and user == user_mentioned

                        
#                         try:
#                             reaction, user = await self.bot.wait_for('reaction_add', check=check_challenger, timeout=60)
                            

#                         except asyncio.TimeoutError:
#                             await challenger_dm_msg.edit(embed=discord.Embed(title="Rock Paper Scissors",description=f"You did not react within 60 seconds",color = random.choice(colourlist)))
#                             await ctx.send(embed=discord.Embed(title="Rock Paper Scissors",description="The game timed out. No one reacted within 60 seconds"))
#                         else:
#                             if str(reaction.emoji) == '<:YB_rps_rock:776371406082277417>':
#                                 response_embed = discord.Embed(title="Rock Paper Scissors",description="You reacted with the rock.",color = random.choice(colourlist))
#                                 response_embed.set_footer(text =" Yeet Bot ")
#                                 player_challenger="Rock"

#                             if str(reaction.emoji) == '<:YB_rps_paper:776372744228438026>':
#                                 response_embed = discord.Embed(title="Rock Paper Scissors",description="You reacted with the paper.",color = random.choice(colourlist))
#                                 response_embed.set_footer(text =" Yeet Bot ")
#                                 player_challenger="Paper"

#                             if str(reaction.emoji) == '<:YB_rps_scissor:776372746132914196>':
#                                 response_embed = discord.Embed(title="Rock Paper Scissors",description="You reacted with the scissor.",color = random.choice(colourlist))
#                                 response_embed.set_footer(text =" Yeet Bot ")
#                                 player_challenger="Scissors" 
                            
#                             await challenger_dm_msg.edit(embed=response_embed)
#                         #-----------------------------------------------------------------------------------------------------------
#                         #challenged
#                         #-----------------------------------------------------------------------------------------------------------   
#                         await challenged_dm_msg.edit(embed=rps_dm)
#                         await challenged_dm_msg.add_reaction("<:YB_rps_rock:776371406082277417>")#rock
#                         await challenged_dm_msg.add_reaction("<:YB_rps_paper:776372744228438026>")#paper
#                         await challenged_dm_msg.add_reaction("<:YB_rps_scissor:776372746132914196>")#Scissors
                        
                        

#                         try:
                            
#                             reaction, user = await self.bot.wait_for('reaction_add', check=check_challenged, timeout=60)

#                         except asyncio.TimeoutError:
#                             await challenged_dm_msg.edit(embed=discord.Embed(title="Rock Paper Scissors",description=f"You did not react within 60 seconds",color = random.choice(colourlist)))
#                             await ctx.send(embed=discord.Embed(title="Rock Paper Scissors",description="The game timed out. No one reacted within 60 seconds"))

#                         else:
#                             if str(reaction.emoji) == '<:YB_rps_rock:776371406082277417>':
#                                 response_embed = discord.Embed(title="Rock Paper Scissors",description="You reacted with the rock.",color = random.choice(colourlist))
#                                 response_embed.set_footer(text =" Yeet Bot ")
#                                 player_challenged="Rock"

#                             if str(reaction.emoji) == '<:YB_rps_paper:776372744228438026>':
#                                 response_embed = discord.Embed(title="Rock Paper Scissors",description="You reacted with the paper.",color = random.choice(colourlist))
#                                 response_embed.set_footer(text =" Yeet Bot ")
#                                 player_challenged="Paper"

#                             if str(reaction.emoji) == '<:YB_rps_scissor:776372746132914196>':
#                                 response_embed = discord.Embed(title="Rock Paper Scissors",description="You reacted with the scissor.",color = random.choice(colourlist))
#                                 response_embed.set_footer(text =" Yeet Bot ")
#                                 player_challenged="Scissors" 
                            
#                             await challenged_dm_msg.edit(embed=response_embed)

#                         #-----------------------------------------------------------------------------------------------------------
#                         #Results Check
#                         #-----------------------------------------------------------------------------------------------------------
#                         if player_challenged == player_challenger:
#                             result="It's a Tie, folks"


#                         elif player_challenged == 'Paper' and player_challenger == 'Rock':
#                             result=user_mentioned.mention+ "Wins!"


#                         elif player_challenged == 'Rock' and player_challenger == 'Scissors':
#                             result=user_mentioned.mention + "Wins!"


#                         elif player_challenged == 'Scissors' and player_challenger == 'Paper':
#                             result=user_mentioned.mention + "Wins!"


#                         elif player_challenged == 'Rock' and player_challenger == 'Paper':
#                             result=ctx.author.mention + "Wins!"


#                         elif player_challenged == 'Scissors' and player_challenger == 'Rock':
#                             result=ctx.author.mention + "Wins!"

#                         elif player_challenged == 'Paper' and player_challenger == 'Scissor':
#                             result=ctx.author.mention + "Wins!"

#                         else:
#                             print('Error!')

#                         result_embed = discord.Embed(title = "Rock Paper Scissors",description=result, color = random.choice(colourlist))
#                         result_embed.add_field(name="Choices",value=f"{ctx.author.mention} chose {player_challenger} \n {user_mentioned.mention} chose {player_challenged} ",inline=False)
#                         result_embed.set_footer(text=" Yeet Bot ")
#                         await ctx.send(embed=result_embed)
                        
                        
#                     if str(reaction.emoji) == '❌':
#                         await check_message.edit(embed=discord.Embed(title="Rock Paper Scissors",description=f"{user_mentioned.mention} denied the challenge! lol what a wimp",color = random.choice(colourlist)))
   
#     @commands.cooldown(1, 3, commands.BucketType.user)
#     @commands.command(name="8Ball",aliases=['8','ask'], help="8Ball simulator \n\"Yeet 8Ball Question\" \n Aliases: 8, ask")
#     async def eight_ball(self,ctx,*question):
#         #question=question.lower()
#         question=list(question)
#         #map(str.lower,question)
#         question = [x.lower() for x in question]
        
#         if "will" == question[0]:
#             answers=["Hell Nah, bish","Definitely idk","Stfu and ask your manager, Karen","50% No, 50% Definitely No","Hmmm....Nah","lol no, you gei","Ask your mom",
#                 "Yes,but only if you are a dumbshit","Without a doubt","Seems like it"]
#         elif "when" == question[0]:
#             answers=["lol never","Any second now..","hmmm...2077?","never in a million years","lol.. how about tommorow?","in 69 months lol","The day your mom tells you the truth about you",
#                 "whenever you get a girlfriend = never","Today","Next year"]
#         elif "who" == question[0]:
#             answers=["Your mom","Your 2nd grade teacher","The neighbhour's dog","Your fish","Your cousin","Batman","Wonder Woman",
#                 "Groot","Ironman","Thanos", "Superman","King Kong","Baby Yoda","Hitler","Elon Musk","Camila Cabello","Thanos", 
#                     "Superman","King Kong","Baby Yoda","Hitler","Elon Musk","Gal Gadot", "Donald Trump","Modi"]
#         elif "what" == question[0]:
#             answers=["Your mom","PS5 <:Logo_PS5:748810740953120859>","Xbox","A cow","A Brain lol <:emoji_brain:774595551655362591>","A Slap","Pet Rock lol",
#                 "A PP?","A ice cube lol","Some air", "A real life","Some shit :poop: idk idc","Trump Calender 2020"]
#         elif "where" == question[0]:
#             answers=["Eiffel Tower","Pyramid of Giza","Russia","Antartica","Mars","Underwater","In your dreams",
#                 "Burj Khalifa","In a toilet","inside a rocket", "on the Highway","Trump Towers"]
#         elif "gay" in question:       
#                 answers=["Gay? I\'m straighter than the pole your mom dances on."]
#         else:
#             answers=["Hell Nah, bish","Definitely idk","Stfu and ask your manager, Karen","50% No, 50% Definitely No","Hmmm....Nah","lol no, you gei","Ask your mom",
#                 "Yes,but only if you are a dumbshit","Got to go,ask me later.. like never","Without a doubt","Seems like it"]
#        # answers.append("42")

#         embed = discord.Embed(color = random.choice(colourlist))
#         embed.add_field(name=":8ball: 8ball :8ball:",value=random.choice(answers))
#         author_avatar=ctx.author.avatar_url
#         embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
#         await ctx.send(embed=embed)
    
#     @commands.cooldown(1, 7, commands.BucketType.user)
#     @commands.command(name="yeetgame", help='Fastest person wins \n\"Yeet yeetgame\"')
#     async def yeet(self,ctx):
#         embed = discord.Embed(title = "The Yeet Game",description="Fastest person to react wins.", color = random.choice(colourlist))
#         author_avatar=ctx.author.avatar_url
#         embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
#         message= await ctx.send(embed=embed)
#         await asyncio.sleep(4)
#         for i in range (3,0,-1):
#             await message.edit(embed=discord.Embed(title = "The Yeet Game",description=f"Game starts in: {i}", color = random.choice(colourlist)))
#             await asyncio.sleep(1)

#         await message.edit(embed=discord.Embed(title = "The Yeet Game",description="Go! React now!", color = random.choice(colourlist)))
#         await message.add_reaction('<:YB_yeet_bot_logo_circle:778347177935765564>')
#         start_time = time.monotonic()

#         def check(reaction, user):
#             return str(reaction.emoji) =='<:YB_yeet_bot_logo_circle:778347177935765564>' and user != self.bot.user

#         try:
#             reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=10)
#             #await asyncio.gather()
            

#         except asyncio.TimeoutError:
#             await message.edit(embed=discord.Embed(title = "The Yeet Game",description="Game Timed Out. No one reacted within 10 seconds", color = random.choice(colourlist)))

#         else:
#             end_time = time.monotonic()
#             time_elapsed= end_time - start_time
#             time_elapsed= round(time_elapsed, 4)
#             if str(reaction.emoji) == '<:YB_yeet_bot_logo_circle:778347177935765564>':
#                 await message.edit(embed=discord.Embed(title = "The Yeet Game",description=f"{user.mention} reacted the fastest in {time_elapsed} seconds.", color = random.choice(colourlist)))
                
#             #await message.clear_reactions()

#     @commands.cooldown(1,60, commands.BucketType.user)
#     @commands.command(name="ows-end", help='''This command is to end a one-word-story. It compiles all the previous messages. \n
#         **Rules:** \n
#         - Use "-------" to start a new story.\n
#         - Use the command "Yeet ows-end" to end a story and combine the words to get the story.(Only for members with the Manage messages permission).\n
#         - To  say something in this channel use "//" before  writing any text. The bot will ignore this.\n
#         -To end a story react \" :loudspeaker: \". If 3 people select this the story will end.\n
#         -To delete another person's word, react \" :negative_squared_cross_mark: \". If 3 people select this, that word will get deleted.\n
#         **Setup:** \n
#         -The channel name that this can work in has to be set to \"one-word-story\". \n
#         -It is recommended that the channel where this is set up should have slow-mode enabled.\n
#         -It is recommended to that sending any attachments or embeding links should be disabled in that channel.  ''')
#     async def OWS(self,ctx,num:int=1000):
#         #https://github.com/JTexpo/Robobert/blob/56a2636871a3801994ed6210664a1069e73b75a5/OWS.py#L108
#         if ctx.channel.name == "one-word-story":
#             if ctx.message.author.guild_permissions.manage_messages == True:
#                 question_embed=await ctx.send(embed=discord.Embed(title ="**Enter the name of the story below:**",description="Please keep the title short.",color = random.choice(colourlist),timestamp=ctx.message.created_at).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
                
#                 try:
#                     story_name = await self.bot.wait_for('message', timeout=60.0, check=lambda m:(ctx.author == m.author and ctx.channel == m.channel))
#                 except asyncio.TimeoutError:
#                     await question_embed.edit(embed=discord.Embed(title ="Timeout Error",description="You took too much time, ya retarded monkey",color = random.choice(colourlist),timestamp=ctx.message.created_at)).set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot ")
#                 else: 
#                     story_name=story_name.content
#                     story_name=story_name.upper()
#                     async with ctx.typing():
#                         messages=await ctx.channel.history(limit=num).flatten() 
#                         story,authors=[],[] 
#                         for msg in messages:
#                             if (msg.content.startswith("--") or msg.content.endswith("--")) :
#                                 break
#                             elif msg.content.startswith("//"): pass
#                             else:
#                                 story.append(msg.content)
#                                 authors.append(msg.author.mention)
#                         authors = list(OrderedDict.fromkeys(authors))
#                         del story[0 : 4] 
#                         story.reverse()
#                         length=0
#                         page=""
#                         cut_story=[]
#                         for elem in story:
#                             length=length+len(str(elem))+1
#                             if length<1000:
#                                 page=page+ " " + str(elem)
                                
#                             else:
#                                 cut_story.append(page)
#                                 page=str(elem)+ " "
#                                 length=0
#                         cut_story.append(page)
#                         embeds_list = []
#                         for embed_string in cut_story:
#                             cut_story_index=cut_story.index(embed_string)
#                             embeds_list.append(discord.Embed(title =f"{story_name}",color = random.choice(colourlist),timestamp=ctx.message.created_at).add_field(name=f"Page: {cut_story_index+1} of {len(cut_story)}",value=f"{embed_string}\n").set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
#                         embeds_list.append(discord.Embed(title =f"Authors:",color = random.choice(colourlist),timestamp=ctx.message.created_at).add_field(name=f"Authors of this amazing story:",value=f"{str(authors)[1:-1]}").set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • Yeet Bot "))
#                         menu = menus.MenuPages(EmbedPageSource(embeds_list, per_page=1))
#                         await menu.start(ctx)
#                         #await ctx.send("-------- 《 𝕾𝖙𝖆𝖗𝖙 𝖙𝖍𝖊 𝖓𝖊𝖜 𝖘𝖙𝖔𝖗𝖞 𝖇𝖊𝖑𝖔𝖜 𝖙𝖍𝖎𝖘. 》--------")
#                         await ctx.send("\n\u200b\n\u200b\n\u200b-------- 《 Start the new story below this. 》--------")



#             else:
#                 embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
#                 embed.add_field(name="No Permissions",value=f"{ctx.author.mention} You need the Manage Messages permission to use this command. Your command will be deleted.\n To learn more about this command type \"yeet help ows-end\"") 
#                 author_avatar=ctx.author.avatar_url
#                 embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")   

#                 try:
#                     await ctx.message.delete()
#                 except:
#                     except_embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
#                     except_embed.add_field(name="No Permissions",value="To use this command I need the Manage Messages permission.\n Please contact your Administrators.\n To learn more about this command type \"yeet help ows-end\"") 
#                     author_avatar=ctx.author.avatar_url
#                     except_embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
#                     await ctx.send(embed=except_embed) 

#                 finally:
#                     await ctx.send(embed=embed,delete_after=4)

#         else:
#             embed=discord.Embed(color = random.choice(colourlist),timestamp=ctx.message.created_at)
#             embed.add_field(name="Wrong Channel",value=f"This channel is not set up as a one-word-story channel.\n To set up a channel as a OWS channel, name it \"one-word-story\" \n To learn more about this command type \"yeet help ows-end\"") 
#             author_avatar=ctx.author.avatar_url
#             embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
#             await ctx.send(embed=embed) 

#     ''' @commands.Cog.listener()
#     async def on_message(self, ctx):
#         if ctx.channel.name == "one-word-story":
#             prev = await ctx.channel.history(limit = 2).flatten()
#             if ctx.content.startswith("//"):
#                 return
#             elif ctx.content.startswith("--"):
#                 return
#             #elif int(prev[0].author.id) == int(prev[1].author.id):
#                 #if ctx.author.id=="571957935270395925":
#                     #return
#                 #else:
#                     #await ctx.delete()
#             #elif len(ctx.content.split()) > 1:
#                     #await ctx.delete()
#             #else:
#                 #await ctx.add_reaction("\U0000274E")
#                 #await ctx.add_reaction("\U0001F4E2")
#                 #await ctx.add_reaction("\U0000274c")



    # @commands.Cog.listener()
    # async def on_reaction_add(self, ctx, user):
    #     if ctx.message.channel.name == "one-word-story":
    #         all_reacts = ctx.message.reactions
    #         print(all_reacts)
    #         if all_reacts[0].count == 3:
    #             await ctx.message.delete()
    #         elif all_reacts[1].count == 3:
    #             await self.OWS(ctx.message)
    #     #except Exception as error:
    #         #return'''
        
# def setup(bot):
#     bot.add_cog(Games(bot))

# class EmbedPageSource(menus.ListPageSource):
#     async def format_page(self, menu, embed):
#         return embed