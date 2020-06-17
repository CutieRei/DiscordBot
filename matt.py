import discord
from discord.ext import tasks,commands
from discord.utils import get
import random,json

bot = commands.Bot(command_prefix=".")

items = ["Staff","Staff","Gold","Gold","Flour","Flour","Fish","Fish","World Locks","Flower"]

@bot.event
async def on_ready():
	a = bot.get_channel(722381863838023761)
	b = bot.get_channel(722382457902596098)
	print("Joined!")
	ids = [a,b]
	channel = random.choice(ids)
	await channel.send("Hello everyone im back!")
	
@bot.command()
@commands.has_role("SS Tier")
async def new(ctx,name,r:int,g:int,b:int):
	await ctx.guild.create_role(name=name,colour=discord.Colour.from_rgb(r,g,b))
	await ctx.send("Successfully Created!")

@bot.command(aliases=["del","d"])
@commands.has_role("SS Tier")
async def delete(ctx, roleName):
	for i in ctx.guild.roles:
		if i.name == roleName:
			await i.delete()
			await ctx.send(f"{i.name} deleted!")

@bot.command(aliases=["gr"])
@commands.has_role("SS Tier")
async def giverole(ctx, member: discord.Member,role :discord.Role):
	if role.name in [i.name for i in member.roles]:
		await ctx.send(f"{member} already have that role!")
	else:
		await member.add_roles(role)
		await ctx.send(f"Successfully added {role} role to {member}")

@bot.command()
@commands.has_role("SS Tier")
async def dc(ctx):
	card = discord.Embed(
	color=discord.Colour.from_rgb(127,255,127),
	title="Bot has been deactivated",
	description="I will be back!"
	)
	await ctx.send(embed=card)
	await bot.logout()

@bot.command()
async def verify(ctx):
	avatar = ctx.author.avatar_url_as(static_format='png')
	userRole = []
	for i in ctx.author.roles:
		userRole.append(i.name)
	print(userRole)
	getRole = ctx.guild.get_role(722716128333266946)
	card = discord.Embed(
	colour=discord.Colour.from_rgb(255,110,110),
	title="Failed",
	description="You already verified!"
	)
	card.set_thumbnail(url=avatar)
	if str(getRole.name) in userRole:
		await ctx.send(embed=card)
	else:
		with open("balance.json","r+") as f:
			data = json.load(f)
			await ctx.author.add_roles(getRole)
			card.title = "Success"
			card.description="You successfully verified!"
			card.colour=discord.Colour.from_rgb(110,255,100)
			data[ctx.author.name] = 0
			f.seek(0)
			json.dump(data,f,indent=4)
			await ctx.send(embed=card)
	
@bot.command(aliases=["i"])
@commands.has_any_role("SS Tier","subscribers")
async def info(ctx,member:discord.Member=None):
	if member and "SS Tier" in [i.name for i in ctx.author.roles]:
		print()
		avatar = member.avatar_url_as(static_format='png')
		card = discord.Embed(
		colour=member.color,
		title="Info"
		)
		card.set_thumbnail(url=avatar)
		with open("balance.json","r+") as f:
			data = json.load(f)
			userData = data[member.name]
			card.description=f"Name: **{member.name}**\nID: **{member.id}**\nRole: **{member.top_role}**\nBalance: **{userData}** bucks"
			await ctx.send(embed=card)
	
	else:
		print([i.name for i in ctx.author.roles])
		avatar = ctx.author.avatar_url_as(static_format='png')
		card = discord.Embed(
		colour=ctx.author.color,
		title="Info",
		)
		with open("balance.json","r+") as f:
			data = json.load(f)
			card.set_thumbnail(url=avatar)
			userData = data.get(ctx.author.name)
			card.description=f"Name: **{ctx.author.name}**\nID: **{ctx.author.id}**\nRole: **{ctx.author.top_role}**\nBalance: **{userData}** bucks"
			await ctx.send(embed=card)

