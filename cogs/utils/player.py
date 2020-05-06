import random
import collections
from typing import List, Optional


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

    def set_dead(self):
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

    def clear_vote_target(self):
        self.vote_target = None
        return self

    def clear_raid_target(self):
        self.raid_target = None
        return self

    def clear_fortune_target(self):
        self.fortune_target = None
        return self

    def get_side(self) -> str:
        """プレイヤーの陣営を取得"""
        if self.role in '村占':
            return '村人陣営'
        if self.role in '狼':
            return '人狼陣営'


def alive_players(players) -> List[Player]:
    """プレイヤーのリストから生存者を抽出"""
    return [p for p in players if not p.is_dead]


def get_werewolfs(players) -> List[Player]:
    """プレイヤーのリストから人狼を抽出"""
    return [p for p in players if p.role == '狼']


def get_fortuneteller(players) -> Optional[Player]:
    """プレイヤーのリストから占い師を抽出"""
    for p in players:
        if p.role == '占':
            return p
    return None


def is_set_target(players) -> bool:
    """全員が指定完了しているか"""
    for p in players:
        if p.vote_target is None:
            return False
        if p.role == '狼' and p.raid_target is None:
            return False
        if p.role == '占' and p.fortune_target is None:
            return False
    return True


def targeting(specifications) -> Player:
    """指定リストから実行対象を選出"""
    max_specified_count = max(specifications.values())
    max_specified_players = []
    for vote in specifications.most_common():
        if vote[1] == max_specified_count:
            max_specified_players.append(vote[0])
        else:
            break
    return random.choice(max_specified_players)


def execute(players) -> Player:
    """処刑処理"""
    specifications = collections.Counter(p.vote_target for p in players)
    target = targeting(specifications)
    return target.set_dead()


def raid(players) -> Optional[Player]:
    """襲撃処理"""
    werewolfs = get_werewolfs(players)
    specifications = collections.Counter(w.raid_target for w in werewolfs)
    target = targeting(specifications)
    if target.is_dead:
        return None
    return target.set_dead()


def fortune(players) -> Optional[str]:
    """占い処理"""
    fortuneteller = get_fortuneteller(players)
    if fortuneteller is not None:
        return fortuneteller.fortune_target.get_side()
    return None
