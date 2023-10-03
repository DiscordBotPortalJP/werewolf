from discord.ext import commands
from application.player import Player


class PlayersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """ゲームに参加するコマンド"""
        if self.bot.game.status == "nothing":
            return await ctx.send("現在ゲームはありません。")
        elif self.bot.game.status == "playing":
            return await ctx.send("現在ゲーム進行中です。")
        member = ctx.author
        for p in self.bot.game.players:
            if member.id == p.id:
                return await ctx.send("すでにゲームに参加しています。")
        player = Player(member.id)
        self.bot.game.players.append(player)
        await ctx.send(f"{member.mention}さんが参加しました。")

    @commands.command()
    async def leave(self, ctx):
        """ゲームから退出するコマンド"""
        if self.bot.game.status == "nothing":
            return await ctx.send("現在ゲームはありません。")
        elif self.bot.game.status == "playing":
            return await ctx.send("既にゲームが始まっているため退出できません。")
        member = ctx.author
        for p in self.bot.game.players:
            if member.id == p.id:
                self.bot.game.players.remove(p)
                return await ctx.send("ゲームから退出しました。")
        return await ctx.send("ゲームに参加していません。")


def setup(bot):
    bot.add_cog(PlayersCog(bot))
