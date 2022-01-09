from matplotlib import colors, pyplot as plt
import aiohttp
import asyncio
import json
import geopandas as gpd
    
    
async def main():
    async with aiohttp.ClientSession('http://127.0.0.1:1337') as session:
        with open("jsonp.json") as gj:
            gjson = json.load(gj)
        df_places = gpd.read_file('jsonp.json')
        df_places2 = gpd.read_file('jsonp1.json')
        cn_map = df_places.plot(fc="#CCEBEB",ec="#009999",lw=1)
        for item, (index, row), (index2, row2)in zip(gjson.get('features'), df_places.iterrows(), df_places2.iterrows()):
            if index2 != index:
                break;
            async with session.post('/data', json=item) as response:
                sum_raw = await response.json()
                sum = sum_raw.get('sum')
            cn_map.scatter(row2['longitude'], row2['latitude'], s=sum / 500000, color='#FFEB3B',alpha=.5,ec='k',lw=.1)
        
        plt.savefig("1.png", dpi=1000)
    

loop = asyncio.get_event_loop()
loop.run_until_complete(main())