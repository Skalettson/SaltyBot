import disnake
import qrcode
from disnake.ext import commands

import sqlite3
#command_prefix можно ставить любой, какой вам нужен.
bot = commands.Bot(command_prefix = "!",
                   intents = disnake.Intents.all(),
                   help_command = None,
                   test_guilds = [213213123231123123, 123123232142312412],
                   activity = disnake.Activity(name="!хелпа - YOUR_BOT",
                                               type=disnake.ActivityType.streaming,
                                               status = disnake.Status.streaming,
                                               url="https://localhost/",
                                               details="https://localhost/",

                    )
)
#Подключаем sqlite3
con = sqlite3.connect('sample.db')
cur = con.cursor()

@bot.event
async def on_ready():
    print(f"Ботяра {bot.user} подключён к Дискорду и готов работать!")
    #Создаём БД пользователей
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INT,
        name TEXT,
        warns INT)
    """)
    con.commit()
    #Добавляем пользователей в БД
    for guild in bot.guilds:
        for member in guild.members:
            if cur.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cur.execute(f'INSERT INTO users VALUES ({member.id}, "{member}", 0)')
                con.commit()
            else:
                pass
#Команды админов прописаны в коге. Можете не обращать внимания на них.
@bot.command(name="хелпани", aliases=["хелпа"])
async def help(ctx) -> None:
    await ctx.reply("**Help -  чем помочь?**\nДоступные команды: \n**!хелпа** \n**!клир** \nКоманды админов: \n**/app** \n**/warns** \n**/mywarns** \n**/warn** \n**/unwarn**")

@bot.command(name="клир", aliases=["очистка"])
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Очищено: {amount} \n**YOUR_BOT**")

@bot.command(name="qrcode", aliases=["qr", "code"])
async def qrc(ctx, code: str):
    img = qrcode.make('https://localhost')

    img.save("img/qrcode.png")

    await ctx.send(file=disnake.File(fp="/qrcode.png"))



token = open('token.cfg', 'r').readline()
bot.run(token)