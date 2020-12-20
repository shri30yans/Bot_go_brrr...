# python
import urllib
import json
import aiohttp
import asyncio

async def main():
# url = "http://api.giphy.com/v1/gifs/search"
    params = urllib.parse.urlencode({
    "q": "StarWars",
    "api_key": "oDTSbME4wt0vrDLJ1r1ZEL1tlxuXLFwy",
    "limit": "1",
    "rating": "pg-13"
     })
# with urllib.request.urlopen(url, params) as response:
#     data = json.loads(response.read())
# print(json.dumps(data, sort_keys=True, indent=4))

    async with aiohttp.ClientSession() as session:
        async with session.get("http://api.giphy.com/v1/gifs/search",params=params) as resp:
            response= json.loads(await resp.text())
            response=response["data"][0]["images"]["downsized_large"]["url"]
            print(response)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())