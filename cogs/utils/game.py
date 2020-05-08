from typing import Optional
from cogs.utils.player import Player, Players


class Game():
    """人狼ゲーム

    Attributes:
        status (str): 進行状況
        channel (discord.TextChannel): ゲームを進行するチャンネル
        players (Players): 参加者リスト
        days (int): ゲームの経過日
        executed (Optional[Player]): 処刑されたプレイヤー
        raided (Optional[Player]): 襲撃されたプレイヤー
        fortuned (Optional[str]): 占い結果
    """

    def __init__(self):
        self.status = 'nothing'
        self.channel = None
        self.players = Players()
        self.days = 0
        self.executed = None
        self.raided = None
        self.fortuned = None

    def is_village_win(self) -> bool:
        """村人陣営が勝利しているか"""
        for p in self.players.alives:
            if p.role == "狼":
                return False
        return True

    def is_werewolf_win(self) -> bool:
        """人狼陣営が勝利しているか"""
        village_count = 0
        werewolf_count = 0
        for p in self.players.alives:
            if p.role == "狼":
                werewolf_count += 1
            else:
                village_count += 1
        return village_count <= werewolf_count

    def is_set_target(self) -> bool:
        """全員が指定完了しているか"""
        for p in self.players.alives:
            if p.vote_target is None:
                return False
            if p.role == '狼' and p.raid_target is None:
                return False
            if p.role == '占' and p.fortune_target is None:
                return False
        return True

    def execute(self) -> Player:
        """処刑処理"""
        self.executed = self.players.votes.most.die()
        return self

    def raid(self) -> Optional[Player]:
        """襲撃処理"""
        target = self.players.raids.most
        if not target.is_dead:
            self.raided = target.die()
        return self

    def fortune(self) -> Optional[str]:
        """占い処理"""
        if self.players.alives.fortuneteller is not None:
            self.fortuned = self.players.alives.fortuneteller.fortune_target.side
        return self
