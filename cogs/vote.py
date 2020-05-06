from cogs.utils import player
from discord.ext import commands


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
        if not player.is_set_target():
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

    @commands.command()
    async def vote(self, ctx):
        await self.change_date(self, ctx)

    @commands.command()
    async def raid(self, ctx):
        await self.change_date(self, ctx)

    @commands.command()
    async def fortune(self, ctx):
        await self.change_date(self, ctx)


def setup(bot):
    return bot.add_cog(Vote(bot))
