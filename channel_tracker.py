import discord
import os
from dotenv import load_dotenv
from discord.ext import commands 
from datetime import datetime
import aiosqlite
import traceback
import logging



load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = os.getenv("DISCORD_TOKEN")
DB_NAME = os.getenv("DB_NAME")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")
CHANNEL_ID = os.getenv("CHANNEL_ID")
DIZZY = os.getenv("DIZZY")
LOG_ACTIVITY_CHANNEL = os.getenv("LOG_ACTIVITY")

study_times = {}
logging.basicConfig(filename='.output.log', filemode='w', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')



@bot.event
async def initialize_db():
      async with aiosqlite.connect(DB_NAME) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS study_sessions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                duration_in_minutes REAL  
            
                )
            """)

            await db.commit()

      
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await initialize_db()

@bot.event
async def on_voice_state_update(member, before, after):
    study_channel = CHANNEL_NAME
    channel = bot.get_channel(int(LOG_ACTIVITY_CHANNEL))
   
    if after.channel is not None and after.channel.name == study_channel and before.channel != after.channel:
            start_time = datetime.now()
            print(f"{member.name}({member.id}) began studying")
            study_times[member.id] = start_time
            async with aiosqlite.connect(DB_NAME) as db:
                  await db.execute("""
                    INSERT INTO study_sessions (member_id, username, start_time) VALUES (?, ?, ?)
                  """, (member.id, member.name, start_time.strftime("%b %d, %Y at %I:%M%p")))
                  await db.commit()

    
    if before.channel is not None and before.channel.name == study_channel and before.channel != after.channel:

            print(f"{member.name}({member.id}) stopped studying")
             # fallback - none if no member found
            start_time = study_times.pop(member.id, None)

            if start_time is not None:
                end_time = datetime.now()
                duration = end_time - start_time
                minutes = duration.total_seconds() / 60
                print(f"{member.name} studied for {minutes:.1f} minutes")
                if channel is not None:
                      await channel.send(f"{member.name} studied for {minutes:.1f} minutes")


                async with aiosqlite.connect(DB_NAME) as db:
                      await db.execute("""
                            UPDATE study_sessions SET end_time = ?, duration_in_minutes = ? where member_id = ? AND end_time is NULL
                      """, (end_time.strftime("%b %d, %Y at %I:%M%p"), minutes, member.id ))
                      await db.commit()

@bot.event
async def on_error(event, *args, **kwargs):
     channel = bot.get_channel(int(CHANNEL_ID))
     print(channel)
      #  Print to terminal
     print(event)
     print(traceback.format_exc())

     if channel is not None:
           await channel.send(f"Event: {event} \n Traceback:{traceback.format_exc()}")

      

bot.run(TOKEN)


