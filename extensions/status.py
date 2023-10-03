import random
import discord
from discord import app_commands
from discord.ext import commands
from constants.roles import simple


class GameStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ゲーム作成', description='新しい人狼ゲームを作成します')
    @app_commands.guild_only()
    async def _create_game_app_command(self, interaction: discord.Interaction):
        match self.bot.game.status:
            case 'playing':
                await interaction.response.send_message('既にゲームが進行中です', ephemeral=True)
                return
            case 'waiting':
                await interaction.response.send_message('既に参加者を募集中です', ephemeral=True)
                return
        self.bot.game.status = 'waiting'
        self.bot.game.channel = interaction.channel
        await interaction.response.send_message('参加者の募集を開始しました')

    @app_commands.command(name='ゲーム開始', description='人狼ゲームを開始します')
    @app_commands.guild_only()
    async def _start_game_app_command(self, interaction: discord.Interaction):
        match self.bot.game.status:
            case 'nothing':
                await interaction.response.send_message('まだ参加者を募集していません', ephemeral=True)
                return
            case 'playing':
                await interaction.response.send_message('既にゲーム中です', ephemeral=True)
                return

        n = len(self.bot.game.players)
        role = simple[n]
        role_list = random.sample(role, n)
        for i in range(n):
            player = self.bot.game.players[i]
            user = self.bot.get_user(player.id)
            role = role_list[i]
            await user.send(f'あなたの役職は {role} です')
            if role == '村':
                continue

            player.set_role(role)

        await interaction.response.send_message('役職が配布されました。配布された自分の役職を確認し、準備を完了させてください。')
        self.bot.game.status = 'playing'
        await interaction.response.send_message('ゲームが開始されました。それぞれの役職にあった行動をとってください。')

    @app_commands.command(name='ステータス確認', description='現在の人狼ゲームのステータスを確認します')
    @app_commands.guild_only()
    async def _show_game_status_app_command(self, interaction: discord.Interaction):
        match self.bot.game.status:
            case 'nothing':
                await interaction.response.send_message('参加者を募集していません', ephemeral=True)
                return
            case 'waiting':
                await interaction.response.send_message('参加者を募集中です', ephemeral=True)
                return
            case 'playing':
                await interaction.response.send_message('人狼ゲームが進行中です', ephemeral=True)
                return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GameStatus(bot))
