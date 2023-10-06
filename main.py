import disnake # Подключаем библиотеку
from disnake.ext import commands, tasks
from config import TOKEN as DSkey, TM_API_KEY as TMkey
import requests
from classes import User
import httpx
import asyncio

intents = disnake.Intents.default() # Подключаем "Разрешения"
intents.message_content = True
# Задаём префикс и интенты
bot = commands.Bot(command_prefix='/', intents=intents) 

dictUsers = dict()

def SearchItemOnTM(hashname):
    return requests.get(f"https://market.csgo.com/api/v2/search-item-by-hash-name?key={TMkey}&hash_name={hashname}").json()
    


# С помощью декоратора создаём первую команду
@bot.slash_command(name="addskin", description="Добавляет скин в базу")
async def addskin(inter, hashname: str):
    try:
        if (dictUsers.get(inter.author.nick)) == None:
            dictUsers[inter.author.nick] = User()
        #skin = inter.message.content.split('/addskin ')
        #if len(hashname) == 2:
            #skin = inter.message.content.split('/addskin ')[1]
        a = SearchItemOnTM(hashname)
        if len(a['data']) == 0:
            await inter.response.send_message('Неверное название скина, скопируйте с https://market.csgo.com')
        else:
            dictUsers[inter.author.nick].addSkin(hashname, float(a['data'][0]['price'])/100)
            await inter.response.send_message(f"Скин {hashname} успешно добавлен. Его стоимость на TM: {float(a['data'][0]['price'])/100}, в Steam: [пока что недоступно]")
        #else:
        #    await inter.response.send_message('Неверный ввод. Попробуйте ввести: ?addskin [Название предмета с https://market.csgo.com как указано в закрепе].')
    except Exception:
        await inter.response.send_message('Что-то пошло не так, попробуйте позже')

@bot.slash_command(name="showskins", description="Показывает скины из базы")
async def showskins(inter):
    try:
        msg = ""
        for skin in dictUsers[inter.author.nick].dictSkins:
            msg = msg + f"{skin}: {dictUsers[inter.author.nick].dictSkins.get(skin)} руб.\n"
        await inter.response.send_message(f"{msg}")
    except Exception:
        await inter.response.send_message('Что-то пошло не так, попробуйте позже')


@tasks.loop(minutes=1)
async def updateprices():
    if len(dictUsers) != 0:
        for user in dictUsers:
            for skin in dictUsers[user].dictSkins:
                dictUsers[user].dictSkins[skin] = SearchItemOnTM(skin)
        print('Цены обновлены')

@bot.event
async def on_ready():
    updateprices.start()

bot.run(DSkey)