@bot.command()
@commands.has_role("SS Tier")
async def clear(ctx, amount:int):
	channel = ctx.channel
	deleted = await channel.purge(limit=amount)
	card = discord.Embed(
	title=f"Successfully deleted {len(deleted)} messages",
	colour = discord.Colour.from_rgb(120,255,120)
	)
	await ctx.send(embed=card,delete_after=3)

@bot.command()
@commands.cooldown(1,60,commands.BucketType.member)
@commands.has_any_role("SS Tier","subscribers")
async def get(ctx):
	amount = random.randint(1907,12098)
	word = [f"A guy gave you **{amount}** bucks",f"A begger gave you **{amount}** bucks",f"You found **{amount}** bucks lying around",f"You won **{amount}** bucks",f"Oh? whats this? some nice guy gave you **{amount}** bucks how nice!",f"Elon musk: \"take my **{amount}** bucks loser\""]
	sentence = random.choice(word)
	card = discord.Embed(
	colour=discord.Colour.from_rgb(20,255,20),
	title=sentence
	)
	card.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url_as(static_format='png'))
	with open("balance.json","r+") as f:
		data = json.load(f)
		data[ctx.author.name] += amount
		f.seek(0)
		json.dump(data,f,indent=4)
		await ctx.send(embed=card)
		f.truncate()


@bot.command()
@commands.has_any_role("subscribers","SS Tier")
async def give(ctx,member: discord.Member,amount:int):
	with open("balance.json","r+") as f:
		data = json.load(f)
		authorCash = data.get(ctx.author.name)
		card = discord.Embed(
		colour=discord.Colour.from_rgb(255,20,20),
		title="Failed",
		description="You do not have enough balance lol"
		)
		card.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url_as(static_format='png'))
		if amount > authorCash:
			await ctx.send(embed=card)
		else:
			card.colour=discord.Colour.from_rgb(20,255,20)
			card.title="Success"
			card.description=f"Successfully given **{amount}** bucks to {member.name}"
			data[ctx.author.name] -= amount
			data[member.name] += amount
			f.seek(0)
			json.dump(data,f,indent=4)
			await ctx.send(embed=card)
			f.truncate()

@bot.command(aliases=["cash"])
@commands.has_role("SS Tier")
async def cashed(ctx,member:discord.Member,amount:int):
	with open("balance.json","r+") as f:
		data = json.load(f)
		data[member.name] += amount
		card = discord.Embed(
		colour=discord.Colour.from_rgb(20,255,20),
		title="Success",
		description=f"Successfully given {amount} to {member.name}"
		)
		card.set_author(name=bot.user.name,icon_url=bot.user.avatar_url)
		await ctx.send(embed=card)
		f.seek(0)
		json.dump(data,f,indent=4)
		f.truncate()

@bot.command(aliases=["loan","pay"])
@commands.has_role("SS Tier")
async def uncashed(ctx,member:discord.Member,amount:int):
	with open("balance.json","r+") as f:
		card = discord.Embed(
		colour=ctx.author.color,
		title="Success",
		description=f"Successfully decreased **{member.name}** by **{amount}**"
		)
		card.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url_as(static_format='png'))
		data = json.load(f)
		data[member.name] -= amount
		if data[member.name] < 0:
			data[member.name] = 0
		else:
			pass
		f.seek(0)
		json.dump(data,f,indent=4)
		await ctx.send(embed=card)
		f.truncate()



@bot.event
async def on_command_error(ctx,error):
	if isinstance(error, commands.CommandOnCooldown):
		remain = error.retry_after
		minute = 0
		hour = 0
		if remain >= 60:
			remain -= 60
			minute += 1
		if minute >= 60:
			minute -= 60
			hour += 1
		card = discord.Embed(
		title=f"You need to wait **{hour}h** **{minute}m** **{int(remain)}s** to use the commands again!",
		colour=discord.Colour.from_rgb(255,20,20)
		)
		await ctx.send(embed=card)
	else:
		raise error
	

bot.run('NzIyMzg3MzU1MTA0OTY4NzM0.XunAUg.ERREHByXW0ciKivJHa7ZX0IL54g')