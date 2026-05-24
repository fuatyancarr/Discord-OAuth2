import discord
import os
import json
from discord.ext import commands
import requests 
import keygen

# --- PORT VE API AYARI (RENDER UYUMLU) ---
PORT = os.environ.get("PORT", "1337")
# Eğer sistem Render'da çalışıyorsa Render'ın linkini çeker, yoksa lokale döner
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL", f"http://127.0.0.1:{PORT}")
api = RENDER_EXTERNAL_URL

with open("config.json", "r") as f:
    config = json.load(f)

tkn = config["token"]
offline_token = config["offline_token"]
online_token = config["online_token"]

# Intents ayarını all yerine default + message_content yapıyoruz (Çökme riskini önlemek için)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True 

client = commands.Bot(command_prefix=(["-", "."]), intents=intents)

@client.event
async def on_ready():
    # os.system satırı Render loglarını bozduğu için kaldırıldı.
    guilds_count = len(client.guilds)
    print(f"Connected; {client.user} | Guilds count: {guilds_count}")
    

@client.event
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound):
        return
    em = discord.Embed(title="Error", description=f"```{error}```", color=0x00000)
    await ctx.send(embed=em, delete_after=5)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def status(ctx, guild_id= None):
    msg = await ctx.send("Fetching.....")
    if guild_id == None:
        if not os.path.exists("running.txt"):
            return await msg.edit(content="No running tasks.")
        f = open("running.txt", "r").read().splitlines()
        if len(f) == 0:
            return await msg.edit(content="No running tasks.")
        embed = discord.Embed(title="Running Tasks", description="", color=0x00000)
        for guild in f:
            total_path = f"guilds/{guild}-total.txt"
            added_path = f"guilds/{guild}.txt"
            
            total = open(total_path, "r").read() if os.path.exists(total_path) else "1"
            added = open(added_path, "r").read() if os.path.exists(added_path) else "0"
            
            remaining = int(total) - int(added)
            speed_per_minute = 60
            estimated_minutes = int(remaining) / speed_per_minute
            hours = int(estimated_minutes / 60)
            minutes = int(estimated_minutes % 60)
            seconds = int((estimated_minutes % 1) * 60)
            if hours > 0:
                estimated_time = f"{hours}h {minutes}m {seconds}s"
            else:
                estimated_time = f"{minutes}m {seconds}s"
            added_percent = int((int(added) / int(total)) * 100) if int(total) > 0 else 0
            remaining_percent = int((int(remaining) / int(total)) * 100) if int(total) > 0 else 0
            embed.description += f"Guild: `{guild}`\nAdded: `{added}/{total} {added_percent}%`\nRemaining: `{remaining} {remaining_percent}%`\nSpeed: `60/m`\nETA: `{estimated_time}`\n\n"
        await ctx.send(embed=embed)
    else:
            if not os.path.exists("running.txt"):
                return await ctx.send("No Running task found.")
            f = open("running.txt", "r").read().splitlines()
            if guild_id not in f:
                return await ctx.send("No Running task found for guild: " + guild_id)
            else:
                total_path = f"guilds/{guild_id}-total.txt"
                added_path = f"guilds/{guild_id}.txt"
                total = open(total_path, "r").read() if os.path.exists(total_path) else "1"
                added = open(added_path, "r").read() if os.path.exists(added_path) else "0"
                
                remaining = int(total) - int(added)
                speed_per_minute = 60
                estimated_minutes = int(remaining) / speed_per_minute
                hours = int(estimated_minutes / 60)
                minutes = int(estimated_minutes % 60)
                seconds = int((estimated_minutes % 1) * 60)
                if hours > 0:
                    estimated_time = f"{hours}h {minutes}m {seconds}s"
                else:
                    estimated_time = f"{minutes}m {seconds}s"
                added_percent = int((int(added) / int(total)) * 100) if int(total) > 0 else 0
                remaining_percent = int((int(remaining) / int(total)) * 100) if int(total) > 0 else 0
                em = discord.Embed(title=f"Status - {guild_id}", description="", color=0x00000)
                em.description += f"Guild: `{guild_id}`\nAdded: `{added}/{total} {added_percent}%`\nRemaining: `{remaining} {remaining_percent}%`\nSpeed: `60/m`\nETA: `{estimated_time}`\n\n"
                await ctx.send(embed=em)

        
@client.command(aliases=['gen'])
async def generate(ctx, key_type:str, start:int, total:int, uses=None):
    if ctx.author.id != 1124544216454926398:
        return await ctx.send("unauthorized")
    key, url = keygen.generate_key(key_type=key_type, total=total, start=start, uses=uses)
    em = discord.Embed(title="Key Generated", description=f"Key: `{key}`\nType: `{key_type}`\nAmount: `{total}`\n\nBot Invite: [Click here to Invite]({url})\n\nNote: ```It will start automatically as soon as you add the bot, if didn't start make sure the bot is in server and send command .redeem```", color=0x00000)
    await ctx.send(embed=em)
    
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def redeem(ctx, key=None, server_id=None):
    await ctx.message.delete()
    if key == None or server_id == None:
        return await ctx.send("usage: .redeem <key> <server-id>")
    url = f"{api}/callback?code=ded&state={key}&guild_id={server_id}&permissions=1"
    r = requests.get(url)
    try:
        response_data = r.json()
    except:
        response_data = r.text
    em = discord.Embed(description=f"{response_data}", color=0x00000)
    return await ctx.send(embed=em)

