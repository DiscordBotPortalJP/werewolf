import random
import discord
from discord import app_commands
from discord.ext import commands
from application.player import Player
from application.game import Game
from constants import roles


class PlayCog(commands.Cog):
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
        role = roles.simple[n]
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

    @app_commands.command(name='仲間の人狼を表示', description='仲間の人狼を表示します')
    @app_commands.guild_only()
    async def _show_werewolfs_app_command(self, interaction: discord.Interaction):
        game: Game = self.bot.game
        if game.players.get(interaction.user.id).role != '狼':
            await interaction.response.send_message('あなたは人狼ではありません', ephemeral=True)
            return
        werewolfs = ' '.join(interaction.guild.get_member(player.id).mention for player in self.bot.game.players.werewolfs)
        await interaction.response.send_message(f'この村の人狼は {werewolfs} です。', ephemeral=True)

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
    await bot.add_cog(PlayCog(bot))
