
import discord
from discord.ext import commands
import youtube_dl
import asyncio
import os
from collections import deque

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}
        self.queues = {}
        self.now_playing = {}
        self.loop_mode = {}  # 0: no loop, 1: loop song, 2: loop queue
        
        # YouTube DL options
        self.ytdl_format_options = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        
        self.ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        
        self.ytdl = youtube_dl.YoutubeDL(self.ytdl_format_options)

    def get_queue(self, guild_id):
        if guild_id not in self.queues:
            self.queues[guild_id] = deque()
        return self.queues[guild_id]

    async def search_youtube(self, query):
        """Search for a song on YouTube"""
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(f"ytsearch:{query}", download=False))
            
            if 'entries' in data and data['entries']:
                return data['entries'][0]
            return None
        except Exception as e:
            print(f"Error searching: {e}")
            return None

    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx, *, query=None):
        """Play a song or add it to queue"""
        if not query:
            await ctx.send("🎵 Please provide a song name or URL!\nExample: `!play never gonna give you up`")
            return
            
        if not ctx.author.voice:
            await ctx.send("❌ You need to be in a voice channel!")
            return
            
        channel = ctx.author.voice.channel
        
        # Connect to voice channel if not connected
        if ctx.guild.id not in self.voice_clients:
            try:
                voice_client = await channel.connect()
                self.voice_clients[ctx.guild.id] = voice_client
            except Exception as e:
                await ctx.send(f"❌ Couldn't connect to voice channel: {e}")
                return
        
        # Search for the song
        async with ctx.typing():
            song_info = await self.search_youtube(query)
            
            if not song_info:
                await ctx.send("❌ Couldn't find that song!")
                return
                
            song_data = {
                'title': song_info.get('title', 'Unknown'),
                'url': song_info.get('webpage_url', ''),
                'duration': song_info.get('duration', 0),
                'requester': ctx.author,
                'stream_url': song_info.get('url', '')
            }
            
            queue = self.get_queue(ctx.guild.id)
            
            # If nothing is playing, start playing immediately
            voice_client = self.voice_clients[ctx.guild.id]
            if not voice_client.is_playing():
                await self.play_song(ctx, song_data)
            else:
                queue.append(song_data)
                embed = discord.Embed(
                    title="🎵 Added to Queue",
                    description=f"**{song_data['title']}**",
                    color=discord.Color.green()
                )
                embed.add_field(name="Position in queue", value=len(queue), inline=True)
                embed.add_field(name="Requested by", value=ctx.author.mention, inline=True)
                await ctx.send(embed=embed)

    async def play_song(self, ctx, song_data):
        """Play a specific song"""
        voice_client = self.voice_clients[ctx.guild.id]
        
        try:
            # Create audio source
            source = discord.FFmpegPCMAudio(song_data['stream_url'], **self.ffmpeg_options)
            
            # Play the song
            voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.song_finished(ctx), self.bot.loop))
            
            # Update now playing
            self.now_playing[ctx.guild.id] = song_data
            
            # Send now playing embed
            embed = discord.Embed(
                title="🎵 Now Playing",
                description=f"**{song_data['title']}**",
                color=discord.Color.blue()
            )
            embed.add_field(name="Requested by", value=song_data['requester'].mention, inline=True)
            
            if song_data['duration']:
                duration = f"{song_data['duration'] // 60}:{song_data['duration'] % 60:02d}"
                embed.add_field(name="Duration", value=duration, inline=True)
                
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Error playing song: {e}")

    async def song_finished(self, ctx):
        """Called when a song finishes"""
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        
        # Check loop mode
        loop_mode = self.loop_mode.get(guild_id, 0)
        
        if loop_mode == 1:  # Loop current song
            current_song = self.now_playing.get(guild_id)
            if current_song:
                await self.play_song(ctx, current_song)
                return
        elif loop_mode == 2 and guild_id in self.now_playing:  # Loop queue
            queue.append(self.now_playing[guild_id])
        
        # Play next song in queue
        if queue:
            next_song = queue.popleft()
            await self.play_song(ctx, next_song)
        else:
            if guild_id in self.now_playing:
                del self.now_playing[guild_id]

    @commands.command(name='skip', aliases=['s'])
    async def skip(self, ctx):
        """Skip the current song"""
        if ctx.guild.id not in self.voice_clients:
            await ctx.send("❌ Not connected to a voice channel!")
            return
            
        voice_client = self.voice_clients[ctx.guild.id]
        if voice_client.is_playing():
            voice_client.stop()
            await ctx.send("⏭️ Skipped!")
        else:
            await ctx.send("❌ Nothing is playing!")

    @commands.command(name='queue', aliases=['q'])
    async def queue_command(self, ctx):
        """Show the current queue"""
        queue = self.get_queue(ctx.guild.id)
        
        if not queue and ctx.guild.id not in self.now_playing:
            await ctx.send("📭 Queue is empty!")
            return
            
        embed = discord.Embed(
            title="🎵 Music Queue",
            color=discord.Color.purple()
        )
        
        # Show currently playing
        if ctx.guild.id in self.now_playing:
            current = self.now_playing[ctx.guild.id]
            embed.add_field(
                name="🎵 Now Playing",
                value=f"**{current['title']}**\nRequested by {current['requester'].mention}",
                inline=False
            )
        
        # Show queue
        if queue:
            queue_list = []
            for i, song in enumerate(list(queue)[:10], 1):  # Show first 10 songs
                queue_list.append(f"{i}. **{song['title']}** - {song['requester'].mention}")
            
            embed.add_field(
                name="📝 Up Next",
                value="\n".join(queue_list),
                inline=False
            )
            
            if len(queue) > 10:
                embed.add_field(
                    name="📊 Queue Stats",
                    value=f"Showing 10 of {len(queue)} songs",
                    inline=True
                )
        
        await ctx.send(embed=embed)

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stop music and clear queue"""
        if ctx.guild.id not in self.voice_clients:
            await ctx.send("❌ Not connected to a voice channel!")
            return
            
        voice_client = self.voice_clients[ctx.guild.id]
        
        # Clear queue and stop playing
        self.queues[ctx.guild.id] = deque()
        if ctx.guild.id in self.now_playing:
            del self.now_playing[ctx.guild.id]
            
        voice_client.stop()
        await ctx.send("⏹️ Stopped music and cleared queue!")

    @commands.command(name='leave', aliases=['disconnect'])
    async def leave(self, ctx):
        """Leave the voice channel"""
        if ctx.guild.id not in self.voice_clients:
            await ctx.send("❌ Not connected to a voice channel!")
            return
            
        voice_client = self.voice_clients[ctx.guild.id]
        await voice_client.disconnect()
        del self.voice_clients[ctx.guild.id]
        
        # Clear queue
        if ctx.guild.id in self.queues:
            del self.queues[ctx.guild.id]
        if ctx.guild.id in self.now_playing:
            del self.now_playing[ctx.guild.id]
            
        await ctx.send("👋 Left the voice channel!")

    @commands.command(name='loop')
    async def loop(self, ctx, mode=None):
        """Set loop mode: off, song, queue"""
        if not mode:
            current_mode = self.loop_mode.get(ctx.guild.id, 0)
            modes = ["Off", "Song", "Queue"]
            await ctx.send(f"🔄 Current loop mode: **{modes[current_mode]}**\nUse `!loop off/song/queue` to change")
            return
            
        mode = mode.lower()
        if mode in ['off', 'none', '0']:
            self.loop_mode[ctx.guild.id] = 0
            await ctx.send("🔄 Loop mode: **Off**")
        elif mode in ['song', 'track', '1']:
            self.loop_mode[ctx.guild.id] = 1
            await ctx.send("🔄 Loop mode: **Song**")
        elif mode in ['queue', 'all', '2']:
            self.loop_mode[ctx.guild.id] = 2
            await ctx.send("🔄 Loop mode: **Queue**")
        else:
            await ctx.send("❌ Invalid mode! Use: `off`, `song`, or `queue`")

async def setup(bot):
    await bot.add_cog(MusicCog(bot))