@client.command()
async def ltc(ctx): 
    await ctx.send("LeUUjdR44S9314Y3LQUW1JeS4HCsDt6mK1")
    await ctx.send("ltc addy ^^")

@client.command()
async def mail(ctx): 
    await ctx.send("**requested1337@protonmail.com**")
    await ctx.send("Coinbase / Binance mail ^")

@client.command()
async def upi(ctx):
    await ctx.send("exploit@fam")

@client.command()
async def calc(ctx, *, expression):
    if ctx.author.id != 1124544216454926398:
        return await ctx.send("unauthorized")
    print(ctx.author)
    # Güvenli eval işlemi için basit koruma
    sol = eval(expression, {"__builtins__": None}, {})
    await ctx.send(f"{expression} = {sol}")

@client.command()
async def ping(ctx):
    await ctx.send(f"{round(client.latency * 1000)}ms")

@client.command()
async def vt(ctx, *, vouch):
    msg = await ctx.send(f"`+rep <@468818639588687873> {vouch}`")
    await msg.reply("> copy paste this in <#1119597593048121404> channel.")

@client.command()
async def leave(ctx, type:str, guild: str):
    if ctx.author.id != 1124544216454926398:
        return await ctx.send("unauthorized")
    if type == "offline": 
        r = requests.delete("https://canary.discord.com/api/v9/users/@me/guilds/"+guild, headers={"Authorization": "Bot "+offline_token})
        try:
            jsonx = r.json()
        except:
            jsonx = ""
        em = discord.Embed(description=f"{r.status_code} | {jsonx}", color=0x00000)
        return await ctx.send(embed=em)
    elif type == "online":
        r = requests.delete("https://canary.discord.com/api/v9/users/@me/guilds/"+guild, headers={"Authorization": "Bot "+online_token})
        try:
            jsonx = r.json()
        except:
            jsonx = ""
        em = discord.Embed(description=f"{r.status_code} | {jsonx}", color=0x00000)
        return await ctx.send(embed=em)
    else:
        return await ctx.send("Invalid type, type can be either offline or online.")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def stock(ctx):
    offline = len(open("offline.txt", "r").read().splitlines()) if os.path.exists("offline.txt") else 0
    online = len(open("online.txt", "r").read().splitlines()) if os.path.exists("online.txt") else 0
    em = discord.Embed(title="Stock", description=f"Offline: `{offline}`\nOnline: `{online}`", color=0x00000)
    await ctx.send(embed=em)

client.run(tkn)
@client.command()
async def mail(ctx): 
    await ctx.send("**requested1337@protonmail.com**")
    await ctx.send("Coinbase / Binance mail ^")

@client.command()
async def upi(ctx):
    await ctx.send("exploit@fam")

@client.command()
async def calc(ctx, *, expression):
    if ctx.author.id != 1124544216454926398:
        return await ctx.send("unauthorized")
    # print(expression)
    print(ctx.author)
    sol = eval(expression)
    await ctx.send(f"{expression} = {sol}")

@client.command()
async def ping(ctx):
    await ctx.send(f"{round(client.latency * 1000)}ms")

@client.command()
async def vt(ctx, *, vouch):
    msg = await ctx.send(f"`+rep <@468818639588687873> {vouch}`")
    await msg.reply("> copy paste this in <#1119597593048121404> channel.")

@client.command()
async def leave(ctx, type:str, guild: str):
    if ctx.author.id != 1124544216454926398:
        return await ctx.send("unauthorized")
    if type == "offline": 
        # remove_tracking(guild)
        r = requests.delete("https://canary.discord.com/api/v9/users/@me/guilds/"+guild, headers={"Authorization": "Bot "+offline_token})
        try:
            jsonx = r.json()
        except:
            jsonx = ""
        em = discord.Embed(description=f"{r.status_code} | {jsonx}", color=00000)
        return await ctx.send(embed=em)
    elif type == "online":
        try:
            jsonx = r.json()
        except:
            jsonx = ""
        r = requests.delete("https://canary.discord.com/api/v9/users/@me/guilds/"+guild, headers={"Authorization": "Bot "+online_token})
        em = discord.Embed(description=f"{r.status_code} | {jsonx}", color=00000)
        return await ctx.send(embed=em)
    else:
        return await ctx.send("Invalid type, type can be either offline or online.")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def stock(ctx):
    offline = len(open("offline.txt", "r").read().splitlines())
    online = len(open("online.txt", "r").read().splitlines())
    em = discord.Embed(title="Stock", description=f"Offline: `{offline}`\nOnline: `{online}`", color=00000)
    await ctx.send(embed=em)


client.run(tkn)
