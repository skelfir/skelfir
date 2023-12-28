import json
#import httpx
import asyncio
import websockets

websocket_url = 'wss://www.seismicportal.eu/standing_order/websocket'
#API_URL = 'https://new.skelfir.com/api/quakes2'
API_URL = 'http://localhost/api/quakes2'


async def receive(ws):
	#async with websockets.connect(websocket_url) as ws:
	msg = await ws.recv()
	print(f'received msg: {msg}')
	quake = json.loads(msg)
	return quake
	#rsp = httpx.post('https://new.skelfir.com/api/quakes/', json=quake)


async def post(quake):
	#rsp = httpx.post('https://new.skelfir.com/api/quakes/', json=quake)
	print('post quake')
	print(quake)
	pass


async def main():
	ws = await websockets.connect(websocket_url)
	#websocket_url = 'wss://www.seismicportal.eu/standing_order/websocket'
	while True:
		quake = await receive(ws)
		await post(quake)


if __name__ == '__main__':
	asyncio.run(main())
