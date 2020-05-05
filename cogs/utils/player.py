# 参加者
class Player():
    def __init__(self, discord_id):
        self.id = discord_id  # Discord ID(int)
        self.role = '村人'  # 役職名(str)
        self.vote_target = None  # ?Player
        self.raid_target = None  # ?Player
        self.fortune_target = None  # ?Palyer

    def set_role(self, role):
        self.role = role
