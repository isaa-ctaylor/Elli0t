"""
MIT License

Copyright (c) 2021 isaa-ctaylor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncpg
import asyncio
import time


class database:
    def __init__(self, **kwargs):
        self.pool = asyncio.get_event_loop().run_until_complete(self.new_connection(**kwargs))

    @classmethod
    async def new_connection(self, **kwargs):
        return await asyncpg.create_pool(user=kwargs.pop("user", "postgres"),
                                         password=kwargs.pop("password", "postgres"),
                                         database=kwargs.pop("database", "data"),
                                         host=kwargs.pop("host", "localhost"))

    async def update_prefixes(self, bot):
        bot.prefixes = {}
        
        async with bot.db.pool.acquire() as con:
            thing = await con.fetch("SELECT * FROM PREFIXES;")

        for i in thing:
            bot.prefixes[int(i["guild_id"])] = str(i["prefix"])
            
        return bot

    async def setPrefix(self, bot, guild_id, prefix):
        async with bot.db.pool.acquire() as con:
            await con.execute("""INSERT INTO prefixes(guild_id, prefix)
                                    values($1, $2)
                                    ON CONFLICT (guild_id)
                                    DO UPDATE SET prefix = $2 WHERE prefixes.guild_id = $1;""", int(guild_id), str(prefix))
        
        return await self.update_prefixes(bot)

    async def load_emoji_users(self, bot):
        async with bot.db.pool.acquire() as con:
            rawemojidata = await con.fetch("SELECT user_id, emojis FROM userdata")
            
        bot.emojiusers = []
        
        for record in rawemojidata:
            if record["emojis"]:
                bot.emojiusers.append(int(record["user_id"]))
                                      
        return bot

    async def ping(self):
        async with self.pool.acquire() as con:
            start = time.perf_counter()
            await con.fetch("SELECT 1")
            theTime = (time.perf_counter() - start)*100
        return theTime
