
# @client.command()
# async def apply(ctx, parameters):
#   thankyou_application=f'''{ctx.author.mention}**Thank you for Applying!**

# `We will contact you when you are accepted!`'''

#   application_log_channel=client.get_channel(875569220648316968)

#   warn = '''**Before taking the quiz challenge:**

# *Note that Type our answers in a single message.*'''

#   programmer=['Can you script in python? If so, rate from 1-10 how good you are at python.', 'Do you have any experience in programming, nuking, or raiding in Discord?', 'Write a python script that auto join a Discord account when the the username and password is inputed. Show me proof. Hint: import requests and maybe urllib. (Points will be deducted if there is an error.)', 'Write a python script that sends a message to a Discord webhook. Show me video proof.', 'Do you know how to use Google Form, Google Sheets, Google Slide, Google Doc, and the corresponding APIs for them? List them here.']

#   antiscam_police=['Do you swear not to abuse your power?', 'What would you do if someone (a friend of the owner) started being rude to you (or others) / tried to raid the server?', 'Do you know how to stop a raid or nuke?', 'What if Heromaex(admin) starts to abuse his power and kick/ban everyone, what would you do?', 'If someone were to ask you for a special role, what would you do?', 'If someone try to bribe you in order to have mod access to the server, what would you do?']

#   assignment_manager=['Are you loyal to the group? If so, prove it.', 'What will you do as an Assignment Manager?', 'What experiences do you have as a leader?', 'Do you know anything about Discord raiding and nuking?', 'What if someone tries to bribe you to gain access to the server? What would you do?', 'Do you know how to use Google Form, Google Sheets, Google Slide, and Google Doc?']
#   if ctx.message.channel.id == 875355578317275206:
#     if parameters.lower() == 'info':
#       apply_embed=discord.Embed(title='Apply Commands', description='Pick whatever rank you wish to apply for and run its commands, you will be challenged with a quiz to see if you pass or not. Goodluck!', color=0x2ecc71)
#       apply_embed.add_field(name='Assignment Manager', value='Type in the following command: `.apply am`', inline=True)
#       apply_embed.add_field(name='Anti-Scam Police', value='Type in the following command: `.apply asp`', inline=True)
#       apply_embed.add_field(name='Programmer', value='Type in the following command: `.apply p`', inline=True)
#       apply_embed.set_footer()
#       await ctx.send(embed=apply_embed)
#     elif parameters.lower() == 'help':
#       await ctx.send('If you wish to apply for a spot in our organization, then fill in your information here to join the Wait list. **Here is the link to Application Form:** https://forms.gle/ew36qawvtatTPiBF9')
#     elif parameters.lower() == 'am':
#       warn_am_msg = await ctx.send(warn)
#       asyncio.sleep(15)
#       await warn_am_msg.delete()
#       asyncio.sleep(2)
#       await ctx.author.send(assignment_manager[0])
      
#     def DMChannel_check(m):
#         if ctx.message.guild==None:
#             return m.author == ctx.message.author and m.channel == discord.DMChannel
    
#     await ctx.author.send(assignment_manager[0])
#     try:
#         msg = await client.wait_for('message', timeout=240, check=DMChannel_check)
#     except:
#         print("error")
#     else:
#         print(msg.content)
        
#     await ctx.author.send(assignment_manager[1])
#     try:
#         msg = await client.wait_for('message', timeout=240, check=DMChannel_check)
#     except:
#         print("error")
#     else:
#         print(msg.content)
    
#     await ctx.author.send(assignment_manager[2])
#     am_msg_3 = await client.wait_for('message', timeout=300, check=DMChannel_check)
#     print(am_msg_3)
    
#     await ctx.send(assignment_manager[3])
#     am_msg_4 = await client.wait_for('message', timeout=60, check=DMChannel_check)
    
#     await ctx.send(assignment_manager[4])
#     am_msg_5 = await client.wait_for('message', timeout=360, check=DMChannel_check)
    
#     await ctx.send(assignment_manager[5])
#     am_msg_6 = await client.wait_for('message', timeout=60, check=DMChannel_check)
    
#     await ctx.send(thankyou_application)

