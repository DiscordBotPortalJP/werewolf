from cogs.utils import player, pagenator
from discord.ext import commands


def get_player(bot, player_id):
    for player in bot.players:
        if player.id == player_id:
            return player


def is_village_win(players):
    for p in players:
        if p.role == '狼':
            return False
    return True


def is_werewolf_win(players):
    village_count = 0
    werewolf_count = 0
    for p in players:
        if p.role == '狼':
            werewolf_count += 1
        else:
            village_count += 1
    return village_count <= werewolf_count


class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 日付変更処理
    async def change_date(self, ctx):
        if not player.is_set_target(self.bot.players):
            return

        players = player.alive_players(self.bot.players)
        executed = player.execute(players)
        text = f'投票の結果 {executed.id} さんが処刑されました'
        await self.bot.game_channel.send(text)

        players = player.alive_players(self.bot.players)
        raided = player.raided(players)
        if raided is not None:
            text = f'{raided.id} さんが無残な姿で発見されました'
            await self.bot.game_channel.send(text)

        if is_village_win(players):
            text = 'ゲームが終了しました。人狼が全滅したため村人陣営の勝利です!'
            await self.bot.game_channel.send(text)
            self.bot.game_status = 'nothing'
            self.bot.game_channel = None
            self.bot.players = []
            self.bot.days = 0
            return

        if is_werewolf_win(players):
            text = 'ゲームが終了しました。村人陣営の数が人狼陣営の数以下になったため人狼陣営の勝利です!'
            await self.bot.game_channel.send(text)
            self.bot.game_status = 'nothing'
            self.bot.game_channel = None
            self.bot.players = []
            self.bot.days = 0
            return

        players = player.alive_players(self.bot.players)
        fortuned = player.fortune(players)
        if fortuned is not None:
            guild = self.bot.game_channel.guild
            text = f'占い結果は {fortuned} です。'
            fortuneteller = player.get_fortuneteller(players)
            await guild.get_member(fortuneteller.id).send(text)

        for p in players:
            p.clear_vote_target().clear_raid_target().clear_fortune_target()

        self.bot.days += 1

    async def do_vote(self, ctx):
        d = {i.mention: i.id for i in self.bot.players if i.id != ctx.author.id}
        data = list(d.keys())
        p = pagenator.Pagenator(self.bot, ctx.author, ctx.author, data, 
        '処刑するユーザーを選びます', 
        '処刑したいユーザーの番号のリアクションを押してください。\n左右矢印リアクションでページを変更できます。')
        target = await p.start()
        target_player = get_player(d[target])
        get_player(ctx.author.id).set_vote(target_player)
        await ctx.author.send('投票完了しました。')
    
    async def do_raid(self, ctx):
        d = {i.mention: i.id for i in self.bot.players if i.role  != '狼' and i.id != ctx.author.id}
        data = list(d.keys())
        p = pagenator.Pagenator(self.bot, ctx.author, ctx.author, data, 
        '殺すユーザーを選びます', 
        '殺したいユーザーの番号のリアクションを押してください。\n左右矢印リアクションでページを変更できます。')
        target = await p.start()
        target_player = get_player(d[target])
        get_player(ctx.author.id).set_raid(target_player)
        await ctx.author.send('投票完了しました。')
    
    async def do_fortune(self, ctx):
        d = {i.mention: i.id for i in self.bot.players if i.id != ctx.author.id}
        data = list(d.keys())
        p = pagenator.Pagenator(self.bot, ctx.author, ctx.author, data, 
        '占うユーザーを選びます', 
        '占いたいユーザーの番号のリアクションを押してください。\n左右矢印リアクションでページを変更できます。')
        target = await p.start()
        target_player = get_player(d[target])
        get_player(ctx.author.id).set_raid(target_player)
        await ctx.author.send('投票完了しました。')

    @commands.command()
    async def vote(self, ctx):
        await self.do_vote(ctx)
        await self.change_date(ctx)

    @commands.command()
    async def raid(self, ctx):
        if get_player(self.bot, ctx.author.id).role != '狼':
            await ctx.send('あなたは人狼ではないので、処刑することはできません。')
            return
        await self.do_raid(ctx)
        await self.change_date(ctx)

    @commands.command()
    async def fortune(self, ctx):
        if get_player(self.bot, ctx.author.id).role != '占':
            await ctx.author.send('あなたは占い師ではないので、占うことはできません。')
            return
        await self.do_fortune(ctx)
        await self.change_date(ctx)


def setup(bot):
    return bot.add_cog(Vote(bot))
