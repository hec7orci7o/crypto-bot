from libs.CoinMarketCap import CMC
from libs.ETHGasStation import ETH
from libs.Pretty import Format
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, TooManyArguments, BadArgument, BadUnionArgument, ArgumentParsingError

class Cripto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmc = CMC()
        self.eth = ETH()
        self.f   = Format()

    @commands.command(help="Usage: `$currency <symbol>* <fiat>`\nExample: `$currency BTC USD`")
    async def currency(self, ctx, symbol:str, converter:str='USD'):
        symbol, converter = symbol.upper(), converter.upper()
        try:
            cData = self.cmc.quotes_latest(symbol=symbol, convert=converter)
            
            if 'data' in cData.keys():
                embed = self.f.currencyEmbed(cData['data'][symbol], symbol, converter, self.cmc.Fiat)
                await ctx.send(embed= embed)
            else:
                # embed = currencyEmbed(cData)
                await ctx.send("status")
        except (MissingRequiredArgument, TooManyArguments, BadArgument, BadUnionArgument, ArgumentParsingError) as e:
            print(e)

    @commands.command(help="Usage: `$hot <limit:[1-3]>* <fiat>`\nExample: `$hot 1 USD`")
    async def hot(self, ctx, limit:int, converter:str='USD'):
        converter = converter.upper()
        converter = 'USD'

        try:
            if limit <= 3:
                cData = self.cmc.listing_latest(limit=limit)

                if 'data' in cData.keys():
                    fiatSym = self.cmc.Fiat[converter]['SYMBOL']
                    embed_list = self.f.hotEmbed(cData['data'], converter, fiatSym)
                    for embed in embed_list:
                        await ctx.send(embed= embed)
                else:
                    # embed = currencyEmbed(cData)
                    await ctx.send("status")
            else:
                await ctx.send("te viniste arriba con el limite")
        except (MissingRequiredArgument, TooManyArguments, BadArgument, BadUnionArgument, ArgumentParsingError) as e:
            print(e)

    @commands.command(help="Usage: `$fiat <fiat>*`\nExample: `$fiat EUR`")
    async def fiat(self, ctx, fiat:str):
        fiat = fiat.upper()
        try:
            fiat_dict =  self.cmc.fiat(fiat)
            embed = self.f.fiatEmbed(fiat ,fiat_dict[fiat])
            await ctx.send(embed = embed)
        except (MissingRequiredArgument, TooManyArguments, BadArgument, BadUnionArgument, ArgumentParsingError) as e:
            print(e)

    @commands.command(help="Usage: `$gas`\nExample: `$gas`")
    async def gas(self, ctx):
        try:
            sData = self.eth.gasPrice()
            embed = self.f.ethGasPriceEmbed(sData)
            await ctx.send(embed= embed)
        except (MissingRequiredArgument, TooManyArguments, BadArgument, BadUnionArgument, ArgumentParsingError) as e:
            print(e)

def setup(bot):
    bot.add_cog(Cripto(bot))
