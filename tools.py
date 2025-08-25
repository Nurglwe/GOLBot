import json,discord,os

def addlink(*args):
  a=[]
  for m in args:
    a.append("")

def getjson(path):
  with open(path,"r") as f:
    return json.load(f)

def writejson(path,data):
  with open(path,"w")as f:
    json.dump(data,f)

def getdiscordutils(objects,key):
  return discord.utils.get(objects, id=int(os.getenv("{}".format(key))))

class embedhandler:
  def __init__(self,title,colour,channel,inl,image,client):
    self.title=title
    self.colour=colour
    self.sendto=channel
    self.client=client
    self.inl=inl
    if image != None:
      self.image=image
  async def sendembed(self,args):
    embed=discord.Embed(title=self.title,colour=self.colour)
    try:
      embed.set_image(url=self.image)
    except:
      print("a")
    keys=list(args.keys())
    vals=list(args.values())
    for i in range(len(vals)):
      output_str = ""
      for val in vals[i]:
        output_str = output_str + str(val) + "\n"
      embed.add_field(name=keys[i],value=output_str,inline=self.inl)
    if not(self.sendto is None):
      return await self.sendto.send(embed=embed)
    else:
      return embed
    


class alltheobject:
  def __init__(self,client):
    self.guild=discord.utils.get(client.guilds,id=int(os.getenv("GUILD")))
    self.delc=discord.utils.get(self.guild.channels,id=int(os.getenv("DELC")))
    self.welc=discord.utils.get(self.guild.channels,id=int(os.getenv("WELC")))
