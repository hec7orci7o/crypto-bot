import os
import datetime
import discord
import random
from discord.ext import commands, tasks
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
        embed = discord.Embed(
            title= "Cog Menu",
            colour= int("3861FB",16)
        )
        lista = [command.name for command in cog.get_commands()]
        value = ''
        for cmd in lista:
            value += (f" + {cmd}\n")
        embed.add_field(name= str(cog.qualified_name).capitalize(), value= value, inline='false')
        await self.get_destination().send(embed= embed)
    
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
        frases = [
            "What everyone in the stock market\nknows, I am not interested in.",
            "When my shoeshine boy invests in the\n stock market, I sell everything.",
            "An investor's destiny is determined by his stomach, not his brain.",
            "Optimism is the enemy of the\nrational buyer.",
            "The two great forces driving the markets aregreed and fear.",
            "An investor needs to do very few\nthings well if he avoids big risks. It is not necessary to do extraordinary\nthings to obtain extraordinary results."
        ]

        embed = discord.Embed(
            description= frases[random.randint(0, 5)],
            color= int("8CBF84", 16)
        )
        embed.set_thumbnail(
            url= "https://ih1.redbubble.net/image.565958121.9349/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.u1.jpg"
        )
        embed.set_author(
            name= f"{str(self.user)[:-5]}",
            url= "https://hec7or.me/",
            icon_url= "https://images.unsplash.com/photo-1590486145851-aae8758c4211?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1868&q=80"
        )
        embed.add_field(
            name= "Stats:",
            value= "```c++\n{}```".format("Running on {} servers.\nStarted at {}".format(len(client.guilds), datetime.datetime.now().strftime("%X"))),
            inline= False
        )
        embed.set_footer(
            text= "Made with 💘 by Hec7orci7o.",
            icon_url= "https://avatars.githubusercontent.com/u/56583980?s=60&v=4"
        )
        
        channel = client.get_channel(int(config('CHANNEL')))
        await channel.send(embed=embed)
        print('Connected as {0}!'.format(self.user))
        print("Event loop 'change presence()' started.")
        self.myLoop.start()

    @tasks.loop(seconds = 3600) # repeat after every 1 hour
    async def myLoop(self):
        game = discord.Activity(type=discord.ActivityType.watching, name="a chance to see those dollars go up | $help")
        await client.change_presence(status=discord.Status.idle, activity=game)


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
