from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint

from app.db import r
from app.db import connection


async def insert_quake(data, conflict='error'):
	async with connection() as conn:
		res = await r.table('quakes').insert(
			data,
			conflict=conflict,
			return_changes=True,
		).run(conn)
	return res


class QuakesRoute(HTTPEndpoint):
	async def get(self, request):
		return JSONResponse({"msg": "Hello, world!"})

	async def put(self, req):
		# full update
		quake = await req.json()
		res = await insert_quake(quake, conflict='replace')
		return JSONResponse(res)

	async def patch(self, req):
		# partial update
		quake = await req.json()
		res = await insert_quake(quake, conflict='update')
		return JSONResponse(res)

	async def post(self, req):
		# insert new
		print('post new quake')
		quake = await req.json()
		print(f'quake: {quake}')
		res = await insert_quake(quake, conflict='error')
		print(res)
		return JSONResponse({"success": True, "id": quake['id']})
