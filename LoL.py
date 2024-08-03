import aiohttp
import config
import asyncio
import Champion

api_key = config.API_KEY


async def get_puuid(name, tag):
    async with aiohttp.ClientSession() as session:
        acc_url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}'
        async with session.get(f'{acc_url}?api_key={api_key}') as acc_data:
            acc_data1 = await acc_data.json()
            return acc_data1['puuid']


async def get_sum_id(region, puuid):
    async with aiohttp.ClientSession() as session:
        url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid' \
              f'/{puuid}' + '?api_key=' + api_key
        async with session.get(url) as sum_data:
            sum_data1 = await sum_data.json()
            return sum_data1['id']


async def get_level(region, puuid):
    async with aiohttp.ClientSession() as session:
        url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid' \
              f'/{puuid}' + '?api_key=' + api_key
        async with session.get(url) as resp:
            info = await resp.json()
            return info['summonerLevel']


async def get_stats(id, puuid, region='RU'):
    async with aiohttp.ClientSession() as session:
        stats = {'level': await get_level(region, puuid)}
        url = f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}?api_key={api_key}'
        async with session.get(url) as resp:
            stat_data = await resp.json()
            stats['rank'] = stat_data[0]['tier'] + ' ' + stat_data[0]['rank'] + ' ' + str(stat_data[0][
                                                                                              'leaguePoints']) + ' lp'
            stats['games'] = stat_data[0]['wins'] + stat_data[0]['losses']
            stats['winrate'] = (stat_data[0]['wins'] / stats['games']) * 100
            stats['winrate'] = '%.1f' % stats['winrate']
            return stats


async def get_top_champions(region, puuid, top=3):
    async with aiohttp.ClientSession() as session:
        url = (f'https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid'
               f'/{puuid}/top?count={top}&api_key={api_key}')
        async with session.get(url) as resp:
            top_champion_data = await resp.json()
            tops = [champ['championId'] for champ in top_champion_data]
            top_champ = [Champion.find_champ(id) for id in tops]
            return top_champ

async def get_icon_id(region, puuid):
    async with aiohttp.ClientSession() as session:
        url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid' \
              f'/{puuid}' + '?api_key=' + api_key
        async with session.get(url) as resp:
            icon_info = await resp.json()
            return icon_info['profileIconId']

