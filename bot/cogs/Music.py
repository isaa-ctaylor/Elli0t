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

import asyncio
import functools
import itertools
import math
import random
import re
import urllib

import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands

youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.20):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**`{0.title}`** by **`{0.uploader}`**'.format(self)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))
        else:
            if days == 0 and hours == 0 and minutes == 0 and seconds == 0:
                duration.append('Live Stream')

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester', 'bot')

    def __init__(self, source: YTDLSource, bot):
        self.source = source
        self.requester = source.requester
        self.bot = bot

    def create_embed(self):
        return (
            discord.Embed(
                title="Now playing:",
                description='[`{0.source.title}`]({0.source.url})'.format(self),
                colour=self.bot.neutral_embed_colour,
            )
                .set_footer(
                text=f"{self.source.duration} - DJ: {self.requester.name}",
                icon_url=self.requester.avatar.url,
            )
                .set_thumbnail(url=self.source.thumbnail)
        )


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(2419200):  # 1 month
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.voice.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx):
        ctx.voice_state = self.get_voice_state(ctx)

    @commands.command(name="join", invoke_without_subcommand=True)
    async def _join(self, ctx):
        '''
        Join a voice channel
        '''

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)

        ctx.voice_state.voice = await destination.connect()

        await ctx.reply(f"\U0001f44c Joined {destination.name}")

    @commands.command(name="summon")
    async def _summon(self, ctx, *, channel: discord.VoiceChannel = None):
        '''
        Summon me to a voice channel
        '''
        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel / not specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            await ctx.reply(f"\U0001f44c Joined {destination.name}")

        ctx.voice_state.voice = await destination.connect()
        await ctx.reply(f"\U0001f44c Joined {destination.name}")

    @commands.command(name="leave")
    async def _leave(self, ctx):
        '''
        Make me leave the voice channel
        '''
        if not ctx.voice_state.voice:
            return await ctx.error('I am not connected to any voice channel.')

        if not ctx.author.voice:
            return await ctx.error("You are not connected to any channel!")
        
        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            return await ctx.error("You aren't in my voice channel.")

        dest = ctx.author.voice.channel
        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]
        embed = discord.Embed(title=f"Disconnected from {dest}", colour=self.bot.neutral_embed_colour)
        await ctx.reply(embed=embed)

    @commands.command(name="vol")
    async def _volume(self, ctx, *, volume: int):
        '''
        Set the player volume
        '''
        if not ctx.author.voice or not ctx.author.voice.channel:
            return await ctx.reply('You are not connected to any voice channel.')

        if not ctx.voice_state.is_playing:
            return await ctx.reply('Nothing being played at the moment.')

        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            return await ctx.reply("You aren't in my voice channel.")

        if volume > 150 or volume < 0:
            return await ctx.reply('Volume must be between **0 and 150**')

        ctx.voice_client.source.volume = volume / 150
        await ctx.message.add_reaction('✅')

    @commands.command(name="now", aliases=['current', 'playing'])
    async def _now(self, ctx):
        '''
        See the current song
        '''
        await ctx.reply(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause')
    async def _pause(self, ctx):
        '''
        Pause the player
        '''
        server = ctx.message.guild
        voice_channel = server.voice_client

        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            return await ctx.reply("You aren't in my voice channel.")

        voice_channel.pause()
        await ctx.message.add_reaction('⏯')

    @commands.command(name='resume')
    async def _resume(self, ctx):
        '''
        Resume the player
        '''
        server = ctx.message.guild
        voice_channel = server.voice_client

        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            return await ctx.reply("You aren't in my voice channel.")

        voice_channel.resume()
        await ctx.message.add_reaction('⏯')

    @commands.command(name="stop")
    async def _stop(self, ctx):
        '''
        Stop the player
        '''
        if not ctx.author.voice or not ctx.author.voice.channel:
            return await ctx.reply('You are not connected to any voice channel.')

        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            return await ctx.reply("You aren't in my voice channel.")

        await ctx.message.add_reaction('✅')
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()

    @commands.command(name='skip')
    async def _skip(self, ctx):
        '''
        Skip the current song
        '''
        if not ctx.author.voice or not ctx.author.voice.channel:
            return await ctx.reply('You are not connected to any voice channel.')

        if not ctx.voice_state.is_playing:
            return await ctx.reply('Not playing any music right now...')

        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            return await ctx.reply("You aren't in my voice channel.")

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()
            return

        elif voter.id != ctx.voice_state.current.requester:
            if ctx.voice_state.current.requester not in ctx.author.voice.channel.members:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
                return

        if voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.reply('Skip vote added, currently at **{}/3**'.format(total_votes))

        else:
            await ctx.reply('You have already voted to skip this song.')

    @commands.command(name='queue')
    async def _queue(self, ctx, *, page: int = 1):
        '''
        See the current queue
        '''
        if len(ctx.voice_state.songs) == 0:
            return await ctx.reply('The queue is empty.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''.join(
            '`{0}.` [**{1.source.title}**]({1.source.url})\n`{1.source.duration}`\n\n'.format(
                i + 1, song
            )
            for i, song in enumerate(ctx.voice_state.songs[start:end], start=start)
        )

        embed = (
            discord.Embed(description='**{} Tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue), colour=self.bot.neutral_embed_colour)
                .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.reply(embed=embed)

    @commands.command(name='shuffle', help="Shuffle the queue")
    async def _shuffle(self, ctx):

        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            return await ctx.reply("You aren't in my voice channel.")

        if len(ctx.voice_state.songs) == 0:
            return await ctx.reply('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove')
    async def _remove(self, ctx, index: int):
        '''
        Remove a song from the queue
        '''
        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            return await ctx.reply("You aren't in my voice channel.")

        if len(ctx.voice_state.songs) == 0:
            return await ctx.reply('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='play')
    async def _play(self, ctx, *, search: str):
        '''
        Play a song
        '''
        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.reply('**`ERROR`**: {}'.format(str(e)))
            else:
                song = Song(source, self.bot)

                await ctx.voice_state.songs.put(song)
                await ctx.reply('Enqueued {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.')

        if (
                ctx.voice_client
                and ctx.voice_client.channel != ctx.author.voice.channel
        ):
            raise commands.CommandError("I'm already in a voice channel.")

def setup(bot):
    bot.add_cog(Music(bot))
