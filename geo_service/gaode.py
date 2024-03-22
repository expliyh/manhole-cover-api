import aiohttp


class GaoDe:
    @staticmethod
    async def geo_decode(longitude: float, latitude: float):
        # TODO: Get key from config
        key = "fbba3ef6d61e2b95c8e01f095095d946"
        url = 'https://restapi.amap.com/v3/geocode/regeo'
        params = {
            'key': key,
            'location': f'{longitude:.6f},{latitude:.6f}',
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


gaode = GaoDe()

