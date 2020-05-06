import random
import collections


# 参加者
class Player():
    def __init__(self, discord_id):
        self.id = discord_id  # Discord ID(int)
        self.role = '村人'  # 役職名(str)
        self.is_dead = False
        self.vote_target = None  # ?Player
        self.raid_target = None  # ?Player
        self.fortune_target = None  # ?Palyer

    def set_dead(self):
        self.is_dead = True
        return self

    def set_role(self, role):
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

    def clear_raid_target(self):
        self.raid_target = None

    def clear_fortune_target(self):
        self.fortune_target = None


# プレイヤーのリストから人狼を抽出
def get_werewolfs(players):
    return [p for p in players if p.role == '狼']


# 指定リストから実行対象を選出
def targeting(specifications):
    max_specified_count = max(specifications.values())
    max_specified_players = []
    for vote in specifications.most_common():
        if vote[1] == max_specified_count:
            max_specified_players.append(vote[0])
        else:
            break
    return random.choice(max_specified_players)


# 処刑処理
def execute(players):
    specifications = collections.Counter(p.vote_target for p in players)
    target = targeting(specifications)
    return target.set_dead()


# 襲撃処理
def raid(players):
    werewolfs = get_werewolfs(players)
    specifications = collections.Counter(w.raid_target for w in werewolfs)
    target = targeting(specifications)
    if target.is_dead:
        return None
    return target.set_dead()
