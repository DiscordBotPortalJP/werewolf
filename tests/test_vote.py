import pytest
from cogs.vote import is_village_win, is_werewolf_win
from cogs.utils.player import Player


village_pattern = [
    ('村村村', True),
    ('村占狼村', False),
    ('村村狼狼', False),
]

werewolf_pattern = [
    ('村村村', False),
    ('村占狼村', False),
    ('村村狼狼', True),
]


@pytest.mark.parametrize('roles, expect', village_pattern)
def test_is_village_win(roles, expect):
    players = []
    for role in roles:
        player = Player(1)
        player.set_role(role)
        players.append(player)
    assert is_village_win(players) is expect


@pytest.mark.parametrize('roles, expect', werewolf_pattern)
def test_is_werewolf_win(roles, expect):
    players = []
    for role in roles:
        player = Player(1)
        player.set_role(role)
        players.append(player)
    assert is_werewolf_win(players) is expect
