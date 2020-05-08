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
