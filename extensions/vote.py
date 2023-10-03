import discord
from discord import app_commands
from discord.ext import commands
from application.game import Game
from application.player import Players
from application.pagenator import Pagenator


class VoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def change_date(self, interaction: discord.Interaction):
        """日付変更処理"""
        if not self.bot.game.is_set_target():
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

    async def select(self, interaction: discord.Interaction, players: Players, set_method, action: str):
        d = {self.bot.get_user(p.id).mention: p.id for p in players if p.id != interaction.user.id}
        target = await Pagenator(
            self.bot,
            interaction.user,
            interaction.user,
            list(d.keys()),
            f'{action}対象に指定するユーザーを選びます',
            f'{action}対象に指定するユーザーの番号のリアクションを押してください。\n左右矢印リアクションでページを変更できます。'
        ).start()
        set_method(self.bot.game.players.get(d[target]))
        await interaction.response.send_message(f'{action}指定完了しました。', ephemeral=True)

    async def select_vote(self, interaction: discord.Interaction):
        set_method = self.bot.game.players.get(interaction.author.id).set_vote
        await self.select(interaction, self.bot.game.players.alives, set_method, '処刑')

    async def select_raid(self, interaction: discord.Interaction):
        set_method = self.bot.game.players.get(interaction.author.id).set_raid
        await self.select(interaction, self.bot.game.players.alives.werewolfs, set_method, '襲撃')

    async def select_fortune(self, interaction: discord.Interaction):
        set_method = self.bot.game.players.get(interaction.author.id).set_fortune
        await self.select(interaction, self.bot.game.players.alives, set_method, '占い')

    @app_commands.command(name='投票', description='処刑したいプレイヤーに投票します')
    @app_commands.guild_only()
    async def _vote_app_command(self, interaction: discord.Interaction):
        await self.select_vote(interaction)
        await self.change_date(interaction)

    @app_commands.command(name='襲撃', description='襲撃したいプレイヤーに投票します')
    @app_commands.guild_only()
    async def _raid_app_command(self, interaction: discord.Interaction):
        if self.bot.game.players.get(interaction.user.id).role != '狼':
            await interaction.response.send_message('あなたは人狼ではないので、襲撃することはできません。', ephemeral=True)
            return
        await self.select_raid(interaction)
        await self.change_date(interaction)

    @app_commands.command(name='占い', description='プレイヤーを一人占います')
    @app_commands.guild_only()
    async def _fortune_app_command(self, interaction: discord.Interaction):
        if self.bot.game.players.get(interaction.user.id).role != '占':
            await interaction.response.send_message('あなたは占い師ではないので、占うことはできません。', ephemeral=True)
            return
        await self.select_fortune(interaction)
        await self.change_date(interaction)

    @app_commands.command(name='仲間の人狼を表示', description='仲間の人狼を表示します')
    @app_commands.guild_only()
    async def _show_werewolfs_app_command(self, interaction: discord.Interaction):
        if self.bot.game.players.get(interaction.user.id).role != '狼':
            await interaction.response.send_message('あなたは人狼ではありません', ephemeral=True)
            return
        guild = self.bot.game.channel.guild
        werewolfs = ' '.join(guild.get_member(w.id).display_name for w in self.bot.game.players.alives.werewolfs)
        await interaction.response.send_message(f'この村の人狼は {werewolfs} です。', ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(VoteCog(bot))
