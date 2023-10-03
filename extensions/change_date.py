import discord
from discord import app_commands
from discord.ext import commands
from application.game import Game


class ChangeDateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='日付変更', description='投票&役職選択完了を確認して日付変更処理を行います')
    @app_commands.guild_only()
    async def change_date(self, interaction: discord.Interaction):
        game: Game = self.bot.game

        if not game.is_set_target():
            return

        guild = game.channel.guild

        game.execute()

        executed = guild.get_member(game.executed.id)
        text = f'投票の結果 {executed.display_name} さんが処刑されました'
        await game.channel.send(text)

        if game.is_village_win():
            text = 'ゲームが終了しました。人狼が全滅したため村人陣営の勝利です!'
            await game.channel.send(text)
            game = Game()
            return

        game.raid()

        if game.raided is not None:
            raided = guild.get_member(game.raided.id)
            text = f'{raided.display_name} さんが無残な姿で発見されました'
            await game.channel.send(text)

        if game.is_werewolf_win():
            text = 'ゲームが終了しました。村人陣営の数が人狼陣営の数以下になったため人狼陣営の勝利です!'
            await game.channel.send(text)
            game = Game()
            return

        game.fortune()

        if game.fortuned is not None:
            text = f'占い結果は {game.fortuned} です。'
            await guild.get_member(game.players.fortuneteller.id).send(text)

        for p in game.players.alives:
            p.clear_vote().clear_raid().clear_fortune()

        game.days += 1


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ChangeDateCog(bot))
