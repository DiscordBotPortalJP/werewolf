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

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_WEREWOLF_TOKEN']
bot.game_status = 'nothing'
bot.players = []  # 参加者の Player オブジェクトのリスト

# ゲームの経過日(投票、占い、襲撃先をリセット時に追加される)
bot.days = 0

# 処刑される人
bot.voted_player = None

# 占いをされる人
bot.fortuned_player = None

# 人狼に殺される人
bot.killed_player = None

# 参加者募集
bot.load_extension('cogs.status')

# プレイヤーの参加


# ゲーム開始


bot.run(token)
