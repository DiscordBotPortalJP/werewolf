from discord.ext import commands


class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voted_player = None  # 処刑される人
        self.fortuned_player = None  # 占いをされる人
        self.killed_player = None  # 人狼に殺される人

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
