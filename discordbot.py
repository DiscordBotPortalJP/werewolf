# TODO
# オブジェクト
#   GM：bot
#   村
#   参加者
#       編成テンプレートの定義
#           4:村村占狼
#           5:村村村占狼
#   村人陣営の役職
#       村人
#       占い師
#   人狼陣営の役職
#       人狼
#   日数
#
# ゲーム進行
#   参加者の募集
#   プレイヤー参加
#   ゲーム開始
#   役職の割り振り
#   投票セット
#   占いセット
#   襲撃セット
#   処刑処理
#   襲撃処理
#   ゲーム終了判定
#   ゲーム結果の表示
#   日付変更処理
#   占い判定処理
#   襲撃結果(生存状況)表示
#       「Aさんが無残な姿で発見されました」
#   占い結果表示

from discord.ext import commands
import os
import traceback
from cogs.utils.errors import PermissionNotFound, NotGuildChannel, NotDMChannel

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_WEREWOLF_TOKEN']
bot.game_status = 'nothing'
bot.game_channel = None
bot.players = []  # 参加者の Player オブジェクトのリスト

# ゲームの経過日(投票、占い、襲撃先をリセット時に追加される)
bot.days = 0

# cogの読み込み
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


bot.run(token)
