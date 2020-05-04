from discord.ext import commands
from cogs.utils.errors import PermissionNotFound, NotGuildChannel

# ゲーム開始前：nothing
# 参加者募集中:waiting
# ゲーム中:playing


class GameStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.guild is None:
            await self.bot.on_command_error(ctx, NotGuildChannel())
            return False

        if not ctx.author.guild_permissions.administrator:
            await self.bot.on_command_error(ctx, PermissionNotFound())
            return False
        
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

    # ゲームを開始するコマンド
    # 編成テンプレート(urils.roles)から役職を割り振る（Player.roleに役職名をセット)
    # ステータスを変更する
    # ゲーム開始メッセージを送信
    @commands.command()
    async def start(self, ctx):
        pass

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
