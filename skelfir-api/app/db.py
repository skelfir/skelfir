from collections import deque
from contextlib import asynccontextmanager

from rethinkdb import r

# CONFIG
pool_size = 4
db_name = 'test'
db_port = 28015
db_host = '139.59.176.108'
# CONFIG

pool = deque()
r.set_loop_type('asyncio')

tables = (
	'quakes',
	'devices',
)


async def create_tables():
	async with connection() as conn:
		existing_tables = await r.table_list().run(conn)
		tables_to_create = list(set(tables) - set(existing_tables))
		for table in tables_to_create:
			await r.table_create(table).run(conn)
			print(f"table {table} created")


async def setup():
	# create `pool_size` number of connections
	# and put them in the connection pool
	for p in range(0, pool_size):
		conn = await r.connect(host=db_host, port=db_port, db=db_name)
		pool.append(conn)
	await create_tables()


@asynccontextmanager
async def connection():
	# pop the first connection in the pool
	conn = pool.popleft()
	try:
		yield conn
	finally:
		# add the connection to the back of the pool
		pool.append(conn)
