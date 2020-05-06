from discord.ext import commands


class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vote(self, ctx):
        pass

    @commands.command()
    async def raid(self, ctx):
        pass

    @commands.command()
    async def fortune(self, ctx):
        pass


def setup(bot):
    return bot.add_cog(Vote(bot))
