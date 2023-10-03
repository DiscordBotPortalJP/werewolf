import traceback
from discord.ext import commands
from utils.errors import PermissionNotFound, NotGuildChannel, NotDMChannel


class HandleErrorCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(ctx, error: commands.CommandError):
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


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HandleErrorCog(bot))
