import discord
from datetime import timedelta
from discord import Color
import getprices

lasttime = None

intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Loggied in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global lasttime
    if lasttime is None or message.created_at - lasttime <= timedelta(seconds=5):
        lasttime = message.created_at
    
        msg = message.content.lower()
        triggerwords = ['avarice', 'totem', '']
            
        if any(word in msg for word in triggerwords):
            prices = getprices.ck_prices("https://www.cardkingdom.com/mtg/fifth-dawn/avarice-totem")
            report = (
                "**Avarice Totems available** ***right now*** **at** ***www.CardKingdom.com:***\n" +
                "\n*NM:* **" + str(prices['nm']['amount']) + "** in stock **| " + str(prices['nm']['price']) + "** each." +
                "\n" +
                "\n*LP:* **" + str(prices['lp']['amount']) + "** in stock **| " + str(prices['lp']['price']) + "** each." + 
                "\n" +
                "\n*MP:* **" + str(prices['mp']['amount']) + "** in stock **| " + str(prices['mp']['price']) + "** each." + 
                "\n" +
                "\n*HP:* **" + str(prices['hp']['amount']) + "** in stock **| " + str(prices['hp']['price']) + "** each."
                )
            # The await keyword is used to signify that the coroutine should pause execution until the awaited task completes
            reportblock=discord.Embed(title="*BUY NOW!*", description=report, url="https://www.cardkingdom.com/mtg/fifth-dawn/avarice-totem" ,colour=Color.blue(), type='rich')
            reportblock.set_thumbnail(url='https://product-images.tcgplayer.com/fit-in/848x848/filters:quality(1)/11781.jpg')

            await message.channel.send(embed=reportblock)


'''    
    {
        "nm": {"amount": 8, "price": 0.99},
        "lp": {"amount": 8, "price": 0.79},
        "mp": {"amount": 5, "price": 0.59},
        "hp": {"amount": 0, "price": 0.39},
    }
'''

client.run('MTIyMzM2NDc0OTAzMTM3NDg2OA.GnmaRX.yIDWXJyBBzPE6dCUpseJgXb76ycu9TO13I-r9I')