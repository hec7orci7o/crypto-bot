import os
import discord
from discord.ext import commands
from decouple import config

class BotHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
    
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title= "Help Menu",
            colour= int("3861FB",16)
        )
        for cog in mapping:
            if cog != None:
                lista = [command.name for command in mapping[cog]]
                value = ''
                for cmd in lista:
                    value += (f" + {cmd}\n")
                embed.add_field(name= str(cog.qualified_name).capitalize(), value= value, inline='false')
        await self.get_destination().send(embed= embed)

    async def send_cog_help(self, cog):
        await self.get_destination().send(f'{cog.cualified_name}: {[command.name for command in cog.get_command()]}')
    
    async def send_command_help(self, command):
        embed = discord.Embed(
            title= "Command: " + str(command.name).capitalize(),
            description= command.help,
            colour= int("3861FB",16)
        )
        await self.get_destination().send(embed= embed)

    async def send_group_help(self, group):
        await self.get_destination().send(f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')

class FinanceBot(commands.Bot):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

client = FinanceBot(command_prefix='$', help_command=BotHelpCommand())

# Cogs
for filename in os.listdir('src/cogs'):
    if filename.endswith('.py'):
        try:
            print(f'cogs.{filename[:-3]} loaded successfully.')
            client.load_extension(f'cogs.{filename[:-3]}')
        except:
            print(f'error al cargar el cog {filename[:-3]}')

client.run(config('TOKEN'))
