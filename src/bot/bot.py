import requests

from discord import Intents, Interaction, ButtonStyle, InteractionType
from discord.ext.commands import Bot, Context
from discord.embeds import Embed
from discord.ext import commands, menus
from utils.config import Config
from discord.ui import View, Button, button


import discord

class DiscordBot():
    def __init__(self, config: Config = None):
        self._config = (config or Config())
        self._bot = self.create_client()
        self._load_configs()
        self.add_events()
        self.add_commands()

    def _load_configs(self):
        self._token = self._config.g.get("bot", "token")


    def init_atributes(self):
        self._repository: str = ""


    def create_client(self) -> Bot:
        intents = Intents.default()
        intents.message_content = True
        bot = Bot(command_prefix="!", intents=intents)
        return bot

    def add_events(self):
        @self._bot.event
        async def on_ready():
            print("ola")

    def add_commands(self):
        @self._bot.command(name="ping")
        async def ping(ctx: Context):
            await ctx.send('pong')

        @self._bot.command(name="pull_request")
        async def request_last_pull_request(ctx: Context):
            await ctx.send("Buscando pull requests em aberto")
            pull_requests = requests.get("https://api.github.com/repos/Nicolas734/alura-iac/pulls?state=open").json()

            for pull_request in pull_requests:
                embed: Embed = Embed(
                    title="Pull request aberto",
                    description="teste",
                    url=pull_request["html_url"],
                )
                await ctx.send(embed=embed)

        @self._bot.command(name="config")
        # async def configs_options(ctx: Context):

        async def _button(ctx: commands.Context):  # Altere de Interaction.CommandContext para commands.Context
            # view = ConfigMenu()
            button = Button(label="Clique")
            async def button_callback(interaction:discord.Interaction):
                await interaction.response.edit_message(content="Hello", view=None)
                await interaction.followup.send("aaaa")
            button.callback = button_callback
            view = View()
            view.add_item(button)
            view.
            await ctx.send("hi", view=view)



    def run(self):
        try:
            self._bot.run(self._token)
        except Exception as error:
            print(error)


# class ConfigMenu(View):
#     def __init__(self) -> None:
#         super().__init__()

#     @button(label="Clique aqui", style=discord.ButtonStyle.blurple)
#     async def menu(self, button:discord.ui.Button, interarion:discord.Interaction):
#         await interarion.reponse.send_message("CLIQUEI")
    
    # @button(label="Menu de opções", style=discord.ButtonStyle.blurple)
    # async def menu(self, button:discord.ui.Button, interarion:discord.Interaction):
    #     embed = Embed(color=discord.Color.random())
    #     embed.set_author(name="Editar")
    #     embed.add_field(name="aaa", value="vbbcv")
    #     await interarion.response.edit_message(embed=embed)
        
        

