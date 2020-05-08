import os
import traceback
from discord.ext import commands
from cogs.utils.errors import PermissionNotFound, NotGuildChannel, NotDMChannel

bot = commands.Bot(command_prefix='/')
bot.game_status = 'nothing'
bot.game_channel = None
bot.players = []  # 参加者の Player オブジェクトのリスト
bot.days = 0  # ゲームの経過日

extensions = [
    'cogs.status',
    'cogs.players',
    'cogs.vote',
]
for extension in extensions:
    bot.load_extension(extension)


@bot.event
async def on_command_error(ctx, error):
    """エラーハンドリング"""

    if isinstance(error, commands.CheckFailure):
        return

    if isinstance(error, PermissionNotFound):
        await ctx.send('コマンドを実行する権限がありません')
        return

    if isinstance(error, NotGuildChannel):
        await ctx.send('サーバー内でのみ実行できるコマンドです')
        return

    if isinstance(error, NotDMChannel):
        await ctx.send('DM内でのみ実行できるコマンドです')
        return

    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    error_msg = "```py\n" + error_msg + "\n```"
    await ctx.send(error_msg)


bot.run(os.environ['DISCORD_BOT_WEREWOLF_TOKEN'])
