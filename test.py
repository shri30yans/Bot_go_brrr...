# from datetime import datetime
# import json
# a_datetime = datetime.now()
# import time
# #print(a_datetime)

# json_datetime = json.dumps({"last_daily_command": "2021-08-14T20:14:44.092472"})
# p=json.loads(json_datetime)
# t=datetime.fromisoformat(p["last_daily_command"])

# elapsed= datetime.now() - t
# print(int(elapsed.total_seconds()))

# def convert(seconds):
#                 days = seconds // (3600 *24)
#                 seconds %= (3600*24)
#                 hours = seconds // 3600
#                 seconds %= 3600
#                 minutes = seconds // 60
#                 seconds %= 60
#                 string = ""
#                 d={"days":days,"hours":hours,"minutes":minutes,"seconds":seconds}
#                 revised_d={}
#                 string=""
#                 for unit in list(d):
#                     if d[unit] != 0:
#                         revised_d[unit] = d[unit]
                
#                 for unit in list(revised_d):
#                     string += f"{revised_d[unit]} {unit}"
#                     if len(revised_d) > 1:
#                         if list(revised_d)[-2] == unit:
#                             string += " and "
#                         elif list(revised_d)[-1] == unit:
#                             pass
#                         else:
#                             string += ", "

#                 return string
# print(convert(int(elapsed.total_seconds())))

# def check(message : discord.Message): 
#         return message.author == ctx.author and message.content == correct_answer and message.guild == None

# try:
#     message = await bot.wait_for('message', timeout = 60, check = check)
# except asyncio.TimeoutError: 
#     await ctx.send("The author didn't respond")            
# else: 
#     await ctx.send("The author responded")

# def convert_str_to_number(x):
#     x = x.replace(',','')
#     num = 0
#     num_map = {'K':1000, 'M':1000000, 'B':1000000000}
#     if x.isdigit():
#         num = int(x)
#     else:
#         if len(x) > 1:
#             num = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
#     return int(num)
# print(convert_str_to_number("1,0,0k"))

print(list([1]))
