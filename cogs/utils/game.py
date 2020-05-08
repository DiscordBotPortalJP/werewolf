import random
import collections
from typing import List, Optional
from cogs.utils.player import Player


class Game():
    """人狼ゲーム

    Attributes:
        status (str): 進行状況
        channel (discord.TextChannel): ゲームを進行するチャンネル
        players (List[Player]): 参加者リスト
        days (int): ゲームの経過日
        executed (Optional[Player]): 処刑されたプレイヤー
        raided (Optional[Player]): 襲撃されたプレイヤー
        fortuned (Optional[str]): 占い結果
    """

    def __init__(self):
        self.status = 'nothing'
        self.channel = None
        self.players = []
        self.days = 0
        self.executed = None
        self.raided = None
        self.fortuned = None

    @property
    def alive_players(self) -> List[Player]:
        """生存プレイヤーリスト"""
        return [p for p in self.players if not p.is_dead]

    @property
    def alive_werewolfs(self) -> List[Player]:
        """生存人狼プレイヤーリスト"""
        return [p for p in self.players if p.role == '狼']

    @property
    def fortuneteller(self) -> Optional[Player]:
        """占い師プレイヤー"""
        for p in self.players:
            if p.role == '占':
                return p
        return None

    @property
    def votes(self):
        """投票指定データ"""
        return [player.vote_target for player in self.alive_players]

    @property
    def raids(self):
        """襲撃指定データ"""
        return [werewolf.raid_target for werewolf in self.alive_werewolfs]

    def is_village_win(self) -> bool:
        """村人陣営が勝利しているか"""
        for p in self.players:
            if p.role == "狼":
                return False
        return True

    def is_werewolf_win(self) -> bool:
        """人狼陣営が勝利しているか"""
        village_count = 0
        werewolf_count = 0
        for p in self.players:
            if p.role == "狼":
                werewolf_count += 1
            else:
                village_count += 1
        return village_count <= werewolf_count

    def is_set_target(self) -> bool:
        """全員が指定完了しているか"""
        for p in self.alive_players:
            if p.vote_target is None:
                return False
            if p.role == '狼' and p.raid_target is None:
                return False
            if p.role == '占' and p.fortune_target is None:
                return False
        return True

    def elect(self, players) -> Player:
        """指定リストから実行対象を選出"""
        aggregates = collections.Counter(players)
        maximum = max(aggregates.values())
        mosts = [a[0] for a in aggregates.most_common() if a[1] == maximum]
        return random.choice(mosts)

    def execute(self) -> Player:
        """処刑処理"""
        self.executed = self.elect(self.votes).set_dead()
        return self

    def raid(self) -> Optional[Player]:
        """襲撃処理"""
        target = self.elect(self.raids)
        if not target.is_dead:
            self.raided = target.set_dead()
        return self

    def fortune(self) -> Optional[str]:
        """占い処理"""
        if self.fortuneteller is not None:
            self.fortuned = self.fortuneteller.fortune_target.get_side()
        return self
