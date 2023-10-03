import discord
from discord import app_commands
from discord.ext import commands
from application.game import Game


class VoteDropdown(discord.ui.Select):
    def __init__(self, members: list[discord.Member]):
        super().__init__(
            placeholder='処刑したいプレイヤー',
            min_values=1,
            max_values=1,
            options=[discord.SelectOption(label=member.display_name, value=str(member.id)) for member in members]
        )

    async def callback(self, interaction: discord.Interaction):
        game: Game = interaction.client.game
        game.players.get(interaction.user.id).set_vote(game.players.get(int(self.values[0])))
        await interaction.response.send_message('処刑希望投票が完了しました。', ephemeral=True)


class VoteView(discord.ui.View):
    def __init__(self, members: list[discord.Member]):
        super().__init__()
        self.add_item(VoteDropdown(members))


class VoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='投票', description='処刑したいプレイヤーに投票します')
    @app_commands.guild_only()
    async def _vote_app_command(self, interaction: discord.Interaction):
        members = [interaction.guild.get_member(player.id) for player in self.bot.game.players.alives]
        await interaction.response.send_message('処刑したいプレイヤーを選択してください', view=VoteView(members), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(VoteCog(bot))
