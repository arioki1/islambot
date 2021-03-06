from aiohttp import ClientSession
from discord.ext import commands
from helpers import get_site_source
import discord
import re

icon = 'https://www.stickpng.com/assets/images/580b585b2edbce24c47b2abb.png'
INVALID_ARGUMENTS = "**Invalid arguments!**\nUsage: `-quranmorphology surah:verse:word\nExample: `-quranmorphology 1:1:2`" \
                    "(for the second word of the first verse of Surah al-Fatiha)"


class QuranMorphology(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession(loop = bot.loop)
        self.morphologyURL = 'http://corpus.quran.com/wordmorphology.jsp?location=({}:{}:{})'
        self.syntaxURL = 'http://corpus.quran.com/treebank.jsp?chapter={}&verse={}&token={}'

    @commands.command(name="morphology")
    async def morphology(self, ctx, ref: str):

        if not self.isInCorrectFormat(ref):
            await ctx.send(INVALID_ARGUMENTS)
            return

        try:
            surah, verse, word = ref.split(':')

        except:
            await ctx.send(INVALID_ARGUMENTS)
            return

        wordSource = await get_site_source(self.morphologyURL.format(surah, verse, word))
        wordImage = self.getWordImage(wordSource)

        paragraph = wordSource.find("p", "first")
        rawMorphology = str(wordSource.find("td", "morphologyCell").text)
        morphology = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \n\1', rawMorphology)
        grammar = wordSource.find("td", "grammarCell")

        syntax = False
        if self.isSyntaxAvailable(int(surah)):
            syntax = True
            syntaxSource = await get_site_source(self.syntaxURL.format(surah, verse, word))
            syntaxImage = self.getSyntaxImage(syntaxSource, word)

        em = discord.Embed(colour=0x006400)
        em.set_author(name=f"Qurʾān {surah}:{verse}, Word {word}", icon_url=icon)
        em.add_field(name='Morphology', value=f'From right to left: \n {morphology} ({grammar.text})', inline=False)
        em.add_field(name='Information', value=f'{paragraph.text}', inline=False)
        if syntax is True:
            em.set_image(url=syntaxImage)
            em.set_thumbnail(url=wordImage)
        else:
            em.set_image(url=wordImage)
        await ctx.send(embed=em)

    def getWordImage(self, source):
        imageText = source.find("a", "tokenLink")
        for image in imageText:
            image = (image['src'])
            imageURL = f"http://corpus.quran.com{image}"
            return imageURL

    def isSyntaxAvailable(self, surah):
        if 1 <= surah <= 8 or 59 <= surah <= 114:
            return True
        else:
            return False

    def getSyntaxImage(self, source, word):
        javascript = str(source.find("div", {"class": "graph"}))
        graphID = (javascript.split("url('/"))[1].split("')")[0]
        print(graphID)
        imageURL = f'http://corpus.quran.com/{graphID}&token={word}'
        return imageURL

    def isInCorrectFormat(self, ref):
        try:
            ref.split(':')
            return True
        except:
            return False


# Register as cog
def setup(bot):
    bot.add_cog(QuranMorphology(bot))
