from discord.ext import commands

# 参加者を管理する
class PlayersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ゲームに参加するコマンド
    # bot.players に Player オブジェクトを格納する
    # ステータスが参加者募集中かをチェックする
    # 既に参加しているメンバーかをチェックする
    @commands.command()
    def join(self, ctx):
        pass


def setup(bot):
    bot.add_cog(PlayersCog(bot))
