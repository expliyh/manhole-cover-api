import aiohttp


class GaoDe:
    @staticmethod
    async def geo_decode(longitude: float, latitude: float):
        # TODO: Get key from config
        key = "TODO: Get key from config"
        url = 'https://restapi.amap.com/v3/geocode/regeo'
        params = {
            'key': key,
            'location': f'{longitude:.5f},{latitude:.5f}',
            'radius': 150,
            'extensions': 'all'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                result = await resp.json()

        return result['regeocode']['formatted_address']

        # road_inters = result['regeocode']['roadinters']
        # road_inters.sort(key=lambda x: x['distance'])
        # if road_inters[0]['distance'] < 30:
        #     return f""
