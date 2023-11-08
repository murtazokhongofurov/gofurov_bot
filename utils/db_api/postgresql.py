from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config


class Database:
    def __int__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = ("CREATE TABLE IF NOT EXISTS users(\n"
               "            id SERIAL PRIMARY KEY,\n"
               "            chat_id BIGINT NOT NULL UNIQUE,\n"
               "            first_name VARCHAR(250),\n"
               "            message TEXT\n"
               "        )")
        await self.execute(sql, execute=True)

    async def add_user(self, chat_id, first_name):
        sql = """INSERT INTO users(
            chat_id, first_name
        ) VALUES ($1, $2)"""
        await self.execute(sql, chat_id, first_name, fetchrow=True)

    async def get_user(self, chat_id):
        sql = """SELECT chat_id, first_name, message FROM users WHERE chat_id=$1"""
        return await self.execute(sql, chat_id, fetchrow=True)

    async def update_user_message(self, chat_id, message):
        sql = """UPDATE users SET message=$1 WHERE chat_id=$2"""
        await self.execute(sql, message, chat_id, fetchrow=True)