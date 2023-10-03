import discord
from discord import app_commands
from discord.ext import commands
from application.player import Player


class PlayersCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='参加', description='人狼ゲームに参加する')
    @app_commands.guild_only()
    async def _join_app_command(self, interaction: discord.Interaction):
        match self.bot.game.status:
            case 'nothing':
                await interaction.response.send_message('現在ゲームはありません。', ephemeral=True)
                return
            case 'playing':
                await interaction.response.send_message('現在ゲーム進行中です。', ephemeral=True)
                return
        for player in self.bot.game.players:
            if interaction.user.id == player.id:
                await interaction.response.send_message('既にゲームに参加しています。', ephemeral=True)
                return
        player = Player(interaction.user.id)
        self.bot.game.players.append(player)
        await interaction.response.send_message(f'{interaction.user.mention} さんが参加しました。')

    @app_commands.command(name='退出', description='人狼ゲームから退出する')
    @app_commands.guild_only()
    async def _left_app_command(self, interaction: discord.Interaction):
        match self.bot.game.status:
            case 'nothing':
                await interaction.response.send_message('現在募集中のゲームはありません。', ephemeral=True)
                return
            case 'playing':
                await interaction.response.send_message('既にゲームが進行中のため退出できません。', ephemeral=True)
                return
        for player in self.bot.game.players:
            if interaction.user.id == player.id:
                self.bot.game.players.remove(player)
                await interaction.response.send_message(f'{interaction.user.mention} さんが退出しました。')
                return
        await interaction.response.send_message('ゲームに参加していません。', ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PlayersCog(bot))
