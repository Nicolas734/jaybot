import requests

from discord import Intents, Interaction, ButtonStyle, InteractionType
from discord.ext.commands import Bot, Context
from discord.embeds import Embed
from discord.ext import commands
from utils.config import Config
from discord.ui import View, Button, button


import discord



class DiscordBot():
    def __init__(self, config: Config = None):
        self._config = (config or Config())
        self._bot : Bot= self.create_client()
        self._load_configs()
        self.init_atributes()
        self.add_events()
        self.add_commands()

    def _load_configs(self):
        self._token = self._config.g.get("bot", "token")


    def init_atributes(self):
        self._repository: str = ""
        self._user: str = ""


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
                    title="Pull request: [{}]".format(pull_request["title"]),
                    description='''Descriçaõ: {} \nCriado: {}\n Ultimo update: {}'''.format(pull_request["body"], pull_request["created_at"], pull_request["updated_at"]),
                    url=pull_request["html_url"],
                )
                await ctx.send(embed=embed)

        @self._bot.command(name="config")
        # async def configs_options(ctx: Context):

        async def _button(ctx: Context):  # Altere de Interaction.CommandContext para commands.Context
            # view = ConfigMenu()
            button = Button(label="Clique")
            async def button_callback(interaction:discord.Interaction):
                await interaction.response.edit_message(content="Hello", view=None)
                await interaction.followup.send("aaaa")
            button.callback = button_callback
            view = View()
            view.add_item(button)

            await ctx.send("hi", view=view)

        @self._bot.command(name="set_config")
        async def set_new_config(ctx: Context):
            message = '1 - Adicionar novas configurações \n2 - Mostrar configurações atuais'
            embed = Embed(title="Menu de Configurações", description=message)

            view = ConfigMenu(timeout=50)

            message = await ctx.send(embed=embed,view=view)
            view.message = message
            await view.wait()
            await view.disable_all_items()
            if view.option_1 is True:
                channel = ctx.channel
                print("Adicionar novas configurações")
                msg = "Por favor envie o usuario do git que deseja monitorar."
                await ctx.send(msg)
                def check(m):
                    return m.author == ctx.author and m.channel == channel
                msg = await self._bot.wait_for("message",check=check)
                self._user = msg.content
                await msg.add_reaction("✅")

                msg = "Por favor envie o repositorio que deseja monitorar."
                await ctx.send(msg)
                def check(m):
                    return m.author == ctx.author and m.channel == channel
                msg = await self._bot.wait_for("message",check=check)
                self._repository = msg.content
                await msg.add_reaction("✅")
                await ctx.send("Configuração salva com sucesso.")

            elif view.option_2 is True:
                print("Mostrar configurações atuais")
                if self._user != "" and self._repository != "":
                    config = "Github User: {}\nGithub repository: {}".format(self._user, self._repository)
                    await ctx.send(config)
                else:
                    msg = "Nenhuma configuração encontrada."
                    await ctx.send(msg)
            else:
                print('cancel')



    def run(self):
        try:
            self._bot.run(self._token)
        except Exception as error:
            print(error)


class ConfigMenu(discord.ui.View):
    
    foo : bool = None
    option_1: bool = None
    option_2: bool = None
    
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
    
    async def on_timeout(self) -> None:
        await self.message.channel.send("Timeout")
        await self.disable_all_items()
    
    @discord.ui.button(label="1", style=discord.ButtonStyle.success)
    async def hello(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.option_1 = True
        await interaction.response.send_message("Option 1")
        self.stop()
    
    @discord.ui.button(label="2", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.option_2 = True
        await interaction.response.send_message("Option 2")
        self.stop()