#Made by k0lp aka api_cats in early 2026
import discord
import asyncio
import aiohttp
from datetime import datetime


intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
session = None
url_IL = 'https://api.rolimons.com/items/v2/itemdetails'
url_GRT = "https://api.rolimons.com/tradeads/v1/getrecentads"
urlITN ="https://api.rolimons.com/itemthumbs/v1/thumbssm"

#Change into ur bot emoji ids
rolimons_tags = {
    1: "<:demand:1463574868648792321>", 
    2: "<:rares:1463574870238695667>",
    3: "<:robux:1463574865343942850>",
    4: "<:any:1463574872570466356>",
    5: "<:upgrade:1463574864152494121>",
    6: "<:downgrade:1463574862886076551>",
    7: "<:rap:1463574867977834761>",
    8: "<:wishlist:1463574866409029796>",
    9: "<:projecteds:1463574873686278358>",
    10: "<:adds:1463574861736575100>"
    }

#Rolimons Item List
async def itemlist():
    async with session.get(url_IL) as responseIL:
        return await responseIL.json()

#Rolimon TradeAds
async def adsniper():
    trade_ids = []
    reload_time = 0
    global res_il
    while True:
        found_trades = []
        async with session.get(url_GRT) as responseRTA:
            ResRTA = await responseRTA.json()
        if responseRTA.status != 200:
            print("\nStatus:",responseRTA.status)
            print(responseRTA)
            print(ResRTA)
        if ResRTA.get("success") == True:
            print(f"{datetime.now()} Loading Trade Ads")
            for tradead in ResRTA["trade_ads"]:
                if tradead[4].get("robux") == None:
                    continue

                if tradead[0] not in trade_ids:
                    print(f"Robux: Found {tradead[3]} {tradead[0]} {tradead[4]['robux']}")
                    found_trades.append(tradead)
                    trade_ids.append(tradead[0])
                    Robux = tradead[4]["robux"]
                    role_ping = ""
                    # REPLACE WITH UR OWN CHANNEL IDS/RANK IDS
                    # REPLACE WITH UR OWN CHANNEL IDS/RANK IDS
                    # REPLACE WITH UR OWN CHANNEL IDS/RANK IDS
                    channel =  bot.get_channel(1459645020268138669) 
                    if Robux < 10000:
                        channel =  bot.get_channel(1463553756590244038)
                        role_ping = 1463593833035202623 
                    elif Robux < 25000:
                        channel =  bot.get_channel(1463552738972401746)
                        role_ping = 1463593850340774101
                    elif Robux < 50000:
                        channel =  bot.get_channel(1463552760824729745)
                        role_ping = 1463593857483669710 
                    elif Robux < 100000:
                        channel =  bot.get_channel(1463552783792869419)
                        role_ping = 1463593858066677873
                    elif Robux < 250000:
                        channel =  bot.get_channel(1463552808375681228)
                        role_ping = 1463593858603684003
                    elif Robux < 500000:
                        channel =  bot.get_channel(1463552842420977757)
                        role_ping = 1463594018511523964
                    elif Robux >= 500000:
                        channel =  bot.get_channel(1463552912147091552)
                        role_ping = 1463594028322000969
                    # REPLACE WITH UR OWN CHANNEL IDS/RANK IDS
                    # REPLACE WITH UR OWN CHANNEL IDS/RANK IDS
                    # REPLACE WITH UR OWN CHANNEL IDS/RANK IDS
                    
                    #Offered Items / Their Side
                    
                    embed_text = (f"<@&{role_ping}> <:robux_icon:1463578277594661060> {format(Robux, ',')}")
                    Offr=""
                    TotalRapOfr = 0
                    TotalValueOfr = 0
                    for item in tradead[4]["items"]:
                        special_type=""
                        item_data = res_il["items"].get(str(item))
                        if item_data:
                            TotalValueOfr += item_data[4]
                            TotalRapOfr += item_data[2]
                            if item_data[1] == "":
                                name = item_data[0]
                            else:
                                name = item_data[1]
                            if item_data[7] == 1:
                                special_type += "<:projecteds_icon:1463574858699903170>"
                            if item_data[9] == 1:
                                special_type += "<:rares_icon:1463574860314972190>"
                            Offr+=(f'- [{name}](https://www.rolimons.com/item/{item}) {special_type} | {format(item_data[4], ",")}\n')
                    Offr +=(f"- <:robux_icon:1463578277594661060> {Robux}")

                    #Requested Items / Your Side
                    Req=""
                    TotalRapReq = 0
                    TotalValueReq = 0
                    if tradead[5].get("items"):
                        for item in tradead[5]["items"]:
                            special_type=""
                            item_data = res_il["items"].get(str(item))
                            if item_data:
                                TotalValueReq += item_data[4]
                                TotalRapReq += item_data[2]
                                if item_data[1] == "":
                                    name = item_data[0]
                                else:
                                    name = item_data[1]
                                if item_data[7] == 1:
                                    special_type += "<:projecteds_icon:1463574858699903170>"
                                if item_data[9] == 1:
                                    special_type += "<:rares_icon:1463574860314972190>"
                                Req+=(f'- [{name}](https://www.rolimons.com/item/{item}) {special_type} | {format(item_data[4], ",")}\n')

                    #Start of Embed
                    embed = discord.Embed(
                        title=tradead[3],
                        url=f"https://www.roblox.com/users/{tradead[2]}/profile",
                        color=0x9b59b6)
                    view = TradeButton(trlink=f"https://www.roblox.com/users/{tradead[2]}/trade", tradlink=f"https://www.rolimons.com/tradead/{tradead[0]}", rolilink=f"https://www.rolimons.com/player/{tradead[2]}")
                    embed.add_field(name=f"Their side {format(TotalValueOfr, ',')}", value=Offr, inline=False),
                    i = 0
                    if tradead[5].get("tags"):
                        embed_tags=""
                        for tag in tradead[5]["tags"]:
                            if i >= 1:
                                embed_tags += f" {rolimons_tags.get(tag)} "
                            else:
                                i += 1
                                embed_tags += f"- {rolimons_tags.get(tag)} "
                        if TotalValueReq > 0:
                            embed.add_field(name=f"Your side {format(TotalValueReq, ',')}", value=f"{Req}{embed_tags}", inline=False),
                        else:
                            embed.add_field(name=f"Your side", value=f"{Req}{embed_tags}", inline=False),
                    else:
                        embed.add_field(name=f"Your side {format(TotalValueReq, ',')}", value=Req, inline=False),
                    try:
                        await channel.send(content=f"{embed_text}", embed=embed, view=view)
                    except Exception as e:
                        print(f"### {datetime.now()} Discord error - Couldnt send, trying again in 5 seconds... // {e}")
                        await asyncio.sleep(5)
                        try:
                            await channel.send(content=f"{embed_text}", embed=embed, view=view)
                            print("### Embed sent!")
                        except Exception as e:
                            print(f"### {datetime.now()} Discord error again - Embed skipped. // {e}")
                        continue
                else:
                    break
            if found_trades == []:
                print("Robux: Couldnt find any matching Trade Ads!")
        else:
            print(f"## {datetime.now()} Uh oh! Problem with Rolimons getrecentads api!",ResRTA)

        if reload_time == 60:
            if len(trade_ids) > 1000:
                trade_ids = trade_ids[-500:] #clears up RAM :D
            res_il = await itemlist()
            print(f"$$ Reloaded Item List {datetime.now()}")
            reload_time = 0
        await asyncio.sleep(60)
        reload_time += 1


#I ChatGTPed these buttons :sob: Rest of code mainly done by me tho
class TradeButton(discord.ui.View):
    def __init__(self, tradlink: str, trlink: str, rolilink: str):
        super().__init__(timeout=None)
        self.add_item(
            discord.ui.Button(
                label="Send",
                url=trlink,
                style=discord.ButtonStyle.link
            )
        )
        self.add_item(
            discord.ui.Button(
                label="Trade Ad",
                url=tradlink,
                style=discord.ButtonStyle.link
            )
        )
        self.add_item(
            discord.ui.Button(
                label="Rolimons",
                url=rolilink,
                style=discord.ButtonStyle.link
            )
        )

@bot.event
async def on_ready():
    global res_il, session
    session = aiohttp.ClientSession()
    res_il = await itemlist()
    print("Item List Loaded!\n")
    print("Starting Trade Ads Loader...")
    asyncio.create_task(adsniper())

#Enter ur bot token
bot.run("totally_real_discord_token")