import discord.object
import discord,os,tools, calendar, pickle, datetime
from discord.ext import commands, tasks
from discord import app_commands
from typing import Optional
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="->",intents=intents, guilds=True, members=True)


'''

Below is events

'''

@tasks.loop(hours = 24)
async def check_date(client):
  current_date = datetime.date.today()
  current_month = current_date.month
  current_year = current_date.year

  if current_date.day == 20:
    if current_month > 11:
      current_month = 0
      current_year += 1
    try:
      await makeschedule(None, current_date.year, current_month + 1)
    except:
      print("Error making new schedule")

  if current_date.day == 1:
    if current_month < 2:
      current_month = 13
      current_year -= 1
    try:
      await movepost (None, current_year, current_month-1)
    except:
      print("Error moving schedule")

@client.event
async def on_ready():
  print("Ready")
  check_date.start(client)

'''

Below is commands

'''


@client.tree.command(
    name="create-schedule", 
    description="Creates a table of thursdays and sundays in a month"
  )
@app_commands.describe(month= "Month (1-12)", year="Year")
#@client.command(brief="Create an orbat for a given year (YYYY) and month (M or MM)")
async def makeschedule(interaction: discord.Interaction, year: int, month: int) -> None:
  standard_op_days = {}
  print(month, year)
  print()
  if os.path.exists(f"./archives/operations-{month}-{year}.pkl"):
    await interaction.response.send_message("Error file already exists. Please delete it or edit it.")
    return
  
  if not(month < 1 or month > 12):
    month_str = calendar.month_name[int(month)]
    first_day, num_days = calendar.monthrange(year, month)
    print(first_day, num_days)
    week_day = first_day
    for day in range(1, num_days + 1):
      week_day += 1
      if week_day  == 4:
        standard_op_days.update({f"{calendar.day_name[week_day-1]} {day} <:Training:1173686838926512199>": [None, None]})
      if week_day >= 7:
        standard_op_days.update({f"{calendar.day_name[week_day-1]} {day} <:Mission:1173686836451885076>": [None, None]})
        week_day = 0

    embed = tools.embedhandler(
      f"Operations for {month_str} {year}",
      0x154c79,
      client.get_channel(1409503885156028416),
      False,
      None,
      client
      )
    mesg = await tools.embedhandler.sendembed(embed, standard_op_days)

    standard_op_days["message id"] = mesg.id
    standard_op_days["channel id"] = 1409503885156028416
    with open(f"./archives/operations-{month}-{year}.pkl", "wb") as f:
      pickle.dump(standard_op_days, f)
    print(standard_op_days)
    await interaction.response.send_message("Operation completed successfully")
  else:
    await interaction.response.send_message("Error: Month input is less than 1 or greater than 12")
    return

@client.tree.command(
    name="add-developer", 
    description="Adds a developer(s) to an operation day")
@app_commands.describe(month= "Month (1-12)", year="Year", args="Targetted users")
#@client.command(brief="Add name(s) from operation automatically. Takes Year (YYYY), Month(M or MM), day (D or DD) and optionally targetted users")
async def adddev (interaction: discord.Interaction, year:int, month:int, day:str, args: Optional[str]= None) -> None:
  print(year, month, day, args)
  if args is None:
    target = [f"<@{interaction.user.id}>"]
  else:
    args = args.split(">")
    target = [user.strip()+">" for user in args]

  try:
    with open(f"./archives/operations-{month}-{year}.pkl", "rb") as f:
      data = pickle.load(f)
  except:
    await interaction.response.send_message("Error: File not found")
    return
  
  for operation in data.keys():
    sub_sect = operation.split(" ")
    if sub_sect[1] == day:
      print(data[operation][0])
      output_str = data[operation][0]
      if output_str == None:
        output_str = ''
      for user in target:
        if user not in output_str:
          print(user)
          output_str = str(output_str) + " " + user.strip()
      data[operation] = [output_str, data[operation][1]] 

  with open(f"./archives/operations-{month}-{year}.pkl", "wb") as f:
    pickle.dump(data, f)
  
  sanitised_data = data.copy()
  sanitised_data.pop("message id")
  sanitised_data.pop("channel id")

  month_str = calendar.month_name[int(month)]
  embed = tools.embedhandler(
    f"Operations for {month_str} {year}",
    0x154c79,
    None,
    False,
    None,
    client
  )
  embed = await tools.embedhandler.sendembed(embed, sanitised_data)
  channel = client.get_channel(data["channel id"])
  message = await channel.fetch_message(data["message id"])
  await message.edit(embed=embed)
  await interaction.response.send_message("Operation completed successfully")


@client.tree.command(
    name="add-mission-name", 
    description="Adds a mission(s) to an operation day")
@app_commands.describe(month= "Month (1-12)", year="Year", args="Mission name")
#@client.command(brief="Add mission name(s) from operation automatically. Takes Year (YYYY), Month(M or MM), day (D or DD) and optionally targetted users")
async def addmission (interaction: discord.Interaction, year:int, month:int, day:str, args: str) -> None:
  print(year, month, day, args)
  try:
    with open(f"./archives/operations-{month}-{year}.pkl", "rb") as f:
      data = pickle.load(f)
  except:
    await interaction.response.send_message("Error: File not found")
    return
  
  for operation in data.keys():
    sub_sect = operation.split(" ")
    if sub_sect[1] == day:
      print(data[operation][1])
      data[operation] = [data[operation][0], args] 

  with open(f"./archives/operations-{month}-{year}.pkl", "wb") as f:
    pickle.dump(data, f)

  sanitised_data = data.copy()
  sanitised_data.pop("message id")
  sanitised_data.pop("channel id")
  print(sanitised_data)
  print(data)

  month_str = calendar.month_name[int(month)]
  embed = tools.embedhandler(
    f"Operations for {month_str} {year}",
    0x154c79,
    None,
    False,
    None,
    client
  )
  embed = await tools.embedhandler.sendembed(embed, sanitised_data)
  channel = client.get_channel(data["channel id"])
  message = await channel.fetch_message(data["message id"])
  await message.edit(embed=embed)
  await interaction.response.send_message("Operation completed successfully")


