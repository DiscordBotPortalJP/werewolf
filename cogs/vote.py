import discord
from discord.ext import commands
from cogs.utils import pagenator, errors
from cogs.utils.game import Game


def get_player(bot, player_id):
    for p in bot.game.players:
        if p.id == player_id:
            return p


class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not isinstance(ctx.channel, discord.DMChannel):
            await self.bot.on_command_error(ctx, errors.NotDMChannel())
            return False
        return True

    # 日付変更処理
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
            await guild.get_member(self.bot.game.fortuneteller.id).send(text)

        for p in self.bot.game.alive_players:
            p.clear_vote_target().clear_raid_target().clear_fortune_target()

        self.bot.game.days += 1

    async def do_vote(self, ctx):
        d = {self.bot.get_user(i.id).mention: i.id for i in self.bot.game.alive_players if i.id != ctx.author.id}
        data = list(d.keys())
        p = pagenator.Pagenator(self.bot, ctx.author, ctx.author, data,
                                '処刑するユーザーを選びます',
                                '処刑したいユーザーの番号のリアクションを押してください。\n左右矢印リアクションでページを変更できます。')
        target = await p.start()
        target_player = get_player(self.bot, d[target])
        get_player(self.bot, ctx.author.id).set_vote(target_player)
        await ctx.author.send('投票完了しました。')

    async def do_raid(self, ctx):
        d = {self.bot.get_user(i.id).mention: i.id for i in self.bot.game.alive_players if i.role != '狼' and i.id != ctx.author.id}
        data = list(d.keys())
        p = pagenator.Pagenator(self.bot, ctx.author, ctx.author, data,
                                '襲撃するユーザーを選びます',
                                '襲撃したいユーザーの番号のリアクションを押してください。\n左右矢印リアクションでページを変更できます。')
        target = await p.start()
        target_player = get_player(self.bot, d[target])
        get_player(self.bot, ctx.author.id).set_raid(target_player)
        await ctx.author.send('襲撃セット完了しました。')

    async def do_fortune(self, ctx):
        d = {self.bot.get_user(i.id).mention: i.id for i in self.bot.game.alive_players if i.id != ctx.author.id}
        data = list(d.keys())
        p = pagenator.Pagenator(self.bot, ctx.author, ctx.author, data,
                                '占うユーザーを選びます',
                                '占いたいユーザーの番号のリアクションを押してください。\n左右矢印リアクションでページを変更できます。')
        target = await p.start()
        target_player = get_player(self.bot, d[target])
        get_player(self.bot, ctx.author.id).set_fortune(target_player)
        await ctx.author.send('占いセット完了しました。')

    @commands.command()
    async def vote(self, ctx):
        await self.do_vote(ctx)
        await self.change_date(ctx)

    @commands.command()
    async def raid(self, ctx):
        if get_player(self.bot, ctx.author.id).role != '狼':
            await ctx.send('あなたは人狼ではないので、襲撃することはできません。')
            return
        await self.do_raid(ctx)
        await self.change_date(ctx)

    @commands.command()
    async def fortune(self, ctx):
        if get_player(self.bot, ctx.author.id).role != '占':
            await ctx.send('あなたは占い師ではないので、占うことはできません。')
            return
        await self.do_fortune(ctx)
        await self.change_date(ctx)

    @commands.command()
    async def werewolfs(self, ctx):
        if get_player(self.bot, ctx.author.id).role != '狼':
            await ctx.send('あなたは人狼ではありません')
            return
        guild = self.bot.game.channel.guild
        werewolfs = ' '.join(guild.get_member(w.id).display_name for w in self.bot.game.alive_werewolfs)
        await ctx.send(f'この村の人狼は {werewolfs} です。')


def setup(bot):
    return bot.add_cog(Vote(bot))
