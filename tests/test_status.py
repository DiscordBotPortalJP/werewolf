from cogs.status import is_village_win, is_werewolf_win
from cogs.utils.player import Player


def test_is_village_win():
    players = []
    for role in '村村村':
        player = Player(1)
        player.set_role(role)
        players.append(player)
    assert is_village_win(players) is True


def test_is_werewolf_win():
    players = []
    for role in '村村狼狼':
        player = Player(1)
        player.set_role(role)
        players.append(player)
    assert is_werewolf_win(players) is True