@client.tree.command(
    name="remove-developer", 
    description="Adds a developer(s) to an operation day")
@app_commands.describe(month= "Month (1-12)", year="Year", args="Targetted user")
#@client.command(brief="Remove name(s) from operation automatically. Takes Year (YYYY), Month(M or MM) and day (D or DD)")
async def removedev (interaction: discord.Interaction, year:int, month:int, day:str, args: Optional[str]= None) -> None:
  print(year, month, day, args)
  if args is None:
    target = [f"<@{interaction.user.id}>"]
  else:
    args = args.split(">")
    target = [user+">" for user in args]
  try:
    with open(f"./archives/operations-{month}-{year}.pkl", "rb") as f:
      data = pickle.load(f)
  except:
    await interaction.response.send_message("Error: File not found")
    return
  print(target)
  print(data)
  
  output_str = ""
  for operation in data.keys():
    sub_sect = operation.split(" ")
    if sub_sect[1] == day:
      print(operation)

      users = data[operation][0].split(" ")
      print(users)
      for user in target:
        if user != ">":
          print(user)
          try:
            users.remove(user)
          except:
            print("Error")
      for user in users:
        if user != '':
          output_str = output_str + user.strip() + " "
      print(output_str)
      if not output_str:
        output_str = None
      data[operation][0] = output_str
  
  with open(f"./archives/operations-{month}-{year}.pkl", "wb") as f:
    pickle.dump(data, f)

  sanitised_data = data.copy()
  sanitised_data.pop("message id")
  sanitised_data.pop("channel id")
  print(sanitised_data)  

  month_str = calendar.month_name[int(month)]
  embed = tools.embedhandler(
    f"Operations for {month_str} {year}",
    0x154c79,
    None,
    False,
    None,
    client
  )
  print(data)
  embed = await tools.embedhandler.sendembed(embed, sanitised_data)
  channel = client.get_channel(data["channel id"])
  message = await channel.fetch_message(data["message id"])
  await message.edit(embed=embed)
  await interaction.response.send_message("Operation completed successfully")


@client.tree.command(
    name="remove-mission-name", 
    description="Removes a mission(s) from an operation day")
@app_commands.describe(year="Year", month= "Month (1-12)", day="Day")
#@client.command(brief="Remove mission name(s) from operation automatically. Takes Year (YYYY), Month(M or MM) and day (D or DD)")
async def removemission (interaction: discord.Interaction, year:int, month:int, day:str) -> None:
  print(year, month, day)
  try:
    with open(f"./archives/operations-{month}-{year}.pkl", "rb") as f:
      data = pickle.load(f)
  except:
    await interaction.response.send_message("Error: File not found")
    return

  print(data)
  
  output_str = ""
  for operation in data.keys():
    sub_sect = operation.split(" ")
    if sub_sect[1] == day:
      print(operation)
      data[operation][1] = None

  with open(f"./archives/operations-{month}-{year}.pkl", "wb") as f:
    pickle.dump(data, f)

  sanitised_data = data.copy()
  sanitised_data.pop("message id")
  sanitised_data.pop("channel id")
  print(sanitised_data)  

  month_str = calendar.month_name[int(month)]
  embed = tools.embedhandler(
    f"Operations for {month_str} {year}",
    0x154c79,
    None,
    False,
    None,
    client
  )
  print(data)
  embed = await tools.embedhandler.sendembed(embed, sanitised_data)
  channel = client.get_channel(data["channel id"])
  message = await channel.fetch_message(data["message id"])
  await message.edit(embed=embed)
  await interaction.response.send_message("Operation completed successfully")


@client.tree.command(
    name="move-post", 
    description="Moves a post to the archives channel")
@app_commands.describe(year="Year", month= "Month (1-12)")
#@client.command(brief="Moves entire schedule post to an archive")
async def movepost (interaction: discord.Interaction, year:int, month:int) -> None:
  print(year, month)
  try:
    with open(f"./archives/operations-{month}-{year}.pkl", "rb") as f:
      data = pickle.load(f)
  except:
    await interaction.response.send_message("Error: File not found")
    return

  channel = client.get_channel(data["channel id"])
  message = await channel.fetch_message(data["message id"])
  await message.delete()

  print(data)
  data.pop("message id")
  data.pop("channel id")
  
  month_str = calendar.month_name[int(month)]
  embed = tools.embedhandler(
    f"Operations for {month_str} {year}",
    0x154c79,
    client.get_channel(1409529449120268298),
    False,
    None,
    client
  )
  mesg = await tools.embedhandler.sendembed(embed, data)

  data["message id"] = mesg.id
  data["channel id"] = 1409529449120268298
  with open(f"./archives/operations-{month}-{year}.pkl", "wb") as f:
    pickle.dump(data, f)
  print(data)
  await interaction.response.send_message("Operation completed successfully")


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