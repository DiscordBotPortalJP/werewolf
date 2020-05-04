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
    async def join(self, ctx):
        if self.bot.game_status == "nothing":
            return await ctx.send("現在ゲームはありません。")
        elif self.bot.game_status == "playing":
            return await ctx.send("現在ゲーム進行中です。")
        
        user = ctx.author
        if user in self.bot.players:
            return await ctx.send("すでにゲームに参加しています。")
        
        self.bot.players.append(user)
        await ctx.send(f"{user.mention}さんが参加しました。")


def setup(bot):
    bot.add_cog(PlayersCog(bot))
