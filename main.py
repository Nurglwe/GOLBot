import discord.object
import discord,os,tools, calendar, pickle
from discord.ext import commands
from discord import app_commands
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
@client.command(brief="Create an orbat for a given year (YYYY) and month (M or MM)")
async def makeschedule(ctx, year: int, month: int) -> None:
  standard_op_days = {}
  print(month, year)
  month_str = calendar.month_name[month]

  if not(month < 1 or month > 12):
    first_day, num_days = calendar.monthrange(year, month)
    print(first_day, num_days)
    week_day = first_day
    for day in range(1, num_days + 1):
      week_day += 1
      if week_day  == 4:
        standard_op_days.update({f"{calendar.day_name[week_day-1]} {day} <:Training:1173686838926512199>": None})
      if week_day >= 7:
        standard_op_days.update({f"{calendar.day_name[week_day-1]} {day} <:Mission:1173686836451885076>": None})
        week_day = 0

    print(standard_op_days)

    with open(f"operations-{month}-{year}.pkl", "wb") as f:
      pickle.dump(standard_op_days, f)

    embed = tools.embedhandler(
      f"Operations for {month_str} {year}",
      0x154c79,
      client.get_channel(1409503885156028416),
      False,
      None,
      client
      )
    await tools.embedhandler.sendembed(embed, standard_op_days)
    
@client.command(brief="Add name(s) from operation automatically. Takes Year (YYYY), Month(M or MM), day (D or DD) and optionally targetted users")
async def addname (ctx, year, month, day, *args) -> None:
  print(year, month, day, args)
  if len(args) == 0:
    target = [f"<@{ctx.author.id}>"]
  else:
    target = [user for user in args]
  
  try:
    with open(f"operations-{month}-{year}.pkl", "rb") as f:
      data = pickle.load(f)
  except:
    await ctx.channel.send("Error: File not found")
  
  print(data)
  
  output_str = ""
  for operation in data.keys():
    sub_sect = operation.split(" ")
    if sub_sect[1] == day:
      print(operation)
      for user in target:
        print(user)
        output_str = output_str + user + " "
      data[operation] = output_str
  
  with open(f"operations-{month}-{year}.pkl", "wb") as f:
    pickle.dump(data, f)
  
  await client.get_channel(1409503885156028416).purge(limit=1)
  
  month_str = calendar.month_name[int(month)]
  embed = tools.embedhandler(
    f"Operations for {month_str} {year}",
    0x154c79,
    client.get_channel(1409503885156028416),
    False,
    None,
    client
  )
  await tools.embedhandler.sendembed(embed, data)
    
@client.command(brief="Remove name(s) from operation automatically. Takes Year (YYYY), Month(M or MM) and day (D or DD)")
async def removename (ctx, year, month, day, *args) -> None:
  print(year, month, day, args)
  try:
    with open(f"operations-{month}-{year}.pkl", "rb") as f:
      data = pickle.load(f)
  except:
    await ctx.channel.send("Error: File not found")
  
  print(data)
  
  output_str = ""
  for operation in data.keys():
    sub_sect = operation.split(" ")
    if sub_sect[1] == day:
      print(operation)
      data[operation] = None
  
  with open(f"operations-{month}-{year}.pkl", "wb") as f:
    pickle.dump(data, f)
  
  await client.get_channel(1409503885156028416).purge(limit=1)
  
  month_str = calendar.month_name[int(month)]
  embed = tools.embedhandler(
    f"Operations for {month_str} {year}",
    0x154c79,
    client.get_channel(1409503885156028416),
    False,
    None,
    client
  )
  await tools.embedhandler.sendembed(embed, data)

@client.command(brief="Ping in ms")
async def ping(ctx):
  await ctx.send('Pong, {} Ms'.format(round(client.latency * 1000, 2)))

@client.command(brief="Syncs slash commands (Only Nurglwe can use this)")
async def synctree (ctx):
  if ctx.author.id == 220213079944724482:
    resp = await client.tree.sync()
    await ctx.send(f"Commands synced with response {resp}")



# Don't touch below
#keepalive.keep_alive()
token = os.getenv('DSTOKEN')
client.run(token)