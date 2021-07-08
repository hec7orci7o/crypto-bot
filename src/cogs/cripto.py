from discord import embeds
from libs.CoinMarketCap import CMC, Help
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, TooManyArguments, BadArgument, BadUnionArgument, ArgumentParsingError

class Cripto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def currency(self, ctx, symbol:str, converter:str='USD'):
        symbol, converter = symbol.upper(), converter.upper()
        try: 
            cmc = CMC()

            cData = cmc.quotes_latest(symbol=symbol, convert=converter)
            
            if 'data' in cData.keys():
                hp = Help()
                embed = hp.currencyEmbed(cData['data'][symbol], symbol, converter, cmc.Fiat)
                await ctx.send(embed= embed)
            else:
                # embed = currencyEmbed(cData)
                await ctx.send("status")
        except (MissingRequiredArgument, TooManyArguments, BadArgument, BadUnionArgument, ArgumentParsingError) as e:
            print(e)

    @commands.command()
    async def fiat(self, ctx, fiat:str):
        fiat = fiat.upper()
        try:
            cmc = CMC()
            fiat_dict =  cmc.fiat(fiat)

            hp = Help()
            embed = hp.fiatEmbed(fiat ,fiat_dict[fiat])

            await ctx.send(embed = embed)
        except (MissingRequiredArgument, TooManyArguments, BadArgument, BadUnionArgument, ArgumentParsingError) as e:
            print(e)

    @commands.command()
    async def hot(self, ctx, limit:int, converter:str='USD'):
        try:
            if limit <= 5:
                cmc = CMC()
                cData = cmc.listing_latest(limit=limit)

                if 'data' in cData.keys():
                    import pprint
                    pprint.pprint(cData)
                    hp = Help()
                    fiatSym = cmc.Fiat[converter]['SYMBOL']
                    embed = hp.hotEmbed(cData['data'][0], cData['data'][0]['symbol'], converter, fiatSym)
                    await ctx.send(embed= embed)
                else:
                    # embed = currencyEmbed(cData)
                    await ctx.send("status")
            else:
                await ctx.send("te viniste arriba con el limite")
        except (MissingRequiredArgument, TooManyArguments, BadArgument, BadUnionArgument, ArgumentParsingError) as e:
            print(e)
        


def setup(bot):
    bot.add_cog(Cripto(bot))
