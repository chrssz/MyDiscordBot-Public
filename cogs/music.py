import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import wavelink

class Music(commands.Cog, name="Music Player"):
    def __init__(self,bot):
        self.bot = bot
    @staticmethod
    #converts given time(in milliseconds) to minutes.
    def convertM(millis):
        seconds = (millis/1000)%60
        minutes = (millis/(1000*60))%60
        hours = ((millis/1000*60*60))%24
        if hours == 0:
            return f'{int(minutes):02d}:{int(seconds):02d}'
        
        return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'

    @commands.Cog.listener()
    async def on_track_end(self,ctx):
        vc: wavelink.Player = ctx.voice_client
        if not vc.queue.is_empty():
            await vc.play(vc.queue.get())
    
    @commands.command()
    async def play(self,ctx: commands.Context, *, search: str) -> None:
        if not ctx.author.voice:
            await ctx.send(f"**Error: You are not in a voice channel**")
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        tracks: list[wavelink.YouTubeTrack] = await wavelink.YouTubeTrack.search(search)
        if not tracks:
            await ctx.send(f'***Could not find any songs with search: `{search}`***')
            return
        track: wavelink.YouTubeTrack = tracks[0]
        vc.queue(track)
        if vc.is_playing():
            await ctx.send(f"***Queued Track: `{track}: {Music.convertM(track.length)}`***")
        else:
            await ctx.send(f"***Playing Track: `{track}: {Music.convertM(track.length)}` ***")
            await vc.play(vc.queue.get())

           
            
    @commands.command()
    async def stop(self,ctx):
       if not ctx.author.voice:
            await ctx.send(f"**Error: not connected to a voice channel**")
       else:
            vc: wavelink.Player = ctx.voice_client
            await vc.stop()
            await ctx.send("***Stopping Audio ***")
    @commands.command()
    async def pause(self,ctx: commands.Context):
        if not ctx.author.voice:
            await ctx.send(f"**Error: not connected to a voice channel**")
        else:
            vc: wavelink.Player = ctx.voice_client
            await vc.pause()
            await ctx.send("***Pausing Audio ***")

    @commands.command()
    async def resume(self,ctx: commands.Context):
        if not ctx.author.voice:
            await ctx.send(f"**Error: not connected to a voice channel**")
        else:
            vc: wavelink.Player = ctx.voice_client
            await vc.resume()
            await ctx.send("***Resuming Audio ***")
    
    @commands.command()
    async def skip(self, ctx: commands.Context):
        if not ctx.author.voice:
            await ctx.send(f"**Error: not connected to a voice channel**")
        else:
            vc: wavelink.Player = ctx.voice_client
            if not vc.queue.is_empty:
                await vc.stop()
                await vc.play(vc.queue.get())
                await ctx.send("***Skipping Current Audio ***")
            else:
                await ctx.send("*** Error: No tracks in queue ***")

    @commands.command()
    async def queue(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        num = 0
        if vc.queue.is_empty:
            await ctx.send("***Queue is empty***")
        for track in vc.queue:
            num+=1
            await ctx.send(f"***Current Queue at Position [{num}]: `{track}` ***")
    
    @commands.command()
    async def clear(self,ctx:commands.Context):
        if not ctx.author.voice:
            await ctx.send(f"**Error: not connected to a voice channel**")
        else:
            vc: wavelink.Player = ctx.voice_client
            await ctx.send("***Clearing Queue and Play History ***")
            vc.queue.reset()
    
    @commands.command()
    async def playhistory(self,ctx:commands.Context):
        vc: wavelink.Player = ctx.voice_client
        if vc.queue.history.is_empty:
            await ctx.send("***Play history is empty***")
        await ctx.send("Play history: ")
        for track in vc.queue.history:
            await ctx.send(f"***`{track}`***")

    
async def setup(bot):
    await bot.add_cog(Music(bot))