from discord.ext import commands
from urllib.request import urlopen
from bs4 import BeautifulSoup
import discord

icon = 'https://s.cafebazaar.ir/1/icons/ir.quranofflainpishgaman.com_512x512.png'


class Mushaf(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mushaf")
    async def mushaf(self, ctx, ref: str):

        try:
            surah, ayah = ref.split(':')

        except:
            await ctx.send("**Invalid verse.** Please type the command in this format: `-mushaf surah:ayah`.\n\ne.g. `-mushaf 112:1`")
            return

        site = urlopen(f'https://www.altafsir.com/Quran.asp?SoraNo={surah}&Ayah={ayah}&NewPage=0&Tajweed=1&LanguageID=2')

        content = site.read()

        soup = BeautifulSoup(content, 'html.parser')

        image = soup.find('img',attrs={'name':'QImage'})['src']

        url = f'https://www.altafsir.com/{image}'

        pageNumber = url.rsplit('/', 1)[-1]
        pageNumber = pageNumber.replace('.gif', '')
        pageNumber = pageNumber.replace('.png', '')
        pageNumber = pageNumber.lstrip('p')
        pageNumber = pageNumber.lstrip('0')

        em = discord.Embed(title=f'{surah}:{ayah}', colour=0x47464f)
        em.set_author(name=f'Madinah Mushaf', icon_url=icon)
        em.set_image(url=url)
        em.set_footer(text=f'Page {pageNumber}')

        await ctx.send(embed=em)


# Register as cog
def setup(bot):
    bot.add_cog(Mushaf(bot))
