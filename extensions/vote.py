import discord
from discord.ext import commands
from utils import errors
from application.game import Game
from application.player import Players
from application.pagenator import Pagenator


class VoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not isinstance(ctx.channel, discord.DMChannel):
            await self.bot.on_command_error(ctx, errors.NotDMChannel())
            return False
        return True

    async def change_date(self, ctx):
        """日付変更処理"""
        if not self.bot.game.is_set_target():
            await self.bot.game.channel.send('指定が行われましたが、未指定の方がいます。')
            return

        guild = self.bot.game.channel.guild

        self.bot.game.execute()

        executed = guild.get_member(self.bot.game.executed.id)
        text = f'投票の結果 {executed.display_name} さんが処刑されました'
        await self.bot.game.channel.send(text)

        if self.bot.game.is_village_win():
            text = 'ゲームが終了しました。人狼が全滅したため村人陣営の勝利です!'
            await self.bot.game.channel.send(text)
            self.bot.game = Game()
            return

        self.bot.game.raid()

        if self.bot.game.raided is not None:
            raided = guild.get_member(self.bot.game.raided.id)
            text = f'{raided.display_name} さんが無残な姿で発見されました'
            await self.bot.game.channel.send(text)

        if self.bot.game.is_werewolf_win():
            text = 'ゲームが終了しました。村人陣営の数が人狼陣営の数以下になったため人狼陣営の勝利です!'
            await self.bot.game.channel.send(text)
            self.bot.game = Game()
            return

        self.bot.game.fortune()

        if self.bot.game.fortuned is not None:
            text = f'占い結果は {self.bot.game.fortuned} です。'
            await guild.get_member(self.bot.game.players.fortuneteller.id).send(text)

        for p in self.bot.game.players.alives:
            p.clear_vote().clear_raid().clear_fortune()

        self.bot.game.days += 1

    async def select(self, ctx, players: Players, set_method, action: str):
        d = {self.bot.get_user(p.id).mention: p.id for p in players if p.id != ctx.author.id}
        target = await Pagenator(
            self.bot,
            ctx.author,
            ctx.author,
            list(d.keys()),
            f'{action}対象に指定するユーザーを選びます',
            f'{action}対象に指定するユーザーの番号のリアクションを押してください。\n左右矢印リアクションでページを変更できます。'
        ).start()
        set_method(self.bot.game.players.get(d[target]))
        await ctx.author.send(f'{action}指定完了しました。')

    async def select_vote(self, ctx):
        set_method = self.bot.game.players.get(ctx.author.id).set_vote
        await self.select(ctx, self.bot.game.players.alives, set_method, '処刑')

    async def select_raid(self, ctx):
        set_method = self.bot.game.players.get(ctx.author.id).set_raid
        await self.select(ctx, self.bot.game.players.alives.werewolfs, set_method, '襲撃')

    async def select_fortune(self, ctx):
        set_method = self.bot.game.players.get(ctx.author.id).set_fortune
        await self.select(ctx, self.bot.game.players.alives, set_method, '占い')

    @commands.command()
    async def vote(self, ctx):
        await self.select_vote(ctx)
        await self.change_date(ctx)

    @commands.command()
    async def raid(self, ctx):
        if self.bot.game.players.get(ctx.author.id).role != '狼':
            await ctx.send('あなたは人狼ではないので、襲撃することはできません。')
            return
        await self.select_raid(ctx)
        await self.change_date(ctx)

    @commands.command()
    async def fortune(self, ctx):
        if self.bot.game.players.get(ctx.author.id).role != '占':
            await ctx.send('あなたは占い師ではないので、占うことはできません。')
            return
        await self.select_fortune(ctx)
        await self.change_date(ctx)

    @commands.command()
    async def werewolfs(self, ctx):
        if self.bot.game.players.get(ctx.author.id).role != '狼':
            await ctx.send('あなたは人狼ではありません')
            return
        guild = self.bot.game.channel.guild
        werewolfs = ' '.join(guild.get_member(w.id).display_name for w in self.bot.game.players.alives.werewolfs)
        await ctx.send(f'この村の人狼は {werewolfs} です。')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(VoteCog(bot))
