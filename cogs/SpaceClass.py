import os, sys, discord, platform, random, aiohttp, json,time,asyncio,datetime
from discord.ext import commands,tasks

colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
            0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]

class Space(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.astronaut_update.start() #pylint: disable=no-member
        # Ignore this error.It is a linter warning.

    @tasks.loop(hours=12)
    async def astronaut_update(self):
        await self.bot.wait_until_ready()
        async with aiohttp.ClientSession() as cs:
            url="http://api.open-notify.org/astros.json"

            async with cs.get(url) as r:
                res = await r.json()
                
                self.number_of_astronauts=res['number']

                astronaut_names_list=res['people']
                
                astronaut_names=list("")
                for person in astronaut_names_list:
                    name=person.get("name")
                    astronaut_names.append(name)
                astronaut_names_string=" \n \u200B"

                for person in astronaut_names:
                    astronaut_names_string=astronaut_names_string +"<a:glowing_planet:779922671395012619>  " + person+" \n"
                self.astronaut_names_string=astronaut_names_string
                

    

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="astronauts",aliases=['astro','astronaut'], help='Brings up some Astronauts Information \n\"Yeet astro\" \n Aliases: astronaut,astronauts')
    async def astronauts(self,ctx):
                embed = discord.Embed(title = "Astronauts <:Kerbal_Astronaut:779922671516254240>", color = random.choice(colourlist),timestamp=ctx.message.created_at)
                embed.add_field(name=f"<:Rocket:779929368368644126> Number of Astronauts in space: {self.number_of_astronauts}",value=self.astronaut_names_string,inline="False")
                author_avatar=ctx.author.avatar_url
                embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
                await ctx.send(embed=embed)

                '''
                <a:glowing_planet:779922671395012619>
                <:Kerbal_Astronaut:779922671516254240>
                <:Spacethink:779922671898591263>      
                <:Moon_Cake:779922674897387530>
                <a:rotating_earth:779922676704739328>
                <:Rocket:779929368368644126>
                <:mars:779978907386380328> 
                '''
                
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="mars", help='Tells the Martian Time and Date \n\"Yeet mars\"')
    async def  mars_time(self,ctx):
        returned_tuple=mars_time_calculate()
        sol=returned_tuple[0]
        time=returned_tuple[1]
        embed = discord.Embed(title = "Martian Date and Time <:mars:779978907386380328>", color = random.choice(colourlist),timestamp=ctx.message.created_at)
        embed.add_field(name=f"<:Rocket:779929368368644126>  |  Sol:",value=f"{sol}",inline="False")
        embed.add_field(name=f":alarm_clock:  |  Time:",value=f"{time} MTC",inline="False")
        author_avatar=ctx.author.avatar_url
        embed.set_footer(icon_url= author_avatar,text=f"Requested by {ctx.message.author} • Yeet Bot ")
        await ctx.send(embed=embed)



          



    '''def mars_nasa_api():
    f = "https://api.nasa.gov/insight_weather/?api_key=DEMO_KEY&feedtype=json&ver=1.0"
    data = requests.get(f)
    tt = json.loads(data.text)
    for i in tt:
    return tt[i]["Season"]

    mars_season= mars_nasa_api().capitalize() #Capatilzes the first letter of the season'''
        
      
def mars_time_calculate():      
    datetime.datetime.utcnow()
    time.time()

    def pretty_thousands(num):
        pretty_num = "{:,}".format(num)
        pretty_num = pretty_num.replace(',', ',')
        return pretty_num

    #Converting  Earth UTC date to sols
    tai_offset = 37     
    millis = 1000*time.time()
    jd_ut = 2440587.5 + (millis / (8.64*10**7))      
    jd_tt = jd_ut + (tai_offset + 32.184) / 86400
    j2000 = jd_tt - 2451545.0
    mars_sol = (((j2000 - 4.5) / 1.027491252) + 44796.0 - 0.00096)

    #Converting UTC to MTC (Martian Coordinated Time)
    mtc = (24 * mars_sol) % 24
    mtc_hours = int(mtc)
    mtc_minutes = int((mtc - mtc_hours)*60)
    mtc_seconds = int(((mtc - mtc_hours)*60 - mtc_minutes)*60)
    mtc_time = datetime.time(hour=mtc_hours, minute=mtc_minutes, second=mtc_seconds)
    Sol=(pretty_thousands(int(mars_sol)))
    Time=str(mtc_time)[0:8]
    return Sol,Time



def setup(bot):
    bot.add_cog(Space(bot))