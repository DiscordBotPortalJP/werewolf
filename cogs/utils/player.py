from __future__ import annotations
from typing import Optional
import random
import collections


class Player():
    """参加者

    Attributes:
        id (int): DiscordのユーザID
        role (str): 役職名
        is_dead (bool): 死亡しているか
        vote_target (Optional[Player]): 投票指定した参加者
        raid_target (Optional[Player]): 襲撃指定した参加者
        fortune_target (Optional[Player]): 占い指定した参加者
    """

    def __init__(self, discord_id: int):
        self.id = discord_id
        self.role = '村'
        self.is_dead = False
        self.vote_target = None
        self.raid_target = None
        self.fortune_target = None

    @property
    def side(self) -> str:
        """プレイヤーの陣営を取得"""
        if self.role in '村占':
            return '村人陣営'
        if self.role in '狼':
            return '人狼陣営'

    def die(self):
        """死亡する"""
        self.is_dead = True
        return self

    def set_role(self, role: str):
        self.role = role
        return self

    def set_vote(self, player):
        self.vote_target = player

    def set_raid(self, player):
        self.raid_target = player

    def set_fortune(self, player):
        self.fortune_target = player

    def clear_vote(self):
        self.vote_target = None
        return self

    def clear_raid(self):
        self.raid_target = None
        return self

    def clear_fortune(self):
        self.fortune_target = None
        return self


class Players(list):
    """参加者(複数)"""

    @property
    def alives(self) -> Players:
        """生存者(複数)"""
        return Players(p for p in self if not p.is_dead)

    @property
    def werewolfs(self) -> Players:
        """人狼(複数)"""
        return Players(p for p in self if p.role == '狼')

    @property
    def fortuneteller(self) -> Optional[Player]:
        """占い師"""
        for p in self:
            if p.role == '占':
                return p
        return None

    @property
    def votes(self) -> Players:
        """投票指定プレイヤー(複数)"""
        return Players(p.vote_target for p in self.alives)

    @property
    def raids(self) -> Players:
        """襲撃指定プレイヤー(複数)"""
        return Players(w.raid_target for w in self.alives.werewolfs)

    @property
    def most(self) -> Player:
        """最頻参加者"""
        aggregates = collections.Counter(self)
        maximum = max(aggregates.values())
        mosts = [a[0] for a in aggregates.most_common() if a[1] == maximum]
        return random.choice(mosts)

    def get(self, player_id) -> Player:
        for p in self:
            if p.id == player_id:
                return p
