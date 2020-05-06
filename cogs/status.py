import random
from discord.ext import commands

from cogs.utils.roles import simple
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
        self.bot.game_channel = ctx.channel
        await ctx.send('参加者の募集を開始しました')

    # ゲームを開始するコマンド
    # 編成テンプレート(utils.roles)から役職を割り振る（Player.roleに役職名をセット)
    # ステータスを変更する
    # ゲーム開始メッセージを送信
    @commands.command()
    async def start(self, ctx):
        if self.bot.game_status == 'playing':
            await ctx.send('既にゲーム中です')
            return

        if self.bot.game_status == 'nothing':
            await ctx.send('まだ参加者を募集していません')
            return

        # 参加者の人数(int)を取得 => n
        n = len(self.bot.players)
        # 役職の文字列(配列)を取得
        role = simple[n]
        # 役職の文字列(配列)をシャッフル
        role_list = random.sample(role, n)
        # 0..n までの数値を回す
        for i in range(n):
            # シャッフルした役職の配列と参加者の配列を同じindexで設定する
            player = self.bot.players[i]
            user = self.bot.get_user(player.id)
            role = role_list[i]
            await user.send(f'あなたの役職は{role}です')
            if role == '村':
                continue

            player.set_role(role)

        await ctx.send('役職が配布されました。配布された自分の役職を確認し、準備を完了させてください。')
        self.bot.game_status = 'playing'
        await ctx.send('ゲームが開始されました。しばらくすると夜に切り替わるのでそれぞれの役職にあった行動をとってください。')

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
