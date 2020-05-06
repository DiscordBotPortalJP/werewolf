from cogs.utils.player import Player, execute, raid

player1 = Player(1)
player2 = Player(2)
player3 = Player(3)
player4 = Player(4)
player5 = Player(5)
players = (player1, player2, player3, player4, player5)


def test_execute():
    player1.set_vote(player2)
    player2.set_vote(player1)
    player3.set_vote(player3)
    player4.set_vote(player2)
    player5.set_vote(player1)

    assert execute(players) in (player1, player2)
    player5.set_vote(player2)
    assert execute(players) is player2
    assert player2.is_dead is True


def test_raid():
    player1.set_role('狼').set_raid(player4)
    player2.set_role('狼').set_raid(player5)
    assert raid(players) in (player4, player5)

    player1.set_raid(player3)
    player2.set_raid(player3)
    assert raid(players) is player3
    assert player3.is_dead is True
    assert raid(players) is None
