from databases import Database
from databases import Database
from core.config import config


connection = Database(
    config.database.DSN,
    min_size=config.database.POOL_SIZE,
    max_size=config.database.POOL_MAX_SIZE,
)


async def startup():
    await connection.connect()


async def shutdown():
    await connection.disconnect()