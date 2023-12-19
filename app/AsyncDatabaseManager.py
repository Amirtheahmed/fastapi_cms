import os
from typing import List

from psycopg.rows import Row
from psycopg_pool import AsyncConnectionPool


class AsyncDatabaseManager:
    def __init__(self):
        self.pool: AsyncConnectionPool | bool = False

    async def connect(self) -> None:
        conn_str = self._get_conn_str()
        self.pool = AsyncConnectionPool(conninfo=conn_str)
        await self.pool.wait()

    async def disconnect(self) -> None:
        await self.pool.close()

    async def get_articles(self) -> List[Row]:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    SELECT * FROM articles
                """
                )

                return await cur.fetchall()

    def _get_conn_str(self) -> str:
        dbname = os.getenv("POSTGRES_DB", "default_db_name")
        user = os.getenv("POSTGRES_USER", "default_user")
        password = os.getenv("POSTGRES_PASSWORD", "default_password")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")

        return (
            f"dbname={dbname} user={user} password={password} host={host} port={port}"
        )
