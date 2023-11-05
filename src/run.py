# import discord
# import requests
# from discord.ext import commands, tasks
# from discord.ext.commands import Context
# from discord.embeds import Embed
# from discord.colour import Color
# from configparser import ConfigParser
# import time
# from datetime import datetime


# config = ConfigParser()
# config.read("config.ini")
# token = config.get("bot", "token")

# intents = discord.Intents.default()
# intents.message_content = True
# bot = commands.Bot(command_prefix="!", intents=intents)

# pr_channel = 1169656253639827456
# last_search = 0

# @bot.command(name="ping")
# async def ping(ctx: Context):
#     await ctx.send('pong')

# @bot.event
# async def on_ready():
#     channel = bot.get_channel(pr_channel)
#     await channel.send(f"Bot online {bot.user}")
#     print(f"Bot online {bot.user}")
#     get_new_pull_requests.start()


# # @bot.event
# # async def on_message(message):
# #     if message.author.bot:
# #         return
# #     if "!" in message.content:
# #         channel = bot.get_channel(message.channel.id)
# #         await channel.send("é um comando")


# @bot.command(name="pull_request")
# async def get_pull_requests(ctx: Context):
    # await ctx.send("Buscando pull requests em aberto")
    # pull_requests = requests.get("https://api.github.com/repos/Nicolas734/alura-iac/pulls?state=open").json()

    # for pull_request in pull_requests:
    #     embed: Embed = Embed(
    #         title="Pull request aberto",
    #         description="teste",
    #         url=pull_request["html_url"],
    #     )
    #     await ctx.send(embed=embed)


# @tasks.loop(minutes=1)
# async def get_new_pull_requests():
#     global last_search
    
#     if last_search == 0:
#         last_search = datetime.utcnow()
#     else:
#         pull_requests = requests.get("https://api.github.com/repos/Nicolas734/alura-iac/pulls?state=open&sort=long-running").json()
#         for pull_request in pull_requests:
#             created = datetime.strptime(pull_request["created_at"], "%Y-%m-%dT%H:%M:%SZ")
#             print("last_search: ", last_search)
#             print("created: ",created)
#             if last_search < created:
#                 print("tem novos pull requests")
#             else:
#                 print("não tem pull requests novos")
#         last_search = datetime.utcnow()


# #https://api.github.com/repos/Nicolas734/alura-iac/pulls?state=open
# #https://api.github.com/repos/EquipeGfour/API-5Semestre-OracleAcademy-FrontEnd/pulls?state=open
# bot.run(token)


from bot.bot import DiscordBot

bot = DiscordBot()
bot.run()