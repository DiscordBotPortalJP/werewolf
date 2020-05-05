from discord.ext import commands


class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fortune(self, player):
        """占い"""
        pass

    async def wolf(self, players):
        """人狼"""
        pass

    async def player_vote(self, players):
        """処刑"""
        pass

    @commands.command()
    async def vote(self, ctx):
        pass


def setup(bot):
    return bot.add_cog(Vote(bot))
