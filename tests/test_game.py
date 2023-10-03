import pytest
from application.game import Game
from application.player import Player

player1 = Player(1)
player2 = Player(2)
player3 = Player(3)
player4 = Player(4)
player5 = Player(5)
game = Game()
game.players.append(player1)
game.players.append(player2)
game.players.append(player3)
game.players.append(player4)
game.players.append(player5)


def test_is_set_target():
    player1.set_vote(player2)
    player2.set_vote(player3)
    player3.set_vote(player4)
    player4.set_vote(player5)
    assert game.is_set_target() is False

    player5.set_vote(player1)
    player1.set_role('狼')
    assert game.is_set_target() is False

    player1.set_raid(player2)
    player5.set_role('占')
    assert game.is_set_target() is False

    player5.set_fortune(player1)
    assert game.is_set_target() is True


def test_execute():
    player1.set_vote(player2)
    player2.set_vote(player1)
    player3.set_vote(player3)
    player4.set_vote(player2)
    player5.set_vote(player1)

    game.execute()
    assert game.executed in (player1, player2)

    player5.set_vote(player2)
    game.execute()
    assert game.executed is player2
    assert player2.is_dead is True


def test_raid():
    player1.is_dead = False
    player2.is_dead = False
    player1.set_role('狼').set_raid(player4)
    player2.set_role('狼').set_raid(player5)
    game.raid()
    assert game.raided in (player4, player5)

    player1.set_raid(player3)
    player2.set_raid(player3)
    game.raid()
    assert game.raided is player3
    assert player3.is_dead is True

    game.raided = None
    game.raid()
    assert game.raided is None


def test_fortune():
    player1.is_dead = False
    player5.is_dead = False
    player1.set_role('狼')
    player5.set_role('占').set_fortune(player1)
    game.fortune()
    assert game.fortuned == '人狼陣営'

    player1.set_role('村')
    game.fortune()
    assert game.fortuned == '村人陣営'


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
    game = Game()
    for role in roles:
        player = Player(1)
        player.set_role(role)
        game.players.append(player)
    assert game.is_village_win() is expect


@pytest.mark.parametrize('roles, expect', werewolf_pattern)
def test_is_werewolf_win(roles, expect):
    game = Game()
    for role in roles:
        player = Player(1)
        player.set_role(role)
        game.players.append(player)
    assert game.is_werewolf_win() is expect
