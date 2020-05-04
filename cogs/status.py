import random

from discord.ext import commands

from .utils.roles import simple
import discord


# ゲーム開始前：nothing
# 参加者募集中:waiting
# ゲーム中:playing


class GameStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.guild is None:
            await ctx.send('サーバー内でのみ実行できるコマンドです')
            return False
        if not ctx.author.guild_permissions.administrator:
            await ctx.send('コマンドを実行する権限がありません')
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
    # 編成テンプレート(utils.roles)から役職を割り振る（Player.roleに役職名をセット)
    # ステータスを変更する
    # ゲーム開始メッセージを送信
    @commands.command()
    async def start(self, ctx):
        if self.bot.game_status == 'playing':
            await ctx.send('既にゲーム中です')
            return

        if self.bot.game_status == 'noting':
            await ctx.send('まだ参加者を募集していません')
            return

        count = len(self.bot.players)
        for role in random.sample(simple[count], count):
            for player in self.bot.players:
                user = self.bot.get_user(player.id)
                await user.send(f'あなたの役職は{role}です')  # ユーザーにdmで役職を通知

                if role == '村':  # 村人なら変更の必要が無いためスキップ
                    continue
                player.role = role

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
