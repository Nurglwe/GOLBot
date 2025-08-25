import discord.object
import discord,os,tools, datetime
from discord.ext import commands
from discord import app_commands
from calendar import monthrange
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="->",intents=intents, guilds=True, members=True)

'''

Below is events

'''

@client.event
async def on_ready():
  print("Ready")

  
'''

Below is commands

'''

@client.tree.command(name="echo", description="Echoes a message")
@app_commands.describe(message= "The message to echo.")
async def echo(interaction: discord.Interaction, message: str) -> None:
  await interaction.response.send_message(message)

'''
@client.tree.command(
    name="create schedule", 
    description="Creates a table of thursdays and sundays in a month"
  )
@app_commands.describe(month= "Month (1-12)", year="Year")
interaction: discord.Interaction,
'''
@client.command()
async def makeschedule(ctx, month: int, year: int) -> None:
  standard_op_days = []
  print(month, year)
  if not(month < 1 or month > 12):
    first_day, num_days = monthrange(year, month)
    print(first_day, num_days)
    week_day = first_day
    for day in range(1, num_days + 1):
      week_day += 1
      if week_day  == 4:
        standard_op_days.append(day)
      if week_day >= 7:
        standard_op_days.append(day)
        week_day = 0
    print(standard_op_days)
    


@client.command()
async def ping(ctx):
  await ctx.send('Pong, {} Ms'.format(round(client.latency * 1000, 2)))

@client.command()
async def synctree (ctx):
  if ctx.author.id == 220213079944724482:
    resp = await client.tree.sync()
    await ctx.send(f"Commands synced with response {resp}")



# Don't touch below
#keepalive.keep_alive()
token = os.getenv('DSTOKEN')
client.run(token)