#     apply_am_embed=discord.Embed(title='Application for Assignment Manager', description=f'''User: {ctx.author.mention}''', color=0x7289da)
#     apply_am_embed.add_field(name=f'Q: {assignment_manager[0]}', value=f'A: {am_msg.content}', inline=False)
#     apply_am_embed.add_field(name=f'Q: {assignment_manager[1]}', value=f'A: {am_msg_2.content}', inline=False)
#     apply_am_embed.add_field(name=f'Q: {assignment_manager[2]}', value=f'A: {am_msg_3.content}', inline=False)
#     apply_am_embed.add_field(name=f'Q: {assignment_manager[3]}', value=f'A: {am_msg_4.content}', inline=False)
#     apply_am_embed.add_field(name=f'Q: {assignment_manager[4]}', value=f'A: {am_msg_5.content}', inline=False)
#     apply_am_embed.add_field(name=f'Q: {assignment_manager[5]}', value=f'A: {am_msg_6.content}', inline=False)
#     await application_log_channel.send(embed=apply_am_embed)
#         elif parameters.lower() == 'asp':
#       warn_asp_msg = await ctx.send(warn)
#       time.sleep(15)
#       await warn_asp_msg.delete()
#       time.sleep(2)
#       await ctx.send(antiscam_police[0])
#       def asp(m):
#         return m.author == ctx.message.author and m.channel == ctx.message.channel
#       asp_msg = await client.wait_for('message', timeout=60, check=asp)
#       await ctx.send(antiscam_police[1])
#       def asp_2(m):
#         return m.author==ctx.message.author and m.channel == ctx.message.channel
#       asp_msg_2 = await client.wait_for('message', timeout=300, check=asp_2)
#       await ctx.send(antiscam_police[2])
#       def asp_3(m):
#         return m.author==ctx.message.author and m.channel == ctx.message.channel
#       asp_msg_3 = await client.wait_for('message', timeout=60, check=asp_3)
#       await ctx.send(antiscam_police[3])
#       def asp_4(m):
#         return m.author==ctx.message.author and m.channel == ctx.message.channel
#       asp_msg_4 = await client.wait_for('message', timeout=300, check=asp_4)
#       await ctx.send(antiscam_police[4])
#       def asp_5(m):
#         return m.author==ctx.message.author and m.channel == ctx.message.channel
#       asp_msg_5 = await client.wait_for('message', timeout=240, check=asp_5)
#       await ctx.send(antiscam_police[5])
#       def asp_6(m):
#         return m.author==ctx.message.author and m.channel == ctx.message.channel
#       asp_msg_6 = await client.wait_for('message', timeout=360, check=asp_6)
#       await ctx.send(thankyou_application)
#       apply_asp_embed=discord.Embed(title='Application for Anti-Scam Police', description=f'''User: {ctx.author.mention}''', color=0x7289da)
#       apply_asp_embed.add_field(name=f'Q: {antiscam_police[0]}', value=f'A: {asp_msg.content}', inline=False)
#       apply_asp_embed.add_field(name=f'Q: {antiscam_police[1]}', value=f'A: {asp_msg_2.content}', inline=False)
#       apply_asp_embed.add_field(name=f'Q: {antiscam_police[2]}', value=f'A: {asp_msg_3.content}', inline=False)
#       apply_asp_embed.add_field(name=f'Q: {antiscam_police[3]}', value=f'A: {asp_msg_4.content}', inline=False)
#       apply_asp_embed.add_field(name=f'Q: {antiscam_police[4]}', value=f'A: {asp_msg_5.content}', inline=False)
#       apply_asp_embed.add_field(name=f'Q: {antiscam_police[5]}', value=f'A: {asp_msg_6.content}', inline=False)
#       await application_log_channel.send(embed=apply_asp_embed)
#     elif parameters.lower() == 'p':
#       warn_p_msg = await ctx.send()
#       time.sleep(15)
#       await warn_p_msg.delete()
#       time.sleep(2)
#       await ctx.send(programmer[0])
#       def p(m):
#         return m.author == ctx.message.author and m.channel == ctx.message.channel
#       p_msg = await client.wait_for('message', timeout=60, check=p)
#       await ctx.send(programmer[1])
#       def p_2(m):
#         return m.author==ctx.message.author and m.channel == ctx.message.channel
#       p_msg_2 = await client.wait_for('message', timeout=300, check=p_2)
#       await ctx.send(programmer[2])
#       def p_3(m):
#         return m.author==ctx.message.author and m.channel == ctx.message.channel and m.attachments
#       p_msg_3 = await client.wait_for('message', timeout=60, check=p_3)
#       await ctx.send(programmer[3])
#       def p_4(m):
#         return m.author==ctx.message.author and m.channel == ctx.message.channel and m.attachments
#       p_msg_4 = await client.wait_for('message', timeout=300, check=p_4)
#       await ctx.send(programmer[4])
#       def p_5(m):
#         return m.author==ctx.message.author and m.channel == ctx.message.channel
#       p_msg_5 = await client.wait_for('message', timeout=240, check=p_5)
#       await ctx.send(thankyou_application)
#       apply_p_embed=discord.Embed(title='Application for Programmer', description=f'''User: {ctx.author.mention}''', color=0x7289da)
#       apply_p_embed.add_field(name=f'Q: {programmer[0]}', value=f'A: {p_msg.content}', inline=False)
#       apply_p_embed.add_field(name=f'Q: {programmer[1]}', value=f'A: {p_msg_2.content}', inline=False)
#       apply_p_embed.add_field(name=f'Q: {programmer[2]}', value=f'A: {p_msg_3.attachments}', inline=False)
#       apply_p_embed.add_field(name=f'Q: {programmer[3]}', value=f'A: {p_msg_4.attachments}', inline=False)
#       apply_p_embed.add_field(name=f'Q: {programmer[4]}', value=f'A: {p_msg_5.content}', inline=False)
#       await application_log_channel.send(embed=apply_p_embed)
#   else:
#     await ctx.send('You are not allowed to use this command in this channel!')