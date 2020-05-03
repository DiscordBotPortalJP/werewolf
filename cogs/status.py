from discord.ext import commands
from cogs.utils.errors import NoGuildError, PermissionNotFound

# ゲーム開始前：nothing
# 参加者募集中:waiting
# ゲーム中:playing


class GameStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.guild is None:
            raise NoGuildError

        if not ctx.author.guild_permissions.administrator:
            raise PermissionNotFound

        return True

    @commands.command()
    async def create(self, ctx):
        if self.bot.game_status == 'playing':
            await ctx.send('ゲーム中です')
            return
        if self.bot.game_status == 'waiting':
            await ctx.send('既に参加者募集中です')
            return
        self.bot.game_status = 'waiting'
        await ctx.send('参加者の募集を開始しました')

    @commands.command()
    async def set_nothing(self, ctx):
        self.bot.game_status = 'nothing'
        await ctx.send(f'game_status を {self.bot.game_status} に変更しました')

    @commands.command()
    async def set_playing(self, ctx):
        self.bot.game_status = 'playing'
        await ctx.send(f'game_status を {self.bot.game_status} に変更しました')

    @commands.command()
    async def set_waiting(self, ctx):
        self.bot.game_status = 'waiting'
        await ctx.send(f'game_status を {self.bot.game_status} に変更しました')

    @commands.command()
    async def game_status(self, ctx):
        await ctx.send(f'現在の game_status は {self.bot.game_status} です')


def setup(bot):
    bot.add_cog(GameStatus(bot))
