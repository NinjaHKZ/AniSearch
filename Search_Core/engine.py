import aiohttp, os, sys
import asyncio, json


class Engine:
	async def Start(config) -> dict:
		print('Core Iniciado')
		Tasks = []
		for data in config:
			try:
				if data['auth'] == 'DeveloperServerProcessCore[32#@AdminAuth022HRoot@#32]':
					Tasks.append(asyncio.create_task(Engine._EngineCore(data)))
			except KeyError:
				pass

		if len(Tasks) == 0:
			return {'RunError': 'Failed'}
		results = await asyncio.gather(*Tasks) 

		_resultsFilter = {}

		for dicts in results:
			for data in dicts.items():
				for i in data[1]:
					sitename = i[0]

					for replacement in [('á', 'a'), ('à', 'a'), ('-', ' '), (';', ' '),('  ', '')]:
						sitename = sitename.lower().replace(replacement[0], replacement[1]).title() 

					try:
						_resultsFilter[sitename].append(i[1])

					except KeyError:
						_resultsFilter.update({sitename: [i[1]]})
								
		return _resultsFilter

	async def _EngineCore(db) -> dict:

		async with aiohttp.ClientSession() as request:
			if db['method'] == 'post':
				req = await request.post(db['url'], data=db['data'], headers=db['headers'])

			elif db['method'] == 'get':
				req = await request.get(db['url'], data=db['data'], headers=db['headers'])
	
			req = await req.json() if req.content_type != "text/html" else await req.text()

			try:
				req = json.loads(req)
				req = (db['name'],  req)

			except:
				req = (db['name'],  req)


			_data = { req[0]: [] }


			if req[0] == 'animefire.net':
				await asyncio.sleep(0)
				
				for i in req[1]:
					_data[req[0]].append((i[0], 'https://animefire.net/animes/'+i[5]))
					await asyncio.sleep(0)
			
			elif req[0] == 'animesorionvip.com':
				await asyncio.sleep(0)

				for  i in req[1].items():
					try:
						_data[req[0]].append((i[1]['title'], i[1]['url']))
						await asyncio.sleep(0)

					except TypeError:
						_data[req[0]].append(('error', 'not found'))
						break
			return _data


if __name__ == "__main__":
	anime = 'steins'
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

	conf = [{
				'name': "animefire.net",
				'url': "https://animefire.net/proc/quicksearch", 
				'method': "post",  
				'data': {'word': anime},
				'headers': None,
				'auth': 'DeveloperServerProcessCore[32#@AdminAuth022HRoot@#32]'
			},{
				
				'name': "animesorionvip.com",
				'url': f"https://animesorionvip.com/wp-json/animesorion/search/?keyword={anime}&nonce=159160d430",
				'method': "get",
				'data': None,
				'headers': {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'}
			}]


	data = asyncio.run(Engine.Start(conf))
	print(json.dumps(data, indent=3))