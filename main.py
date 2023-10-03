import discord
from discord.ext import commands
from application.game import Game
from constants.discord import TOKEN

extensions = [
    'handle_error',
    'players',
    'status',
    'vote',
]


class WerewolfBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('$'),
            intents=discord.Intents.all(),
        )

    async def setup_hook(self):
        for extension in extensions:
            await self.load_extension(f'extensions.{extension}')
        # await self.tree.sync()


def main():
    bot = WerewolfBot()
    bot.game = Game()
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
